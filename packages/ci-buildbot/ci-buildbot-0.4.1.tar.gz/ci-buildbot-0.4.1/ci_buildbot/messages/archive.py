
from .mixins import (
    CodebuildMixin,
    PythonMixin,
    GitMixin,
    GitChangelogMixin,
    Message
)


class ArchiveCodeMessage(GitChangelogMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'archive.tpl'
