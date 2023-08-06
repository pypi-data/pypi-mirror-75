import json
import re
from typing import List, Union, Optional
from pathlib import Path

from google.cloud.storage import Client, Blob, Bucket
from google.cloud import exceptions
import rasterio

from .exceptions import UP42Error, SupportedErrors
from .logging import get_logger

logger = get_logger(__name__)


def create_gac_json(gac_string: str):
    """
    Create json with GCS credentials to use for verification.
    """
    gac_string = json.loads(gac_string, strict=False)

    gcs_json_path = "/tmp/input/GOOGLE_APPLICATION_CREDENTIALS.json"
    with open(gcs_json_path, "w") as f:
        json.dump(gac_string, f)
    return gcs_json_path


def get_s3(gcs_json_path: str) -> Client:
    """
    Handles & tests the authentication with GCS by creating the credentials json and
    setting the env variable for the json path.
    """
    try:
        s3 = Client.from_service_account_json(gcs_json_path)
    except ValueError:
        raise UP42Error(
            SupportedErrors.API_CONNECTION_ERROR,
            "Google cloud authentication was not successful, please check your credentials.",
        )

    return s3


def get_bucket(s3: Client, bucket_name: str) -> Bucket:
    """
    Gets the bucket object, raises if bucket not available.
    """
    # pylint: disable=attribute-defined-outside-init
    bucket = s3.lookup_bucket(bucket_name=bucket_name)
    if bucket is None:
        raise UP42Error(
            SupportedErrors.INPUT_PARAMETERS_ERROR,
            f"Bucket with name {bucket_name} is not available!",
        )
    return bucket


def open_rasterio_fly(
    gcs_json_path: str, blob: Optional[Blob] = None, s3_url: Optional[str] = None
) -> rasterio.io.DatasetReader:
    """
    Opens a rasterio dataset on s3 on the fly - without downloading.

    Args:
        blob: Gcs blob object, with attributes bucket-name (blocks-e2e-testing) &
            key (`e2e_geotiff_custom/folder2/fb520cc5-7bb7-41c9-bf17-1b15a0560f2a_ms.tif`)
        s3_url: Direct s3 file url (`gs://blocks-e2e-testing/e2e_geotiff_custom/
            folder2/fb520cc5-7bb7-41c9-bf17-1b15a0560f2a_ms.tif`)

    Returns:
        Open rasterio object.
    """
    # TODO: See if direct use of credentials as arguments (not json credentials file) ..
    # TODO: .. would also require rasterio --no-binary installation.
    if blob is not None and s3_url is None:
        s3_url = f"gs://{blob.bucket.name}/{blob.name}"
        filename = blob.name.split("/")[-1]
        gdal_url = f"/vsigs_streaming/{blob.bucket.name}/{blob.name}"
    elif blob is None and s3_url is not None:
        filename = str(Path(s3_url).name)
        gdal_url = f"/vsigs_streaming/{s3_url.split('//')[-1]}"
    else:
        raise ValueError("Provide either s3_url or blob.")

    with rasterio.Env(GOOGLE_APPLICATION_CREDENTIALS=gcs_json_path,):
        src = rasterio.open(gdal_url)
    return src, s3_url, filename


def download_folder(bucket: Bucket, folder_url: str, out_dir: Union[str, Path]):
    """
    Clones a specific folder in the bucket to the output directory.

    Args:
        folder_url: GCS URL of the selected directory.
    Examples:
        `gcs_folder_url = "gs://blocks-e2e-testing/e2e_dimap_custom/test_prefix_dir/
        DS_PHR1A_202005061019188_FR1_PX_E013N52_0513_01183/"`

    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if folder_url.endswith("/"):
        folder_url = folder_url[:-1]

    prefix_scene = folder_url.partition(f"{bucket.name}/")[-1]
    blobs = list(bucket.list_blobs(prefix=prefix_scene))
    for blob in blobs:
        if not blob.name.endswith("/"):
            scene_id = folder_url.split("/")[-1]
            file_name = blob.name.partition(f"{scene_id}/")[-1]
            out_fp = out_dir / scene_id / file_name
            out_fp.parent.mkdir(parents=True, exist_ok=True)
            try:
                blob.download_to_filename(out_fp)
            except exceptions.NotFound:
                raise UP42Error(
                    SupportedErrors.NO_INPUT_ERROR,
                    "Download was unsuccessful - found no files in the bucket!",
                )

    logger.info(f"Download successful for files in {folder_url}.")


def download_file(bucket: Bucket, file_url: str, out_file: Union[str, Path]):
    """
    Clones a file in the bucket to the output directory.
    Examples:
        `gcs_file_url = "gs://blocks-e2e-testing/e2e_geotiff_custom/folder1/
        33c03020-2797-4bd4-b3b7-763d4de12754_ms.tif"`
        `out_file = "/tmp/output/33c03020-2797-4bd4-b3b7-763d4de12754_ms.tif"`
    """
    out_file = Path(out_file)

    tif_prefix = file_url.partition(f"gs://{bucket.name}/")[-1]
    blob = Blob(name=tif_prefix, bucket=bucket)
    try:
        blob.download_to_filename(out_file)
    except exceptions.NotFound:
        raise UP42Error(
            SupportedErrors.NO_INPUT_ERROR,
            "Download was unsuccessful - found no files in the bucket!",
        )

    logger.info("Download was successful.")


def filter_blobs_regex(blobs: List[Blob], regex_pattern: str) -> List[Blob]:
    """
    Filters blobs by a regex pattern for the blob names.

    Example filtering pattern for GeoTIFF format:
        `regex_pattern ="(.+TIF|.+tif|.+TIFF|.+tiff)"`
    Example of filtering pattern for Dimap format:
        `regex_pattern = "(DIM_)(.*)((_P_*)|(_PMS_*))(.*)(.XML)"`
    """
    filtered_blobs = []
    for blob in blobs:
        blob_filename = blob.name.split("/")[-1]
        if re.match(regex_pattern, blob_filename):
            filtered_blobs.append(blob)

    if not filtered_blobs:
        raise UP42Error(
            SupportedErrors.NO_INPUT_ERROR,
            "Search was unsuccessful - found no files with the selected pattern in the bucket!",
        )
    return filtered_blobs
