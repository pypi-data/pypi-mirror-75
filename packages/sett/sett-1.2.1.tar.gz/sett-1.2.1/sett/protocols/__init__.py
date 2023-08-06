import inspect

from . import liquid_files, sftp
from ..core.error import UserError


protocols = (liquid_files, sftp)
protocols_by_name = {p.__name__.replace(
    __name__ + ".", ""): p.upload for p in protocols}

__all__ = tuple(protocols_by_name)


def parse_protocol(s):
    try:
        return protocols_by_name[s]
    except KeyError:
        raise UserError(f"Invalid protocol: {s}")


def needs_argument(protocol, argument):
    args = inspect.signature(protocol)
    return argument in args.parameters
