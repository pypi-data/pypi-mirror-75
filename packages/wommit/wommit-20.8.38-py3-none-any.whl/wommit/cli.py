import re

import click
#import questionary
import questionary
from click import ClickException
from click.testing import CliRunner
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from wommit.apihandler import ApiHandler
from wommit.commitman import Questioneer
#import shutil
import subprocess

from wommit.msgtool import MsgTool
from wommit.utils.changelog_gen import ChangelogGenerator, LogVersion
from wommit.utils.exceptions import NoAnswersError, NoStandardsError, RepoException, NoGitRepo
from wommit.utils.utils import get_format_string
import wommit.utils.utils as utils
from wommit.configman import Configurator
from prompt_toolkit import print_formatted_text, HTML
import hashlib


@click.group()
def cli():
    """A package for intuitively commiting files with Git."""
    pass

@cli.command()
@click.option("-id", type=str, help="Check a commit message with the specified ID.")
@click.option("-ids", nargs=2, type=str, default="", help="Check all commit messages between two IDs (newest ID first).")
@click.option("-m", type=str, help="Check if the given string passes the check.")
@click.option("-l", "--latest", is_flag=True, help="Check all local commits that have not been pushed.")
def check(id, ids, m, latest):
    """Checks if previous commit message meets the Conventional Commits format."""

    try:

        # pop = subprocess.Popen(text=True, check=True, capture_output=True, encoding='utf-8')
        runargs = utils.get_subprocess_runargs()
        gitcmd = "git log -1 --pretty=%B".split()
        check_msgs = []

        if id:
            gitcmd.append(id)
            msg = subprocess.run(gitcmd, **runargs).stdout
            check_msgs.append(msg)
        elif m:
            check_msgs.append(m)
        elif latest or ids: # Format this piece of code better.
            if ids:
                hashgets = f"git log {ids[1]}..{ids[0]} --pretty=%H".split(' ')
            else:

                branchname = subprocess.run('git branch --show-current'.split(), **runargs).stdout.strip()
                hashgets = f"git log origin/{branchname}..{branchname} --pretty=%H".split(' ')
            callhashes = subprocess.run(hashgets, **runargs).stdout.strip()
            hashes = [x for x in callhashes.split("\n") if x]
            if not hashes:
                print("No new commits to check.")
                return
            for hash in reversed(hashes):
                msg = subprocess.run(gitcmd + [hash], **runargs).stdout
                check_msgs.append(msg)

        else: # Default check on latest commit
            msg = subprocess.run(gitcmd, **runargs).stdout
            check_msgs.append(msg)

        # Check all git messages.

        text = FormattedText([('', '\n'),('bg:#D924EF' , 'SHAPEIT CHECK'),('','\n')])

        print_formatted_text(text)

        for msg in check_msgs:
            _check_and_print(msg)

    except subprocess.CalledProcessError as e:

        # r = re.find("\bfatal: ambiguous argument '[\s\S]+': unknown revision or path not in the working tree.\b")
        # if "fatal: ambiguous argument 'asd': unknown revision or path not in the working tree" in e.stderr:
        if "fatal: ambiguous argument " in e.stderr:
            print(e.stderr)
            raise click.BadParameter("Found no commits with this hash", param=id, param_hint="-i")

        elif "fatal: not a git repository (or any of the parent directories): .git" in e.stderr:
            raise click.UsageError("This is not a git repository. Make it a git repository with git init")

        else:
            raise e

def _check_and_print(msg):

    tool = MsgTool()

    # msg = tool.check_and_convert(msg)
    cc_msg = tool.check_and_convert(msg)
    if cc_msg:
        passtup = ("ansigreen" , "Your message passes! :)")
    else:
        passtup = ("ansired", "Your message doesn't pass! :(")

    text = FormattedText([

        # ('bg:#D924EF' , 'SHAPEIT CHECK'),
        # ('','\n'),
        # ('#4DF5F7', 'Your commit:\n\n'),
        ('' , msg),
        ('', '\n'),
        passtup,
        ('', '\n\n---\n'),
    ])

    style = Style.from_dict({
        # 'msg':'bg:#A6ACAC fg:#ansiblack',
        'msg': 'fg:#ansiwhite',
    })

    print_formatted_text(text, style=style)

@cli.command()
def format():
    """Prints the Wommit commit format."""
    print("Format:\n" + get_format_string() + "\n")

@cli.group()
@click.option('-t', is_flag=True, help="Test the functionality.")
@click.option('-g', is_flag=True, help="Global config.")
@click.pass_context
def configure(ctx, t, g):
    """Configure available types and scopes."""
    ctx.ensure_object(dict)
    ctx.obj['confman'] = Configurator(t, g)

@configure.command()
@click.pass_context
def e(ctx):
    """Edit current types and scopes."""
    try:
        ctx.obj['confman'].edit()
    except KeyError as e: # Process was cancelled and returned empty values.
        exit()

@configure.command()
@click.pass_context
def p(ctx):
    """Prints all types and scopes."""
    ctx.obj['confman'].print_info()

@configure.command()
@click.pass_context
def s(ctx):
    """Edit settings."""
    try:
        ctx.obj['confman'].settings()
    except KeyError as e: # Process was cancelled and returned empty values.
        exit()

@configure.command()
@click.pass_context
def overwrite(ctx):
    """Overwrites local data with global."""
    val = questionary.confirm("Are you sure").ask()
    if val:
        globaldata = ctx.obj['confman'].overwrite_with_global()
        print("Global data is now local!")

@cli.command()
@click.option('-e', '--expert', is_flag=True, help="Expert mode, autocompletion. Overrides default.")
@click.option('-m', '--menu', is_flag=True, help="Menu mode. Overrides default.")
@click.option('--manual', type=str, help="Custom message input, converts feat names to emojis.")
@click.option('-t', '--test','--dry', is_flag=True, help="Manually test the functionality.")
@click.option('-g', is_flag=True, help="Use global settings.")
def c(expert, menu, manual, test, g):
    """Commit your staged files using an intuitive menu."""
    try:
        if not test and not utils.has_staged_files():
            print("Your repo has no files staged for commiting.")
            return

        conf = Configurator(testing=test, global_conf=g)
        data = conf.load_data()
        q = Questioneer(data=data, show_staged=True)
        default_mode = data['settings']['method']
        if manual:
            message = MsgTool().check_and_convert(manual)

        elif expert:
            message = q.autocomp()
        elif menu:
            message = q.select()
        elif default_mode == "autocomplete":
            message = q.autocomp()
        elif default_mode == 'menu':
            message = q.select()



    except NoAnswersError:# The user interrupted the prompt.
        raise click.Abort
    except NoStandardsError as err: # If the message didn't follow the standards.
        raise click.UsageError("Message did not conform to the commit standards.")
    except (RepoException, NoGitRepo) as err:
        raise click.UsageError("You are not inside a git repo.")

    # Er allerede sjekket. Trenger bare å printe.
    _check_and_print(message)
    # print("Commit message passed.")

    if test:
        print(f"\nTest completed.\n")

    else:

        try: # Attempt to commit
            subprocess.run(['git', 'commit', '-m', message], text=True, check=True)
        except subprocess.CalledProcessError as expert:
            print(expert.stderr)
        else:
            print_formatted_text(HTML("<aaa bg='ansigreen'>Commited!</aaa>"))

@cli.command()
@click.option('-b','--basic',is_flag=True, help="Prints an easily readable changelog.")
@click.option('-r','--release',is_flag=True, help="Prints a changelog designed for Github releases.")
@click.option('-e', '--edit', is_flag=True, help="Edit a release tag with the generated changelog.")
@click.option('-post', '--post_release', is_flag=True, help="Checks between two latest instead of latest to now.")
def changelog(basic, release, edit, post_release):
    """Generates a changelog from all wommit commits."""

    if basic:
        gen = ChangelogGenerator(LogVersion.BASIC)
    elif release:
        gen = ChangelogGenerator(LogVersion.RELEASE)
    else:
        gen = ChangelogGenerator(LogVersion.BASIC)

    changelog = gen.generate_changelog(pre_release=(not post_release))

    if edit:
        print("going in")
        ApiHandler().edit_release(changelog)

    try:
        print(changelog)
    except:
        return changelog