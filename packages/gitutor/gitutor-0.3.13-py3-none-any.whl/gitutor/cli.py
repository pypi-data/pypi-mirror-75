import git
import click

from goBack.commands import goBack
from init.commands import init
from save.commands import save
from ignore.commands import ignore
from compare.commands import compare

@click.group()
@click.pass_context
def cli(ctx):
    """ Git the easy way """
    #Check ctx was initialized
    ctx.ensure_object(dict)

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
