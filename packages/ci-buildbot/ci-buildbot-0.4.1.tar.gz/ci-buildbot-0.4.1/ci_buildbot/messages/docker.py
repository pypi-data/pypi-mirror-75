from .mixins import (
    PythonMixin,
    GitMixin,
    CodebuildMixin,
    DockerMixin,
    DockerImageNameMixin,
    Message
)


class DockerStartMessage(DockerImageNameMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'docker_start.tpl'


class DockerSuccessMessage(DockerImageNameMixin, DockerMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'docker_success.tpl'


class DockerFailureMessage(DockerImageNameMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'docker_failed.tpl'
