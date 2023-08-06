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

from .settings import jinja_env


class PythonMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def python(self, values: Dict[str, str]):
        """
        Extract some stuff from setup.py, if present.

        If setup.py is present, we'll add the following keys to `values`:

        * `name`: the output of `python setup.py name`
        * `version`: the output of `python setup.py version`

        """
        setup_py = pathlib.Path.cwd() / 'setup.py'
        if setup_py.exists():
            # Extract some stuff from python itself
            python_setup = run_setup(str(setup_py))
            values['name'] = python_setup.get_name()
            values['version'] = python_setup.get_version()


class GitMixin:

    def __init__(self, *args, **kwargs):
        self.__get_repo()
        self.__build_url_patterns()
        super().__init__(*args, **kwargs)

    def __get_repo(self):
        self.repo = Repo('.')

    def __build_url_patterns(self):
        # https://caltech-imss-ads@bitbucket.org/caltech-imss-ads/exeter_api/src/0.10.2/
        #
        p = parse(self.repo.remote().url)
        origin_url = f"https://{p.host}/{p.owner}/{p.repo}"
        if origin_url.endswith('.git'):
            origin_url = origin_url[:-4]
        self.url_patterns = {}
        if p.bitbucket:
            self.url_patterns['commit'] = f"<{origin_url}/commits/" + "{sha}|{sha}>"
            self.url_patterns['project'] = f"<{origin_url}/src/" + "{version}/|{name}>"
            self.url_patterns['diff'] = f"{origin_url}/branches/compare/" + "{from_sha}..{to_sha}#diff"
        elif p.github:
            self.url_patterns['commit'] = f"<{origin_url}/commit/" + "{sha}|{sha}>"
            self.url_patterns['project'] = f"<{origin_url}/tree/" + "{version}|{name}>"
            self.url_patterns['diff'] = f"{origin_url}/compare/" + "{from_sha}..{to_sha}"
        else:
            self.url_patterns['commit'] = "{sha}"
            self.url_patterns['project'] = "{name}"
            self.url_patterns['diff'] = None
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

    def git(self, values: Dict[str, str]):
        """
        Extract info about the git repo.  Assume we're in the checked out clone.
        """
        headcommit = self.repo.head.commit
        values['committer'] = str(headcommit.author)
        values['sha'] = headcommit.hexsha
        values['branch'] = self.repo.head.reference.name
        self.__get_last_version(values)
        # Add the diff URL
        if 'diff' in self.url_patterns:
            values['diff_url'] = self.url_patterns['diff'].format(
                from_sha=values['sha'][0:7],
                to_sha=values['last_version_sha'][0:7],
            )


class CodebuildMixin:

    def __init__(self, *args, **kwargs):
        if 'log_group' in kwargs:
            self.log_group = kwargs['log_group']
        super().__init__(*args, **kwargs)

    def aws(self, values: Dict[str, str]):
        values['status'] = 'Success' if 'CODEBUILD_BUILD_SUCCEEDING' in os.environ else 'Failed'
        values['region'] = os.environ['AWS_DEFAULT_REGION']
        values['build_id'] = os.environ.get('CODEBUILD_BUILD_ID', None)
        build_seconds = time.time() - float(os.environ['CODEBUILD_START_TIME'])
        build_minutes = int(build_seconds // 60)
        build_seconds = int(build_seconds - build_minutes * 60)
        values['build_time'] = f"{build_minutes}m {build_seconds}s"
        values['build_status_url'] = f"<https://{values['region']}.console.aws.amazon.com/codebuild/home/?region={values['region']}/builds/{values['build_id']}|Click here>"


class PushAndArchiveMessage(PythonMixin, GitMixin):
    """
    Generate a json string suitable for sending to slack that annotates an
    the initial git push and archive to S3 step:

        * Application info (name, version)
        * Git info (branch, commit, changelog, authors)
    """

    def __init__(self, *args, **kwargs):
        if 'filename' in kwargs:
            self.filename = kwargs['filename']
        else:
            self.filename = None
        super().__init__(*args, **kwargs)

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

    def format(self):
        """
        Generate the full JSON string to send to slack.
        """
        values = {}
        self.python(values)
        self.git(values)
        self.git_changelog(values)
        now = datetime.datetime.now(timezone('UTC'))
        now_pacific = now.astimezone(timezone('US/Pacific'))
        values['completed_date'] = now_pacific.strftime('%Y-%m-%d %H:%M %Z')
        template = jinja_env.get_template('archive.tpl')
        return(json.loads(template.render(**values)))


class DockerBuildMessage(PythonMixin, GitMixin, CodebuildMixin):
    """
    Generate a json string suitable for sending to slack that annotates an
    the Docker build and pus to ECR step:

        * Application info (name, version)
        * Git info (commit, author)
        * Docker info

    """

    def __init__(self, image, *args, **kwargs):
        self.image = image
        super().__init__(*args, **kwargs)

    def docker(self, values: Dict[str, str]):
        client = docker.from_env()
        image = client.images.get(self.image)
        values['image_id'] = image.short_id.split(':')[1]
        values['image_size'] = image.attrs['Size'] / (1024 * 1024)

    def format(self):
        """
        Generate the full JSON string to send to slack.
        """
        values = {}
        self.python(values)
        self.git(values)
        self.docker(values)
        self.aws(values)
        now = datetime.datetime.now(timezone('UTC'))
        now_pacific = now.astimezone(timezone('US/Pacific'))
        values['completed_date'] = now_pacific.strftime('%Y-%m-%d %H:%M %Z')
        template = jinja_env.get_template('docker.tpl')
        print(values)
        return(json.loads(template.render(**values)))

