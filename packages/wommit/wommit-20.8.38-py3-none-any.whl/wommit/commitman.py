import time

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.application import get_app
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.validation import Validator

from wommit.apihandler import ApiHandler
from wommit.autocomplete import WommitCompleter, get_prompt_info, IssueCompleter
from wommit.utils.exceptions import NoAnswersError, NoStandardsError
from wommit.msgtool import MsgTool
from wommit.utils.utils import load_data, emojize_types
from questionary import prompt

import wommit.msgtool


# def parse_subject(text):
#     if isinstance(text, str):
#         text = text.strip(".").strip()
#
#     return required_validator(text, msg="Subject is required.")


def parse_scope(scopes):
    if not scopes:
        return ""

    f_scope = ",".join(scopes)
    return f"({f_scope})"


class Questioneer:
    def __init__(self, data=None, show_staged:bool = False):
        if not data:
            self.data = load_data()
        else:
            self.data = data

        self.show_staged = show_staged

        self.msgtool = MsgTool(self.data)

    def autocomp(self):
        """Shape commit message using autocompletion."""
        prompttext, style = get_prompt_info(self.show_staged) # Give better name for prompt_stuff. E.g compose_info, compose_prompt
        completer = WommitCompleter(self.data)
        # The creation of the session is what takes the majority of the startup time.
        session = PromptSession(completer=completer)

        text = session.prompt(
            HTML(prompttext),
            style=style,
            complete_while_typing=True,
            multiline=True,
            # pre_run=session.default_buffer.start_completion(),
            # bottom_toolbar=self.bottom_toolbar(session.history.get_strings()),
            # validator=Validator.from_callable(
            #     self.regtool.check_message, error_message="Does not yet meet standards."
            # ),
            validator=wommit.msgtool.RegValidator(),
            key_bindings=self._get_kb(),
            auto_suggest=AutoSuggestFromHistory()
        )
        # return self.do_check(text)
        # return text
        return self.msgtool.check_and_convert(text)

    def select(self):
        """Shape commit message using menus."""
        answers = prompt(self.questions())

        # If the user interruptes
        if not answers:
            raise NoAnswersError

        # message = self.regtool.format_message(answers)

        f = self.msgtool.check_and_convert(answers)
        if not f:
            raise NoStandardsError(
                f"Commit message does not meet standards.\n{f}"
            )

        return f

    def questions(self) -> list:
        """Questions regarding the commit message."""

        repr_data = emojize_types(self.data)

        issuecomp = IssueCompleter(ApiHandler())

        questions = [
            # Parses feature
            {
                "type": "list",
                "name": "prefix",
                "message": "What type of commit is this:",
                "choices": repr_data["types"],  # Gets listed features in info json.
            },
            # Parses scope
            {
                "type": "checkbox",
                "name": "scope",
                "message": ("Scope. Specify place of commit change: \n"),
                "choices": repr_data["scopes"],  # Gets listed scopes in info json.
                "filter": parse_scope,
            },
            # Parses commit description
            {
                "type": "input",
                "name": "subject",
                "message": "The subject of this commit:\n",
                # 'filter': parse_subject,
                "validate": Validator.from_callable(
                    (lambda x: len(x) > 0), error_message="Subject can't be empty."
                ),
            },
            # Body of commit
            {
                "type": "autocomplete",
                "name": "body",
                "completer": issuecomp,
                "choices": ['asd'],
                "message": (
                    "Body. Motivation for the change and contrast this "
                    "with previous behavior:\n"
                ),
            },
            # # Optional later addition of breaking changes.
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            # # Optional footers
            # {
            #     "type": "input",
            #     "name": "footer",
            #     "message": (
            #         "Footer. Information about Breaking Changes and "
            #         "reference issues that this commit closes:\n"
            #     ),
            # },
            # Issue
            # {
            #     "type": "confirm",
            #     "name": "issue_close",
            #     "message": "Does this close an issue?",
            #     "default": False,
            # },
            # {
            # "type": "autocomplete",
            #         "name": "issue",
            # "message": "Which one?",
            # "completer": issuecomp,
            # "choices": ['asd'],
            # "when": lambda x: x["issue_close"],
            # "validate": lambda val: re.compile("#\d").match(val) is not None,
            # # 'filter': parse_issue
            # },
        ]
        return questions

    def _get_kb(self):
        kb = KeyBindings()

        @Condition
        def is_line1():
            return get_app().current_buffer.document.line_count == 1

        @kb.add('c-m', filter=is_line1)
        def _(event):
            " Initialize autocompletion, or select the next completion. "
            buff = event.app.current_buffer
            buff.newline()
            buff.newline()

        @Condition
        def one_comp():
            buff = get_app().current_buffer
            if buff.complete_state:
                comps = buff.complete_state.completions
                return len(comps) == 1 and '(' not in buff.document.text_before_cursor
            else:
                return False

        @kb.add('space', filter=one_comp)
        def _(event):
            " Initialize autocompletion, or select the next completion. "
            buff = event.app.current_buffer
            # comp = buff.go_to_completion(0)
            comp = buff.complete_state.completions[0]
            buff.apply_completion(comp)
            buff.insert_text(" ")
            # word = buff.document.get_word_before_cursor()
            # buff.insert_text((comp.text + " "), overwrite=True, move_cursor=-(len(word)))


        return kb

