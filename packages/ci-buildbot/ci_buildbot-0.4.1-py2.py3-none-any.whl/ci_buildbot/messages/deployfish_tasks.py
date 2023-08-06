from .mixins import (
    GitMixin,
    PythonMixin,
    CodebuildMixin,
    DeployfishTasksDeployMixin,
    Message
)


class DeployfishTasksDeployStartMessage(DeployfishTasksDeployMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'deploy_tasks_start.tpl'


class DeployfishTasksDeploySuccessMessage(DeployfishTasksDeployMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'deploy_tasks_success.tpl'


class DeployfishTasksDeployFailureMessage(DeployfishTasksDeployMixin, CodebuildMixin, GitMixin, PythonMixin, Message):
    template = 'deploy_tasks_failed.tpl'
