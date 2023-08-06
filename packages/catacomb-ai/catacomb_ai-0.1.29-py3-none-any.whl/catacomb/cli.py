import os
import click
import requests
import docker
import urllib.request
import yaml
from .static import DOCKERFILE
from .docker_logic import build, push, run
from .auth import authenticate

@click.group()
def cli():
    pass

cli.add_command(authenticate, name="auth")
cli.add_command(build, name="build")
cli.add_command(push, name="push")
cli.add_command(run, name="run")