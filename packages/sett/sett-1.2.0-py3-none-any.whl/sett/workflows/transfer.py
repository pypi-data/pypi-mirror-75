import typing
import json

from ..utils.config import Config
from ..utils.log import create_logger
from ..utils.progress import ProgressInterface
from ..core.crypt import get_recipient_email, extract_pub_key_ids, \
    validated_keys_by_ids
from ..core.archive import check_tar, extract, METADATA_FILE, DATA_FILE_ENCRYPTED
from ..core.metadata import load_metadata
from ..core.error import UserError
from ..protocols import needs_argument


logger = create_logger(__name__)


@logger.exception_to_message((UserError, FileNotFoundError))
def transfer(files: typing.List[str],
             *,
             protocol,
             two_factor_callback: typing.Callable,
             protocol_args: dict,
             config: Config,
             dry_run: bool = False,
             progress: ProgressInterface = None):
    """ Transfer file to the selected recipient on the BiomedIT network.
    """

    logger.info("""Input summary:
    files to transfer: %s"
    dry run          : %s""",
                "\n\t".join(files), str(dry_run))

    with logger.log_task("Input files verification"):
        for tar in files:
            check_tar(tar)

    files_by_recipient = {}
    with logger.log_task("Extracting destination for each file to transfer"):
        for tar in files:
            logger.info("\t-> %s", tar)
            with extract(open(tar, 'rb'), METADATA_FILE, DATA_FILE_ENCRYPTED) \
                    as (metadata, encrypted_file):
                metadata = json.load(metadata)
                keys = tuple(validated_keys_by_ids(
                    extract_pub_key_ids(encrypted_file),
                    config.gpg_store,
                    config.key_validation_authority_keyid,
                    config.keyserver_url))
            metadata = load_metadata(metadata, config.projects_by_id)
            project_id = metadata.projectID
            project = config.projects_by_id.get(project_id)
            if project is None:
                raise KeyError(f"Could not find project with id {project_id}")
            files_by_recipient.setdefault(keys, []).append(tar)

    if dry_run:
        logger.info("Dry run completed successfully")
        return

    for recipient_keys, r_files in files_by_recipient.items():
        emails = [get_recipient_email(k) for k in recipient_keys]
        if needs_argument(protocol, "recipients"):
            protocol_args["recipients"] = emails
        if needs_argument(protocol, "two_factor_callback"):
            protocol_args["two_factor_callback"] = two_factor_callback
        if needs_argument(protocol, "pkey_password_encoding"):
            protocol_args["pkey_password_encoding"] = config.ssh_password_encoding
        with logger.log_task("Transferring files encrypted for "
                             f"{', '.join(emails)}"):
            protocol(r_files, progress=progress, **protocol_args)
