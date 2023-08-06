import os
import base64
import yaml
import requests
import click

CONFIG_PATH = os.path.expanduser('~/') + ".catacombrc"


@click.command()
@click.argument('key')
def authenticate(key):
    config = {}

    if not os.path.exists(CONFIG_PATH):
        open(CONFIG_PATH, "a").close()  
    else:
        with open(CONFIG_PATH, "r") as stream:
            found_config = yaml.safe_load(stream)
            if found_config != None:
                config = found_config
    
    config['key'] = base64.b64encode(key.encode('utf-8'))

    r = requests.get('https://beta.catacomb.ai/api/key/detail/', headers={
        'Authorization': f"Api-Key {key}"
    })

    if 'user' in r.json():
        with open(CONFIG_PATH, "w") as config_file:
            config_file.write(yaml.safe_dump(config))
        click.echo(f"You've successfully authenticated your CLI. Nice to meet you, {r.json()['user']['username']}!")
    else:
        click.echo(f"The provided API key is invalid.")

def get_creds():
    if not os.path.exists(CONFIG_PATH):
        open(CONFIG_PATH, "a").close()  
    else:
        with open(CONFIG_PATH, "r") as stream:
            return yaml.safe_load(stream)