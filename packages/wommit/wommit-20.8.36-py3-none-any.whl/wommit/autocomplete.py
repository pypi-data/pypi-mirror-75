import re
import time
from typing import Iterable

import emojis
from prompt_toolkit import HTML
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.styles import Style

from wommit.utils.exceptions import NoRepoAccessError
from wommit.apihandler import ApiHandler
from wommit.utils.utils import load_data, get_format_string

from prompt_toolkit.completion import Completer, Completion, CompleteEvent
import concurrent.futures
from wommit.msgtool import MsgTool
import logging

class WommitCompleter(Completer):
    # #
    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = load_data()
        self.regtool = MsgTool(self.data)

        logging.basicConfig(filename='myapp.log', level=logging.INFO)

        self.handler = ApiHandler()
        self.issuecomp = IssueCompleter(self.handler)
        self.commitcomp = CommitCompleter(self.handler)

    def form_meta(self, data):
        pass

    def get_completions(self, document, complete_event):

        before = document.text_before_cursor
        word = document.get_word_before_cursor()
        charman = document.char_before_cursor

        # Give all types at start
        # if document.line_count == 1:
        if document.cursor_position_row == 0:

            typematch = re.match("(\w+)$", before)
            scopereg = "^([\u263a-\U0001f645]+)\({1}[a-z,]*"
            scopematch = re.match(scopereg+"$", before)
            endscopematch = re.match(f"{scopereg}\)$", before)
            # scopematch = re.match("^([\u263a-\U0001f645]+)\({1}[a-z,]*$", before)

            # THESE HAVE TO BE IN REVERSE PRIORITY ORDER


            # # Scope end
            # if re.match(self.type_reg + self.scope_start_reg + self.scope_end_reg + "$", document.text_before_cursor):
            if endscopematch:
                yield Completion(") ", start_position=-1)

            # Scopes
            elif scopematch:
                for scope in self.data["scopes"]:
                    if charman == "(":  # Special case at start, yield all
                        start_position = 0
                    elif scope not in before:
                        if charman == ",":
                            start_position = 0
                        elif scope.startswith(word):
                            start_position = -len(word)
                        else:
                            continue
                    else:
                        continue

                    yield Completion(
                        text=scope, display=scope, start_position=start_position
                    )

            #Types
            elif typematch or document.cursor_position == 0:
                for type in self.data["types"]:
                    val = type["value"]
                    if val.startswith(word):
                        if val in self.data['emoji_map']:
                            x = self.data['emoji_map'][val]
                            val_emoji = emojis.encode(x)
                            yield Completion(text=val_emoji, display_meta=val, start_position=-len(word))
                            # yield Completion(text=val, display_meta=val_emoji, start_position=-len(word))


        # Closing
        else:


            comps = list(self.issuecomp.get_completions(document, complete_event))
            commit_comps = list(self.commitcomp.get_completions(document, complete_event))

            if comps:
                yield from comps

            elif commit_comps:
                yield from commit_comps


            elif (word.lower()).startswith("clo"):
                yield Completion(
                    text="Closes ", display="Closes", start_position=-len(word)
                )

            # elif (word.lower()).startswith("bre") and before=="":
            elif document.current_line_before_cursor.lower() == "bre":
                yield Completion("BREAKING CHANGE: ", start_position=-len(word))



class CommitCompleter(Completer):

    def __init__(self, handler: ApiHandler):
        self.commits = handler.get_commits()

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:

        # before = document.text_before_cursor.lower()
        currline = document.current_line_before_cursor
        word = document.get_word_before_cursor().lower()
        charman = document.char_before_cursor

        for commit in self.commits:
            prog = re.compile(r"\(([a-zA-Z0-9]*)\)?", re.MULTILINE)
            regcheck = prog.finditer(currline)
            # titlecheck = commit.title.startswith(word)


            if regcheck:
                for match in regcheck:
                    if ')' not in match.group(0):

                        logging.info(f"content: {match.start()}, {match.end()} " +str(match.group(0)))
                        shacheck = str(commit.sha).startswith(word)
                        if charman == '(' or shacheck:
                            # start_position = 0 if charcheck else -len(word)
                            start_position = -len(word) if charman == '(' else -len(word)-1
                            completion = Completion(
                                text='('+commit.sha+')',display=commit.sha, display_meta=commit.title, start_position=start_position)

                            yield completion



class IssueCompleter(Completer):

    def __init__(self, handler: ApiHandler):
        self.issues = []
        self.future = concurrent.futures.ThreadPoolExecutor().submit(handler.get_issues)
        self.done = False


    def get_completions(self, document, complete_event):

        before = document.text_before_cursor.lower()
        word = document.get_word_before_cursor().lower()

        wordmatch = re.match(r'[\s\S]*#([a-z]+$)', before)
        digmatch = re.match(r'[\s\S]*#([\d]*$)', before)
        if digmatch or wordmatch:
            logging.info(f"digmatch: {bool(digmatch)}!r")
            logging.info(f"wordmatch: {bool(wordmatch)}!r")
            # If thread is not complete
            if not self.done:
                self.fetch_issues()

            # If there are issues to go through
            if self.issues:
                    # There  is a # or a reg match
                for type, nr, title in self.issues:



                    if wordmatch:
                        firval = wordmatch.group(1).lower()
                        start_position = -len(word) - 1
                    else:
                        firval = digmatch.group(1)
                        start_position = -len(word)

                    # if letters typed
                    logging.info(f"title: {title}")
                    logging.info(f"firval word: {firval}")
                    ret_word_b = wordmatch and (title.lower().startswith(firval))
                    ret_dig_b = digmatch and (not firval or str(nr).startswith(firval))

                    if ret_word_b or ret_dig_b:

                        # Styling
                        if type == "PR":
                            style = "fg: #f7f719"
                            selected_style = "bg:#f7f719 fg:ansiblack"
                            info_bg = "#f7f719"


                        else:
                            style = "fg:#0ee6e6"
                            selected_style = "bg:#0ee6e6 fg:ansiwhite"
                            info_bg = "#0ee6e6"

                        info_html = HTML(f"<ttt fg='ansiwhite' bg='#3b8a40'>{title} </ttt><aaa bg='{info_bg}'>{type}</aaa> ")

                        completion = Completion(
                            nr, display_meta=to_formatted_text(info_html), start_position=start_position, style=style,
                            selected_style=selected_style)

                        yield completion
            else:
                return False

    def fetch_issues(self):
        if self.future.done():
            try:
                self.issues = self.future.result()
            except NoRepoAccessError as e:
                logging.info("Could not fetch issues.")
                logging.info(e.message)

            self.done = True

def get_prompt_info():
    text = f"""
<one>Write your commit.</one> <two>Required format</two>:
<format bg='lightgray'>{get_format_string(as_html=True)}</format>

<end>Press Tab to request completion. \nPress Esc+Enter to finish, or Ctrl+C to abort.</end>

> """

    style = Style.from_dict(
        {
            "one": "#57D900",
            "two": "#ff0066 underline",
            "format": "black",
            "end": "ansicyan",
        }
    )

    # message = [('class.one':'Write your commit.'),'']
    return text, style
