from .mixins import (
    GitMixin,
    PythonMixin,
    CodebuildMixin,
    DeployfishDeployMixin,
    Message
)


class DeployfishDeployStartMessage(DeployfishDeployMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'deploy_start.tpl'


class DeployfishDeploySuccessMessage(DeployfishDeployMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'deploy_success.tpl'


class DeployfishDeployFailureMessage(DeployfishDeployMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'deploy_failed.tpl'
