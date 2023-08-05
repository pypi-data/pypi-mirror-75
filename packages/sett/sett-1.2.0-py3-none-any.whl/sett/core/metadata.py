from dataclasses import dataclass

from libbiomedit import metadata as _metadata

from .model import user_is_authorized_for_project
from .error import UserError

# Reexports
AlnumStr = _metadata.AlnumStr
ProjectIdStr = _metadata.ProjectIdStr
METADATA_FILE = _metadata.METADATA_FILE


@dataclass(frozen=True)
class MetaData(_metadata.MetaData):
    """Wrapper around libbiomedit.metadata.MetaData throwing UserError"""
    @classmethod
    def from_dict(cls, d: dict):
        try:
            return super().from_dict(d)
        except ValueError as e:
            raise UserError(format(e))


def load_metadata(metadata: dict, projects_by_id: dict) -> MetaData:
    """Verify the projectID and sender fingerprint present in the json file are
    present in the mapping lists for file transfer and sender ID."""

    m = MetaData.from_dict(metadata)

    project = projects_by_id.get(m.projectID)
    if project is None:
        raise UserError(
            f"Unauthorized projectID '{m.projectID}' found in json file.")
    if not user_is_authorized_for_project(m.sender, project):
        raise UserError(
            f"Unauthorized sender '{m.sender}' found in json file.")
    return m
