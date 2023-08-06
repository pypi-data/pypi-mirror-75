import datetime

from distutils.core import run_setup
import json
import os
import pathlib
import time
from typing import Dict

import docker
from git import Repo
from giturlparse import parse
from pytz import timezone
import sh

from ci_buildbot import __version__
from ..settings import jinja_env


class Message:

    template = None

    def get_template(self):
        return self.template

    def format(self):
        """
        Generate the full JSON string to send to slack.
        """
        values = {}
        self.annotate(values)
        now = datetime.datetime.now(timezone('UTC'))
        now_pacific = now.astimezone(timezone('US/Pacific'))
        values['completed_date'] = now_pacific.strftime('%Y-%m-%d %H:%M %Z')
        values['buildbot'] = f'ci-buildbot-{__version__}'
        template = jinja_env.get_template(self.get_template())
        return(json.loads(template.render(**values)))


class AnnotationMixin:

    def annotate(self, values: Dict[str, str]):
        pass


class PythonMixin(AnnotationMixin):

    def annotate(self, values: Dict[str, str]):
        """
        Extract some stuff from setup.py, if present.

        If setup.py is present, we'll add the following keys to `values`:

        * `name`: the output of `python setup.py name`
        * `version`: the output of `python setup.py version`

        """
        super().annotate(values)
        setup_py = pathlib.Path.cwd() / 'setup.py'
        if setup_py.exists():
            # Extract some stuff from python itself
            python_setup = run_setup(str(setup_py))
            values['name'] = python_setup.get_name()
            values['version'] = python_setup.get_version()


class GitMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        self.repo = None
        self.url_patterns = {}
        self.__get_repo()
        self.__build_url_patterns()
        super().__init__()

    def __get_repo(self):
        if not self.repo:
            self.repo = Repo('.')

    def __build_url_patterns(self):
        # https://caltech-imss-ads@bitbucket.org/caltech-imss-ads/exeter_api/src/0.10.2/
        #
        if not self.url_patterns:
            p = parse(self.repo.remote().url)
            host = p.host
            if host.startswith('codestar-connections'):
                # We're in a CodePipeline, and our true origin is masked.  Assume bitbucket.
                host = "bitbucket.org"
            origin_url = f"https://{host}/{p.owner}/{p.repo}"
            if origin_url.endswith('.git'):
                origin_url = origin_url[:-4]
            if p.github:
                self.url_patterns['commit'] = f"<{origin_url}/commit/" + "{sha}|{sha}>"
                self.url_patterns['project'] = f"<{origin_url}/tree/" + "{version}|{name}>"
                self.url_patterns['diff'] = f"{origin_url}/compare/" + "{from_sha}..{to_sha}"
            else:
                # Assume bitbucket
                self.url_patterns['commit'] = f"<{origin_url}/commits/" + "{sha}|{sha}>"
                self.url_patterns['project'] = f"<{origin_url}/src/" + "{version}/|{name}>"
                self.url_patterns['diff'] = f"{origin_url}/branches/compare/" + "{from_sha}..{to_sha}#diff"
            self.url_patterns['repo'] = origin_url

    def __get_last_version(self, values: Dict[str, str]):
        """
        Update the `values` dict with:

        * `previous_version`: the version number for the tag immediately preceeding ours
        * `last_version_sha`: the sha that that tag points to
        """
        # Get all tags, sorted by the authored_date on their associated commit.  We should have at least one tag -- the
        # one for this commit.
        ordered_tags = sorted(self.repo.tags, key=lambda x: x.commit.authored_date)
        if len(ordered_tags) >= 2:
            # If there are 2 or more tags, there was a previous version.
            # Extract info from the tag preceeding this one.
            values['last_version_sha'] = ordered_tags[-2].commit.hexsha
            values['last_version_url'] = self.url_patterns['project'].format(
                version=values['version'],
                name=f"{values['name']}-{values['version']}"
            )
            values['previous_version'] = ordered_tags[-2].name
        else:
            # There was just our current version tag, and no previous tag.  Go back to the initial commit.
            commits = list(self.repo.iter_commits())
            commits.reverse()
            values['last_version_sha'] = commits[0].hexsha
            values['last_version_url'] = self.url_patterns['project'].format(
                version=values['version'],
                name=f"{values['name']}-{values['version']}"
            )
            values['previous_version'] = "initial"

    def get_branch(self):
        try:
            return self.repo.head.reference.name
        except TypeError:
            # We're in DETACHED_HEAD state, so we have no branch name
            return ''

    def git_changelog(self, values: Dict[str, str]):
        """
        Look through the commits between the current version and the last version
        Update `values` with two new keys:

        * `authors`: a list of all authors in those commits
        * `changelog`: a list of strings representing the commits
        """
        # get the changes between here and the previous tag
        changelog_commits = []
        current = self.repo.head.commit
        # Gather all commits from HEAD to `last_version_sha`
        while True:
            changelog_commits.append(current)
            if current.hexsha == values['last_version_sha']:
                break
            current = current.parents[0]
        changelog = []
        authors = set()
        for commit in changelog_commits:
            authors.add(commit.author.name)
            d = datetime.datetime.fromtimestamp(commit.committed_date).strftime("%Y/%m/%d")
            commit_link = self.url_patterns['commit'].format(sha=commit.hexsha[0:7])
            changelog.append(f"{commit_link} [{d}] {commit.summary} - {str(commit.author)}")
        values['authors'] = sorted(authors)
        values['changelog'] = changelog

    def __get_concise_info(self):
        branch = self.get_branch()
        current = self.repo.head.commit
        sha = current.hexsha[0:7]
        sha_url = self.url_patterns['commit'].format(sha=sha)
        committer = f"{current.author.name} <{current.author.email}>"
        return f"{branch} {sha_url} {committer}"

    def annotate(self, values: Dict[str, str]):
        """
        Extract info about the git repo.  Assume we're in the checked out clone.
        """
        super().annotate(values)
        headcommit = self.repo.head.commit
        values['committer'] = str(headcommit.author)
        values['sha'] = headcommit.hexsha
        values['branch'] = self.get_branch()
        self.__get_last_version(values)
        # Add the diff URL
        if 'diff' in self.url_patterns:
            values['diff_url'] = self.url_patterns['diff'].format(
                from_sha=values['sha'][0:7],
                to_sha=values['last_version_sha'][0:7],
            )
        values['git_info'] = self.__get_concise_info()


class GitChangelogMixin:
    """
    This needs to be used after GitMixin in the inheritance chain.
    """

    def annotate(self, values: Dict[str, str]):
        """
        Look through the commits between the current version and the last version
        Update `values` with two new keys:

        * `authors`: a list of all authors in those commits
        * `changelog`: a list of strings representing the commits
        """
        super().annotate(values)
        # get the changes between here and the previous tag
        changelog_commits = []
        current = self.repo.head.commit
        # Gather all commits from HEAD to `last_version_sha`
        while True:
            changelog_commits.append(current)
            if current.hexsha == values['last_version_sha']:
                break
            try:
                current = current.parents[0]
            except IndexError:
                # We really should never get here
                break
        changelog = []
        authors = set()
        for commit in changelog_commits:
            authors.add(commit.author.name)
            d = datetime.datetime.fromtimestamp(commit.committed_date).strftime("%Y/%m/%d")
            commit_link = self.url_patterns['commit'].format(sha=commit.hexsha[0:7])
            # escape any double quotes in the summary
            summary = commit.summary.replace('"', r'\"')
            changelog.append(f"{commit_link} [{d}] {summary} - {str(commit.author)}")
        values['authors'] = sorted(authors)
        values['changelog'] = changelog


class CodebuildMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        if 'log_group' in kwargs:
            self.log_group = kwargs['log_group']
        super().__init__(*args, **kwargs)

    def get_build_log_url(self, values):
        # arn:aws:codebuild:us-west-2:467892444047:build/terraform-caltech-commons-DockerImageBuild:87bd7955-6c38-4554-b353-ac67880e1347
        fields = os.environ['CODEBUILD_BUILD_ARN'].split(':')
        values['account_id'] = fields[4]
        values['build_project_name'] = fields[5].split('/')[1]
        values['build_id'] = fields[6]
        # https://us-west-2.console.aws.amazon.com/codesuite/codebuild/467892444047/projects/terraform-caltech-commons-archive/build/terraform-caltech-commons-archive%3Aee76bb3e-fd96-4448-8644-eee93cd0d02b/log?region=us-west-2
        # https://us-west-2.console.aws.amazon.com/codesuite/codebuild/467892444047/projects/terraform-caltech-commons-DockerImageBuild/build/terraform-caltech-commons-DockerImageBuild%87bd7955-6c38-4554-b353-ac67880e1347/log?region=us-west-2
        values['build_status_url'] = f"<https://{values['region']}.console.aws.amazon.com/codesuite/codebuild/{values['account_id']}/projects/{values['build_project_name']}/build/{values['build_project_name']}%3A{values['build_id']}/log?region=us-west-2|Click here>"

    def get_pipeline_url(self, values):
        # https://us-west-2.console.aws.amazon.com/codesuite/codepipeline/pipelines/terraform-caltech-commons/view?region=us-west-2
        values['pipeline'] = os.environ['CODEBUILD_INITIATOR'].split('/')[1]
        values['pipeline_url'] = f"<https://{values['region']}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{values['pipeline']}/view?region=us-west-2|{values['pipeline']}>"

    def annotate(self, values: Dict[str, str]):
        super().annotate(values)
        values['status'] = 'Success' if 'CODEBUILD_BUILD_SUCCEEDING' in os.environ else 'Failed'
        values['region'] = os.environ['AWS_DEFAULT_REGION']
        values['build_id'] = os.environ.get('CODEBUILD_BUILD_ID', None)
        build_seconds = time.time() - float(os.environ['CODEBUILD_START_TIME']) / 1000
        build_minutes = int(build_seconds // 60)
        build_seconds = int(build_seconds - build_minutes * 60)
        values['build_time'] = f"{build_minutes}m {build_seconds}s"
        self.get_build_log_url(values)
        self.get_pipeline_url(values)


class DockerImageNameMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        if 'image' in kwargs:
            self.image = kwargs['image']
            del kwargs['image']
        super().__init__(*args, **kwargs)

    def annotate(self, values):
        super().annotate(values)
        values['short_image'] = os.path.basename(self.image)


class DockerMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        if 'image' in kwargs:
            self.image = kwargs['image']
            del kwargs['image']
        super().__init__(*args, **kwargs)

    def annotate(self, values: Dict[str, str]):
        super().annotate(values)
        client = docker.from_env()
        image = client.images.get(self.image)
        values['image_id'] = image.short_id.split(':')[1]
        values['image_size'] = image.attrs['Size'] / (1024 * 1024)


class DeployfishDeployMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        self.service = None
        if 'service' in kwargs:
            self.service = kwargs['service']
            del kwargs['service']
        super().__init__()

    def annotate(self, values: Dict[str, str]):
        super().annotate(values)
        values['service'] = self.service


class DeployfishTasksDeployMixin(AnnotationMixin):

    def __init__(self, *args, **kwargs):
        self.tasks = None
        if 'tasks' in kwargs:
            self.tasks = kwargs['tasks']
            del kwargs['tasks']
        super().__init__()

    def annotate(self, values: Dict[str, str]):
        super().annotate(values)
        values['tasks'] = self.tasks
