from typing import List

from ..core.crypt import upload_keys as crypt_upload_keys
from ..core.error import UserError
from ..utils.log import create_logger


logger = create_logger(__name__)


@logger.exception_to_message(UserError)
def upload_keys(keys: List[str], keyserver: str, gpg_store):
    """Upload keys"""
    logger.info("Uploading keys '%s'", ", ".join(keys))
    crypt_upload_keys(keys, keyserver=keyserver, gpg_store=gpg_store)
