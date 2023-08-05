from typing import List

from ..core.crypt import request_key_signature
from ..core.error import UserError
from ..utils.log import create_logger


logger = create_logger(__name__)


@logger.exception_to_message(UserError)
def request_sigs(key_ids: List[str], *, portal_pgpkey_endpoint_url: str):
    """Requests signatures"""
    for key in key_ids:
        logger.info("Sending a request for '%s'", key)
        request_key_signature(key, portal_pgpkey_endpoint_url)
