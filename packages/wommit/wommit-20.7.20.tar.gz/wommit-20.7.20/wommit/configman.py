import os
import re

import emojis
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter

from wommit.utils import utils
import questionary
import pathlib

class Configurator:
    # Should never edit global config unless global_conf is True.
    def __init__(self, testing: bool=False, global_conf: bool=False):

        self.testing = testing
        self.global_conf = global_conf

        if (global_conf and not os.getenv('SHAPEIT_CONF')):
            os.environ['SHAPEIT_CONF'] = str(pathlib.Path.home())

        self.data = utils.load_data(self.global_conf)

    def _write_data(self, data):
        utils.write_data(data, self.global_conf)

    def load_data(self):
        return self.data
      
    def _write_data(self, data):
        utils.write_data(data, self.global_conf)

    def settings(self):
        questions = [
            {
                "type": "select",
                "name": "option",
                "message": "What setting do you wish to edit?",
                "choices": ["default commit method", "use global config"],
            },
            # Add part
            {
                "when": lambda x: x["option"] == "default commit method",
                "type": "select",
                "name": "which_method",
                "message": "Which method should be the default?",
                "choices": ["menu", "autocomplete"],
            },

            {
                "when": lambda x: x["option"] == "use global config",
                "type": "select",
                "name": "use_global",
                "message": "Use global config by default?",
                "choices": ['Yes', 'No'],

            },

        ]

        s = questionary.prompt(questions)

        if "which_method" in s:
            method = s['which_method']
            self.data.update({'settings':{'method':method}})
            self._write_data(self.data)

        elif "use_global" in s:
            answer = s['use_global']
            boolval = True if answer == 'Yes' else False
            data = dict(self.data, **{'use_global':boolval})
            self._write_data(data)
            print("Local settings now used!")

    # def _get_global_setting(self):


    def print_info(self):
        type_lines = [dicty["value"] for dicty in self.data["types"]]
        formatted_types = "\n".join(type_lines)
        formatted_scopes = "\n".join(self.data["scopes"])

        if utils.is_global_setting():
            state = "GLOBAL"
        else:
            state = "LOCAL"
        print_formatted_text(HTML(f"<sss>{state}</sss>\n<aaa bg='ansiwhite' fg='ansiblack'>Types:</aaa>\n{formatted_types}\n\n"
                                  f"<aaa bg='ansiwhite' fg='ansiblack'>Scopes:</aaa>\n{formatted_scopes}"))

    def edit(self):
        questions = [
            {
                "type": "select",
                "name": "option",
                "message": "What do you wish to do?",
                "choices": ["delete", "add"],
            },
            # Add part
            {
                "when": lambda x: x["option"] == "add",
                "type": "select",
                "name": "which",
                "message": "What do you wish to add?",
                "choices": ["type", "scope"],
            },
            {
                # "when": lambda x: x["which"] == "scope",
                "when": lambda x: "scope" in x.values(),
                "type": "text",
                "name": "addedscope",
                "message": "Type in the name of the scope: ",
                "filter": lambda y: re.sub(
                    r"\W+", "", y
                ),  # Removes all non alphanumeric characters.
            },
            {
                "when": lambda x: "type" in x.values(),
                "type": "text",
                "name": "addedtype",
                "message": "Type in the name of the type: ",
                "filter": lambda y: re.sub(
                    r"\W+", "", y
                ),  # Removes all non alphanumeric characters.
            },
            {
                "when": lambda x: "addedtype" in x,
                "type": "text",
                "name": "type_info",
                "message": "Explain your type:",
            },

            # {
            #     "when": lambda x: "addedtype" in x,
            #     "type": "autocomplete",
            #     "name": "type_emoji",
            #     "message": "Get an emoji for your type:",
            #     "completer": FuzzyCompleter(self.EmojiCompleter),
            #     "choices": ["test"],
            # },

            {
                "when": lambda x: "addedtype" in x,
                "type": "autocomplete",
                "name": "type_emoji",
                "message": "Get an emoji for your type:",
                # "completer": FuzzyCompleter,
                "completer": self.EmojiCompleter(),
                # "choices": [name for emoji in emojis.emojis.db.db.EMOJI_DB for name in emoji.aliases],
                "choices": ["asd"],
                # "choices": [emoji.alises for emoji in emojis.emojis.db.db.EMOJI_DB for emoji in emoji],
            },

            # Delete part
            {
                "type": "checkbox",
                "when": lambda x: x["option"] == "delete",
                "name": "delvals",
                "message": "Which options do you want to remove?",
                "choices": self._format_q(),
            },
        ]

        s = questionary.prompt(questions)
        if "delete" in s.values():
            vals_deleted = self._del_values(s["delvals"])
            print("Deleted: ")
            print(", ".join(vals_deleted))
        # elif s['option'] == 'add':
        else:
            if "addedscope" in s:
                addvar = s["addedscope"]
                self.data["scopes"].append(addvar)

            elif "addedtype" in s:
                # Add type
                addvar = s["addedtype"]
                addtypeinfo = s["type_info"]
                dicadd = {"value": addvar, "name": f"{addvar}: {addtypeinfo}"}
                self.data["types"].append(dicadd)

                # Add emoji for type
                addemoji = s["type_emoji"]
                self.data["emoji_map"][addvar] = addemoji

            if self.testing:
                print("Test finished, won't add to data.")
            else:
                self._write_data(self.data)
                which = s["which"]
                print(f"Added '{addvar}' as an available {which}.")

    def _format_q(self):

        listman = list()
        listman.append(questionary.Separator("Types:"))
        types = [a["value"] for a in self.data["types"]]
        type_dict_list = [{"name": a, "value": "types-" + a} for a in types]
        listman.extend(type_dict_list)

        listman.append(questionary.Separator("Scopes:"))
        scopes = self.data["scopes"]
        scope_dict_list = [{"name": a, "value": "scopes-" + a} for a in scopes]
        listman.extend(scope_dict_list)

        # print(listman)

        return listman

    def _del_values(self, delvalues) -> list:
        """
        Delete values from data file.
        :param delvalues: values to be deleted
        :return: deleted all files that got deleted
        """
        # print(delvalues)
        actualdelvals = list()
        for delval in delvalues:
            splitboy = delval.split("-")
            category, value = splitboy[0], splitboy[1]
            if category == "types":
                # delete list dict element
                self.data[category][:] = [
                    d for d in self.data[category] if d.get("value") != value
                ]

            else:
                self.data[category] = [d for d in self.data[category] if d != value]

            actualdelvals.append(value)

        if not self.testing:
            self._write_data(self.data)
        else:
            print("Test completed, won't save changes.")
        return actualdelvals

    def overwrite_with_global(self):
        """Overrides local data with global data."""
        newconf = Configurator(global_conf=True)
        globaldata = newconf.load_data()
        self._write_data(globaldata)
        return globaldata


    class EmojiCompleter(Completer):

        def __init__(self):
            self.all_emojis = emojis.emojis.db.db.EMOJI_DB

        def get_completions(self, document, complete_event):
            word = document.get_word_before_cursor()

            for emo in self.all_emojis:
                for alias in emo.aliases:
                    if str(alias).startswith(word):
                        yield Completion(text=emo.emoji,display_meta=alias, start_position=-len(word))
