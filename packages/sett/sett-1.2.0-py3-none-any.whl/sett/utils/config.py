import os
import platform
import json
from typing import List, Dict, Any, Optional
import urllib.error
import tempfile

import dataclasses
from dataclasses import dataclass

from libbiomedit.lib.deserialize import deserialize

from .log import exception_to_message, get_default_log_dir
from ..core.model import Project
from ..core.crypt import open_gpg_dir, get_default_gpg_config_dir
from ..core.error import UserError
from ..core.request import urlopen
from .. import APP_NAME_SHORT


CONFIG_FILE_NAME = "config.json"

conf_sub_dir_by_os = {
    "Linux": (".config",),
    "Darwin": (".config",),
    "Windows": ("AppData", "Roaming")
}


@dataclass(frozen=True)
class Connection:
    """dataclass holding config fo a connection (sftp / liquid files)"""
    protocol: str
    parameters: Dict[str, Any]


TMP_DIR = tempfile.gettempdir()


@dataclass
class Config:
    """dataclass holding config data"""

    dcc_portal_url: str = "https://portal.dcc.sib.swiss"
    keyserver_url: str = 'keyserver.dcc.sib.swiss'
    gpg_config_dir: str = get_default_gpg_config_dir()
    key_validation_authority_keyid: str = "881685B5EE0FCBD3"
    sign_encrypted_data: bool = True
    always_trust_recipient_key: bool = True
    repo_url: str = "https://pypi.org"
    check_version: bool = True
    offline: bool = False
    log_dir: str = get_default_log_dir()
    log_max_file_number: int = 1000
    connections: Dict[str, Connection] = dataclasses.field(
        default_factory=lambda: {})
    temp_dir: str = TMP_DIR
    ssh_password_encoding: str = "utf_8"
    default_sender: Optional[str] = None

    @property
    def dcc_portal_endpoint_url(self) -> str:
        return self.dcc_portal_url + "/backend/projects-info"

    @property
    def dcc_portal_pgpkey_endpoint_url(self) -> str:
        return self.dcc_portal_url + "/backend/pgpkey/"

    @property
    def projects_by_id(self):
        projects = load_projects(self)
        return {p.project_id: p for p in projects}  # pylint: disable=not-an-iterable

    @property
    def gpg_store(self):
        return exception_to_message(UserError)(open_gpg_dir)(self.gpg_config_dir)


@exception_to_message()
def load_config() -> Config:
    """Loads the config, returning a Config object"""

    migrate_repo_url()

    cfg_dct = sys_config_dict()
    cfg_dct.update(load_config_dict(get_config_file()))
    return deserialize(Config)(cfg_dct)


def create_config() -> str:
    """Creates a new config file in the home directories config folder

    :return: The path of the created file"""

    config_dir = get_config_dir()
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    config_file = get_config_file()

    with open(config_file, 'w') as f:
        json.dump(config_to_dict(default_config()),
                  f, indent=2, sort_keys=True)
    return config_file


def config_to_dict(config: Config) -> dict:
    """Converts a Config object into a dict"""
    return dataclasses.asdict(config)


def default_config() -> Config:
    """Creates a new Config object with default values"""
    return deserialize(Config)(sys_config_dict())


def sys_config_dict() -> dict:
    """On linux only: try to load global sys config.
    If the env variable `SYSCONFIG` is set search there, else in
    `/etc/{APP_NAME_SHORT}`"""
    if platform.system() == "Linux":
        sys_cfg_dir = os.environ.get("SYSCONFIG", os.path.join(
            "/etc", APP_NAME_SHORT))
        return load_config_dict(os.path.join(sys_cfg_dir, CONFIG_FILE_NAME))
    return {}


def load_config_dict(path: str) -> dict:
    """Load raw config as a dict"""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_projects(config: Config) -> List[Project]:
    """Fetches the list of projects from the portal"""
    if not config.dcc_portal_endpoint_url.lower().startswith('http'):
        raise ValueError(f"Invalid scheme: '{config.dcc_portal_endpoint_url}'")
    try:
        with urlopen(config.dcc_portal_endpoint_url) as response:
            projects = json.loads(response.read().decode())
            return [Project(**project) for project in projects]
    except (urllib.error.URLError, json.decoder.JSONDecodeError,
            TypeError) as e:
        raise UserError(f"Failed to load projects. {format(e)}")


def get_config_file() -> str:
    """user platform specific config file"""

    return os.path.join(get_config_dir(), CONFIG_FILE_NAME)


def get_config_dir() -> str:
    """user platform specific config direcory"""

    return os.path.join(
        os.path.expanduser("~"),
        *conf_sub_dir_by_os[platform.system()],
        APP_NAME_SHORT)


def migrate_repo_url():
    """Migrate repo URL inside the config"""
    cfg_file = get_config_file()
    try:
        with open(cfg_file) as f:
            config_dict = json.load(f)
        if config_dict.get("repo_url") == "https://pypi.dcc.sib.swiss":
            config_dict["repo_url"] = Config().repo_url
        with open(cfg_file, "w") as f:
            json.dump(config_dict, f, indent=2, sort_keys=True)
    except FileNotFoundError:
        pass
