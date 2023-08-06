from typing import List, Union, Optional
from pathlib import Path
import re
import os

import boto3
from mypy_boto3_s3 import S3ServiceResource
from mypy_boto3_s3.service_resource import Bucket, ObjectSummary, Object
import botocore
import rasterio

from .exceptions import UP42Error, SupportedErrors
from .logging import get_logger

logger = get_logger(__name__)


def get_s3(
    aws_access_key_id: str, aws_secret_access_key: str, region_name: str = "eu-west-1"
) -> S3ServiceResource:
    try:
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
    except ValueError:
        raise UP42Error(
            SupportedErrors.API_CONNECTION_ERROR,
            "Google cloud authentication was not successful, please check your credentials.",
        )
    return s3


def get_bucket(s3: S3ServiceResource, bucket_name: str) -> Bucket:
    """
	Checks if the buckets exists, raises if bucket not available.
	"""
    # pylint: disable=attribute-defined-outside-init

    try:
        assert s3.meta.client.head_bucket(Bucket=bucket_name)
        bucket = s3.Bucket(bucket_name)
    except s3.meta.client.exceptions.ClientError:
        raise UP42Error(
            SupportedErrors.INPUT_PARAMETERS_ERROR,
            f"Bucket with name {bucket_name} is not available!",
        )
    return bucket


def open_rasterio_fly(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    blob: Optional[Object] = None,
    s3_url: Optional[str] = None,
) -> rasterio.io.DatasetReader:
    """
    Opens a rasterio dataset on s3 on the fly - without downloading.

    Args:
        blob: AWS blob object, with attributes bucket-name (blocks-e2e-testing)
            & key (`e2e_geotiff_custom/folder2/fb520cc5-7bb7-41c9-bf17-1b15a0560f2a_ms.tif`)
        s3_url: Direct s3 file url (`s3://blocks-e2e-testing/e2e_geotiff_custom/
            folder2/fb520cc5-7bb7-41c9-bf17-1b15a0560f2a_ms.tif`)

    Returns:
        Open rasterio object.
    """
    if blob is not None and s3_url is None:
        s3_url = f"s3://{blob.bucket_name}/{blob.key}"
        filename = blob.key.split("/")[-1]
    elif blob is None and s3_url is not None:
        filename = str(Path(s3_url).name)
    else:
        raise ValueError("Provide either s3_url or blob.")

    with rasterio.Env(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    ):
        src = rasterio.open(s3_url)

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
    blobs = bucket.objects.filter(Prefix=prefix_scene)
    for blob in blobs:
        if not blob.key.endswith("/"):
            scene_id = folder_url.split("/")[-1]
            file_name = blob.key.partition(f"{scene_id}/")[-1]
            out_fp = out_dir / scene_id / file_name
            out_fp.parent.mkdir(parents=True, exist_ok=True)
            try:
                bucket.download_file(blob.key, str(out_fp))
            except botocore.exceptions.ClientError:
                raise UP42Error(
                    SupportedErrors.NO_INPUT_ERROR,
                    "Download was unsuccessful - found no files in the bucket!",
                )

    logger.info(f"Download successful for files in {folder_url}.")


def download_file(bucket: Bucket, file_key: str, out_file: str):
    """
    Downloads a single file object from aws s3.

    Args:
        file_key: file key (file url without `s3://bucketname/`). Also accepts the file
            url.
        out_file: The out filepath.
    """
    # Also accept file url.
    if "s3://" in file_key:
        file_key = file_key.partition(f"s3://{bucket.name}/")[-1]

    try:
        bucket.download_file(file_key, out_file)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.info(f"Object {file_key} does not exist - skipping.")
        else:
            raise


def filter_blobs_regex(
    blobs: List[ObjectSummary], regex_pattern: str
) -> List[ObjectSummary]:
    """
    Filters blobs by a regex pattern for the blob names.

    Example filtering pattern for GeoTIFF format:
        `regex_pattern ="(.+TIF|.+tif|.+TIFF|.+tiff)"`
    Example of filtering pattern for Dimap format:
        `regex_pattern = "(DIM_)(.*)((_P_*)|(_PMS_*))(.*)(.XML)"`
    """
    filtered_blobs = []
    for blob in blobs:
        blob_filename = blob.key.split("/")[-1]
        if re.match(regex_pattern, blob_filename):
            filtered_blobs.append(blob)

    if not filtered_blobs:
        raise UP42Error(
            SupportedErrors.NO_INPUT_ERROR,
            "Search was unsuccessful - found no files with the selected pattern in the bucket!",
        )
    return filtered_blobs


def create_secrets_files(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region: str = "eu-west-1",
    output_format: str = "json",
):
    my_dir = os.path.expanduser("~/.aws")
    if not os.path.exists(my_dir):
        os.makedirs(my_dir)

    config_file_str = f"""[default]
        region = {region}
        output = {output_format}
        """
    with open(os.path.join(my_dir, "config"), "w") as fp:
        fp.write(config_file_str)

    credentials_file_str = f"""[default]
        aws_access_key_id = {aws_access_key_id}
        aws_secret_access_key = {aws_secret_access_key}
        """
    with open(os.path.join(my_dir, "credentials"), "w") as fp:
        fp.write(credentials_file_str)
