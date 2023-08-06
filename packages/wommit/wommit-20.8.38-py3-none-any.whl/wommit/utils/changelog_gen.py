import re
import subprocess
from collections import namedtuple
from enum import Enum, Flag, auto

import requests
from emojis import emojis

from wommit.apihandler import ApiHandler
from wommit.configman import Configurator
from wommit.utils import utils
from wommit.msgtool import MsgTool, RegVal
from wommit.utils.utils import get_repo_info
from prompt_toolkit.shortcuts import ProgressBar

CommitAppend = namedtuple("CommitAppend", ["type", "message"])

class LogVersion(Flag):
    BASIC = auto()
    RELEASE = auto()

class ChangelogGenerator:

    def __init__(self, logver:LogVersion=LogVersion.BASIC):
        self.api_url = "https://api.github.com/graphql"
        self.token = ApiHandler().get_token()
        self.data = Configurator().load_data()
        self.data = utils.load_data()
        self.dont_include = ['Merge', 'bump', 'Update']
        self.logver = logver

    def _r_func(self, query, variables, token):
        return requests.post(
            self.api_url,
            json={"query": query, "variables": variables},
            headers={"Authorization": "token {}".format(token)},
        )

    def generate_changelog(self, pre_release=True):
        commits = self._commits_since_release(pre_release)
        typedict = self._gen_type_list()
        typedict['others'] = []
        # print(commits)
        map = self.data['emoji_map']
        inv_map = {v: k for k, v in map.items()}

        dont_include_joined = "|".join(self.dont_include)

        msgtool = MsgTool(self.data)

        # if sys.stdout.isatty():
        # with ProgressBar() as pb:

        for commit in commits:
            msgc = msgtool.check_message(commit)
            good_commits = []

            if msgc:

                # Change these three to enums at some point.
                breaking, typeman, subject = msgtool.get_reg_vals(msgc,
                                                                  [RegVal.breaking, RegVal.type, RegVal.subject])

                for group in [breaking, typeman]:
                    if group:
                        emoji_text = emojis.decode(group)
                        if emoji_text in inv_map:
                            emoji_val = inv_map[emoji_text]
                            good_commits.append(
                                CommitAppend(emoji_val, subject))  # Adds a new commit message under type list.
                        else:
                            print("NON EMOJI VAL SPOTED")
                            good_commits.append(CommitAppend('others', commit))
            else:
                good_commits.append(CommitAppend('others', commit))

            for val in good_commits:
                if not re.match(f'^({dont_include_joined})', val.message):
                    typedict[val.type].append(val.message)

        # print(typedict)
        changelog = self._changelog_formatter(typedict)
        return changelog

    def _changelog_formatter(self, values):
        retstring = ""
        for typeman, commits in values.items():
            if commits:
                commits = filter(lambda x: bool(x), commits)
                try:
                    emoji =  emojis.encode(self.data['emoji_map'][typeman])
                except KeyError:
                    emoji = emojis.encode(":japanese_goblin:")
                typeman = (typeman + "s" if not typeman[-1] == "s" else typeman).lower()
                seperator = "\n\n - "
                commits_ordered = " - " + seperator.join(commits)
                # commits_ordered = f" - {seperator.join(commits)}"
                if self.logver == LogVersion.BASIC:
                    retstring += f"{emoji} {typeman}:\n\n{commits_ordered}\n\n"
                elif self.logver == LogVersion.RELEASE:
                    retstring += f"<details open>\n<summary>{emoji} {typeman}</summary>\n\n{commits_ordered}\n\n</details><br>\n<br>\n"
                else:
                    print("Unsupported log version")
                    return

        return retstring

    def _gen_type_list(self):
        # types = [a['value'] for a in self.data['types']]
        types = [a for a in self.data['emoji_map'].keys()]
        return {x: [] for x in types}

    def _commits_since_release(self, pre_release:bool):

        data = ApiHandler().get_releases(5)

        try:
            if pre_release:
                last_tag = data[0]['node']['tagName']
                args = f'git log {last_tag}..HEAD --oneline'.split(' ')
            else:
                last_tag = data[0]['node']['tagName']
                earlier_tag = data[1]['node']['tagName']
                args = f'git log {earlier_tag}..{last_tag} --oneline'.split(' ')
        except (IndexError, KeyError) as err: # If there are no earlier releases, get all commits.
            args = f'git log --oneline'.split(' ')

        args.append('--pretty=format:%s (%h)')
        #try:
        moreargs = {'text': True, 'check': True, 'capture_output': True, 'encoding': 'utf-8'}
        call = subprocess.run(args, **moreargs)
        out = call.stdout
        #except subprocess.CalledProcessError as err:
            #print(err.stderr)
            #out =err.stderr

        retlist = (out).split('\n')
        return retlist






if __name__ == '__main__':
    ChangelogGenerator().generate_changelog()