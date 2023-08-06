import git
import click
from git import GitCommandError
from .color_diff import color_diff
from util import commits_full_list, prompt_for_commit_selection

@click.command()
@click.pass_context
@click.option('-c', '--commit', help='Hash of commit to compare')
def compare(ctx,commit):
    '''
    Compare current status with selected commit
    '''
    #Recover repo from context
    repo = ctx.obj['REPO']

    if commit:
        try:
            click.echo(repo.git.diff(commit))
        except GitCommandError:
            click.echo('Hash not found')
        return


    full_list_of_commits = commits_full_list(repo)
    answer = prompt_for_commit_selection(full_list_of_commits, 'Select commit to compare')
    if answer:
        answer_hash = answer['commit'][:7]
        diff_string = repo.git.diff(answer_hash)
        click.echo('\n'.join(color_diff(diff_string.splitlines())))
