import typing
from dataclasses import dataclass, field


@dataclass
class User:
    first_name: str
    last_name: str
    email: str


@dataclass
class Project:
    name: str
    project_id: str
    users: typing.List[User] = field(default_factory=list)
    protocol_parameters: dict = field(default_factory=dict)


def user_is_authorized_for_project(user: str, project: Project) -> bool:  # pylint: disable=unused-argument
    return True
