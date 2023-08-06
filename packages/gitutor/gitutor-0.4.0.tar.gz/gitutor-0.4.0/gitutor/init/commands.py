import click
from github import Github
from github import GithubException
from git import GitCommandError
import git
import os


@click.command()
@click.pass_context
@click.option('-u', '--user', 'user_name' )
@click.option('-p', '--password', 'password', hide_input=True)
@click.option('-l', '--local', is_flag=True)
@click.option('-r', '--repo-name')
@click.option('--ssh', is_flag=True)
def init(ctx, user_name, password,local, repo_name, ssh):
    "Create git repo and github remote"
    if is_initialized_repo():
        click.echo('This is already a git repo!')
        return

    if local:
        init_local_repo()
        return
    if not user_name:
        user_name = click.prompt('Username')
    
    if not password:
        password = click.prompt('Password', hide_input=True)

    if not repo_name:
        repo_name = click.prompt('Repo name')
    
    try:
        g = Github(user_name, password)
        user = g.get_user()
        click.echo('Creating github repo...')
        remote_repo = user.create_repo(repo_name)
    except GithubException as e:
        error_code = e.args[0]
        if error_code == 401 :
            click.echo('Problem with credentials!')
        else:
            if error_code == 422 :
                click.echo('Repo name already used!')
    else:
        local_repo = init_local_repo()
        if ssh:
            local_repo.create_remote('origin', remote_repo.ssh_url)
        else:
            local_repo.create_remote('origin', remote_repo.clone_url)
        click.echo('Push to origin...')
        local_repo.git.push('-u', 'origin', 'master')
        click.echo('Ready!')

def init_local_repo():
    repo_dir = os.getcwd()
    file_name = os.path.join(repo_dir, 'README.md')

    repo = git.Repo.init(repo_dir)
    #Create empty README.md
    open(file_name, 'wb').close()
    repo.index.add([file_name])
    repo.index.commit('first commit')
    return repo

def is_initialized_repo():
    try:
        git.Repo('.', search_parent_directories=True)
    except:
        return False
    else:
        return True




