# General utility functions
import json
import os

import emojis
import re
import pathlib
import html
from subprocess import run, CalledProcessError

from wommit.utils.exceptions import NoGitRepo

pack_dir_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
infopath = pack_dir_path.joinpath('template_info.json')
default_global = pathlib.Path.home().joinpath('SHAPEIT_CONF.json')
global_infopath =os.getenv('SHAPEIT_CONF', default_global)

cwd = pathlib.Path(os.getcwd())

def has_staged_files() -> bool:
    call = run(["git", "diff", "--staged", "--quiet"], capture_output=True)
    code = call.returncode

    if code == 1:
        return True
    elif code == 0:
        return False
    elif code == 129:
        raise NoGitRepo
    else:
        # Raise exception
        call.check_returncode()


def get_repo_info() -> (str, str):
    """Returns a dict with owner and name of local repo in key-value pairs."""
    gitargs = ["git", "config", "--get", "remote.origin.url"]
    repo_url = run(gitargs, check=True, capture_output=True, text=True, encoding="utf-8").stdout
    if not repo_url:
        print("Repo does not yet have a remote")
        return

    splitted = repo_url.split("/")
    x = list(map(lambda s: re.sub(r'(\.git|\n)$', '', s), splitted))
    return {'owner': x[3], 'name': x[4]}


def add_emoji_maps():
    data = load_data()
    listman = [i['value'] for i in data['types']]
    emoji_dict = {val: '' for val in listman}
    data['emoji_map'] = emoji_dict
    write_data(data)

def is_global_setting():
    with open(infopath, "r") as f:
        content = json.load(f)
    return content["use_global"]

def load_data(g=False):

    if g:
        with open(global_infopath, "r") as f:
            content = json.load(f)
    else:

        with open(infopath, "r") as f:
            content = json.load(f)

        if is_global_setting() or g:
            if global_infopath.is_file():
                with open(global_infopath, "r") as f:
                    content = json.load(f)
            else:
                write_data(content, g)

    return content

def write_data(data : dict, g=False):
    if g:
        path = global_infopath
    else:
        path = infopath
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def emojize_types(data, name='name'):
    ret_data = dict(data)
    for typedict in ret_data['types']:
        currval = typedict['value']
        try:
            relemoji = emojis.encode(data['emoji_map'][currval])
            typedict[name] = "{} {}".format(relemoji, typedict[name])
        except KeyError as e:
            print(e)
            continue

    return ret_data

def get_subprocess_runargs():
    return {'text': True, 'check': True, 'capture_output': True, 'encoding': 'utf-8'}


# def check_message(message: str, types: list=[]) -> bool:
#     """
#     Checks if the commit message conforms to
#     the conventional commit standard.
#     :param message: commit message to check
#     :param types: mandatory types for repo. if empty, all types are allowed.
#     :return: True if the message is valid, False otherwise.
#     """
#     if types:
#         typestr = "|".join(types)
#     else:
#         typestr = ".+" # allow anything as type
#         #raise AllowedTypesError
#     reg_s = r"^({typestr})(!?)(\({{1}}[a-z,]+\){{1}})?: ([^ ]+)".format(typestr=typestr) # Double { used to escape.
#     return bool(re.match(reg_s, message))

# def check_message(message: str, types: list=[]) -> bool:
#     """
#     Checks if the commit message conforms to
#     the conventional commit standard.
#     :param message: commit message to check
#     :param types: mandatory types for repo. if empty, all types are allowed.
#     :return: True if the message is valid, False otherwise.
#     """
#     if types:
#         typestr = "|".join(types)
#     else:
#         typestr = ".+" # allow anything as type
#         #raise AllowedTypesError
#     reg_s = r"^({typestr})(!?)(\({{1}}[a-z,]+\){{1}})? ([^ ]+)".format(typestr=typestr) # Double { used to escape.
#     return bool(re.match(reg_s, message))

def convert_type_to_emoji(type:str):
    pass


def get_format_string(as_html=False):
    format = """
&lt;type&gt;[optional scope] &lt;description&gt;
[optional body]
[optional footer]"""
    if as_html:
        return format
    else:
        return str(html.unescape(format))




# Add variant of this. Currently regex is stored in two spots.
#
# def get_regex(as_string=True):
#     type_reg = '^\w+'
#     mid_reg = '\({1}[a-z,]*'
#     scope_reg = '\){1}'
#     end_reg = ':'
#
#     if as_string:
#         return f'{type_reg}{mid_reg}{scope_reg}'
