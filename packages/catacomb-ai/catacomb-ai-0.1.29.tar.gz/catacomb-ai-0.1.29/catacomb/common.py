import docker
import click
import os
import yaml

DEBUG = False
CATACOMB_URL = 'http://localhost:8000' if DEBUG else 'https://beta.catacomb.ai'

def common_config():
    config = get_config()
    try:
        config["docker_client"] = docker.from_env()
    except:
        click.echo("Something went wrong! Ensure you have Docker installed and logged in locally.")
        os.exit(1)

    return config

def get_config():
    config = {}
    if not os.path.exists(".catacomb"):
        open(".catacomb", "a").close()
    else:
        with open(".catacomb", "r") as stream:
            found_config = yaml.safe_load(stream)
            if found_config != None:
                config = found_config

    saved_config = config.copy()

    if "docker_username" not in config:
        if "DOCKER_USERNAME" in os.environ:
            config["docker_username"] = os.environ["DOCKER_USERNAME"]
        else:
            config["docker_username"] = click.prompt("🤖 Docker hub username", type=str)

    if "system_name" not in config:
        if "CATACOMB_SYSTEM_NAME" in os.environ:
            config["system_name"] = os.environ["CATACOMB_SYSTEM_NAME"]
        else:
            config["system_name"] = click.prompt("🤖 System name", type=str)
    
    if "description" not in config:
        if "CATACOMB_SYSTEM_DESCRIPTION" in os.environ:
            config["description"] = os.environ["CATACOMB_SYSTEM_DESCRIPTION"]
        else:
            config["description"] = click.prompt("🤖 System description (markdown supported)", type=str)

    if "description" not in config:
        if "CATACOMB_SYSTEM_DESCRIPTION" in os.environ:
            config["description"] = os.environ["CATACOMB_SYSTEM_DESCRIPTION"]
        else:
            config["description"] = click.prompt("🤖 System description (markdown supported)", type=str)

    # TODO: add error checking that input_type is supported
    if "input_type" not in config:
        if "CATACOMB_SYSTEM_INPUT_TYPE" in os.environ:
            config["input_type"] = os.environ["CATACOMB_SYSTEM_INPUT_TYPE"]
        else:
            config["input_type"] = click.prompt("🤖 Input type (TEXT, JSON, or FILE)", type=str)

    if "examples_location" not in config:
        if "CATACOMB_EXAMPLES_LOCATION" in os.environ:
            config["examples_location"] = os.environ["CATACOMB_EXAMPLES_LOCATION"]
        else:
            config["examples_location"] = click.prompt("🤖 Examples file location (enter to skip)", show_default=False, default='')

    if saved_config != config:
        with open(".catacomb", "w") as config_file:
            config_file.write(yaml.safe_dump(config))

    return config