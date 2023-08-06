import os
import git
import click
import requests
from datetime import datetime

from goBack.commands import goBack
from init.commands import init
from save.commands import save
from ignore.commands import ignore
from compare.commands import compare



def run_config(command):
    api_endpoint = 'https://firestore.googleapis.com/v1/projects/gitutor/databases/(default)/documents/metrics/'

    path = os.path.dirname(__file__)
    config_file = path + '/.gitutor_config'

    with open(config_file, 'r') as _:
        flag = int(_.read())

    if flag == 1:
        fields = {
            "fields": {
                "command": {"stringValue": command},
                "date": {"timestampValue": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
            }
        }

        response = requests.post(api_endpoint, json = fields)

        with open(config_file, 'w') as _:
            _.write('0')


@click.group()
@click.pass_context
def cli(ctx):
    """ Git the easy way """
    #Check ctx was initialized
    ctx.ensure_object(dict)

    # run_config(ctx.invoked_subcommand)
    
    if ctx.invoked_subcommand != 'init':
        try:
            repo = git.Repo(".", search_parent_directories=True)
            ctx.obj['REPO'] = repo
            #print( f"Location {repo.working_tree_dir}" )
            #print(f"Remote from init: {repo.remote('origin').url} ")
        except Exception as e:
            click.echo(e)
            #print("not git repo")
            exit()

cli.add_command(init)
cli.add_command(goBack)
cli.add_command(save)
cli.add_command(ignore)
cli.add_command(compare)

def main():
    cli(obj={})

if __name__ == '__main__':
    cli(obj={})
