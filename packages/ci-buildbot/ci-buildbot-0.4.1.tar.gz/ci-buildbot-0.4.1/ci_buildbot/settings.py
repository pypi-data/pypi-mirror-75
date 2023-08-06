from pathlib import Path  # python3 only
#from typing import Union, List, Dict

from jinja2 import FileSystemLoader, Environment
from pydantic import BaseSettings


templates_path = Path(__file__).parent / 'templates'
jinja_env = Environment(
    loader=FileSystemLoader(str(templates_path))
)


class Settings(BaseSettings):
    """
    See https://pydantic-docs.helpmanual.io/#settings for details on using and overriding this.
    """
    api_token: str = None

    debug: bool = False

    channel: str = "jenkins"

    statsd_host: str = 'scope.cloud.caltech.edu'
    statsd_port: int = 8125
    statsd_prefix: str = 'ci-buildbot.test'

    class Config:
        env_file = '.env'
        fields = {
            'api_token': {'env': 'SLACK_API_TOKEN'},
            'debug': {'env': 'DEBUG'},
            'channel': {'env': 'CHANNEL'},
        }
