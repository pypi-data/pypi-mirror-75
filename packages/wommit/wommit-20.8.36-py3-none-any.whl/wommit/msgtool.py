import re
from enum import Enum
from typing import Union

import emojis
from prompt_toolkit.document import Document

from wommit.utils.utils import load_data
from prompt_toolkit.validation import Validator, ValidationError


class RegVal(Enum):
    # Which group of the regex contains what part.
    breaking = 1
    type = 2
    exclamation = 3
    scope = 4
    subject = 5

class MsgTool:

    def __init__(self, data=None):
        if not data:
            data = load_data()
        self.types = [a["value"] for a in data["types"]]
        self.emomap = data["emoji_map"]
        matchedemos = [b for (a,b) in self.emomap.items() if a in self.types]
        self.emojis = [emojis.encode(a) for a in matchedemos]



    def check_and_convert(self, input: Union[str, dict]):

        if isinstance(input, dict):
            input = self.msg_dict_to_str(input)

        m = self.check_message(input)
        if m:
            return self._convert_message(input, m)

    def check_message(self, message) -> re.Match:
        """
        Checks if the commit message conforms to
        the conventional commit standard.
        :param message: commit message to check
        :param types: mandatory types for repo. if empty, all types are allowed.
        :return: True if the message is valid, False otherwise.
        """
        # if types:
        #     typestr = "|".join(types)
        if self.types:
            typestr = "|".join(self.types + self.emojis)
        else:
            typestr = ".+" # allow anything as type
        boom = emojis.emojis.db.get_emoji_by_alias("boom").emoji

        ##
        reg_s = r"^({boom})?({typestr})(!?)(\([a-z,]+\))? ([\s\S]+\n?)".format(typestr=typestr, boom=boom) # Double { used to escape.
        ##

        m = re.match(reg_s, message)
        if not m:
            mergematch = re.match(r"^Merge branch [\w] into [\w]", message)
            return mergematch

        return m

    def get_reg_vals(self, match: re.Match, vals:[RegVal]) -> list:
        retlist = []
        for val in vals:
            groupnr = val.value
            retlist.append(match.group(groupnr))

        return retlist


    def _convert_message(self, message, match):

        typeman = match.group(RegVal.type.value)

        if "BREAKING CHANGE:" in message and not match.group(RegVal.exclamation.value):
            boom = emojis.emojis.db.get_emoji_by_alias("boom").emoji
            mslist = message.split('\n')
            mslist[0] =  boom + mslist[0]
            message = "\n".join(mslist)
            # message = re.sub(firval, firval+"!", message)


        has_emoji = bool(emojis.get(typeman))
        has_match = typeman in self.emomap
        if has_emoji:
            pass
        elif has_match:
            emo = emojis.encode(self.emomap[typeman])
            s = r"^\b{}\b".format(typeman)
            message = re.sub(s, emo, message)
        else:
            print("Couldn't convert to emoji.")

        return message


    def get_reg(self, types=False, mid=False, scopes=False):
        pass

    def msg_dict_to_str(self, answers: dict) -> str:
        """Generate the message with the given answers."""

        # if answers["issue_close"]:
        #     answers["issue"] = "Closes {}".format(answers["issue"])
        # else:
        #     answers["issue"] = ""

        if answers["is_breaking_change"]:
            answers["breaking_change"] = "BREAKING CHANGE:"
            answers["prefix"] = answers["prefix"] + "!"

        else:
            answers["breaking_change"] = ""

        # ret = "{prefix}{scope} {subject}\n\n{breaking_change}{body} \n\n{footer}{issue}".format(
        #     **answers
        # )
        ret = "{prefix}{scope} {subject}\n\n{breaking_change}{body}".format(
            **answers
        )
        return ret



class RegValidator(Validator):
    # Ugly and weird validator, not relying on other parts of regex tool.
    # Will polish in the future, works for now.

    def __init__(self):
        self.msgtool = MsgTool()

    def find_error(self, msg):
        typereg = '([\u263a-\U0001f645]+)'
        if not re.match(f"{typereg}", msg):
            return "Insert type first."
        elif re.match(f"{typereg}\([a-z,]*$", msg):
            return "Finish scope part."
        elif re.match(f"{typereg}\([a-z,]*\)$", msg):
            return "Need space between type/scopes and subject."
        elif re.match(f"{typereg}(\([a-z,]*\))* $", msg):
            return "Subject can't be empty."
        elif not self.msgtool.check_message(msg):
            return "Message currently invalid."

    def validate(self, document: Document) -> None:
        errmsg = self.find_error(document.text)
        if errmsg:
            raise ValidationError(message=errmsg)
