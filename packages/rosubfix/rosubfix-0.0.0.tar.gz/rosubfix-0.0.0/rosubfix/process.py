import itertools
import re
from pathlib import Path
from typing import Iterable, Tuple

import attr
from cached_property import cached_property


def grouper(n, iterable):
    """
    >>> list(grouper(3, 'ABCDEFG'))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    # https://stackoverflow.com/a/31185097
    iterable = iter(iterable)
    return iter(lambda: list(itertools.islice(iterable, n)), [])


@attr.s
class Rule:
    """Single substitution rule."""

    regex_string: str = attr.ib()
    substitution: str = attr.ib()
    sort_key = attr.ib()

    @classmethod
    def from_dictionary_line(cls, line):
        line = line.strip("\r\n")

        s = remove_diacritics(line.strip(" "))

        if s.islower():
            pat = (
                f"((?:{re.escape(s[0])}|{re.escape(s[0].upper())})"
                f"{re.escape(s[1:])})"
            )
        else:
            pat = f"({re.escape(s)})"

        if line.startswith(" "):
            pat = "\\b" + pat

        if line.endswith(" "):
            pat = pat + "\\b"

        return cls(
            regex_string=pat, substitution=line.strip(" "), sort_key=-len(line)
        )

    def substitute(self, string):
        substitution = self.substitution
        if string[0].isupper():
            substitution = substitution[0].upper() + substitution[1:]
        return substitution


class BaseRuleGroup:
    def finditer(self, string: str) -> Iterable[Tuple[int, int, str, Rule]]:
        raise NotImplementedError()


@attr.s
class RuleGroupSubset(BaseRuleGroup):
    rules = attr.ib()

    @cached_property
    def regex(self):
        # handle case with no rules
        if not self.rules:
            return re.compile("$a")  # this never matches anything

        return re.compile("|".join(rule.regex_string for rule in self.rules))

    def finditer(self, string) -> Iterable[Tuple[int, int, str, Rule]]:
        for m in self.regex.finditer(string):
            index = m.lastindex
            yield m.span(index) + (m.group(index), self.rules[index - 1])


@attr.s
class RuleGroup(BaseRuleGroup):
    rules = attr.ib()

    @cached_property
    def children(self):
        return [
            RuleGroupSubset(rule_sublist)
            for rule_sublist in grouper(30, self.rules)
        ]

    def finditer(self, string):
        for child in self.children:
            yield from child.finditer(string)


RO_DIACRITICS = {
    "ă": "a",
    "Ă": "A",
    "â": "a",
    "Â": "A",
    "ă": "a",
    "î": "i",
    "ș": "s",
    "Ș": "S",
    "ț": "t",
    "Ț": "T",
    "ş": "s",
    "Ş": "S",
    "ţ": "t",
    "Ţ": "T",
}
RO_DIACRITICS_REGEX = re.compile("|".join(RO_DIACRITICS.keys()))


def remove_diacritics(string):
    def substitute(match):
        return RO_DIACRITICS[match.group()]

    return RO_DIACRITICS_REGEX.sub(substitute, string)


class SubFix:
    """Main object that fix up subtitles."""

    def __init__(self, dictionary_file: Path):
        with open(dictionary_file, "rt", encoding="utf-8") as file:
            rules = [Rule.from_dictionary_line(line) for line in file]

        rules.sort(key=lambda rule: rule.sort_key)
        self.rulegroup = RuleGroup(rules=rules)

    def substitute(self, string: str) -> str:
        results = list(self.rulegroup.finditer(string))
        results.sort(key=lambda x: (x[0], x[3].sort_key))

        repl = []
        last_end = 0

        for match_start, match_end, match_string, rule in results:
            if match_start < last_end:
                continue

            repl.append(string[last_end:match_start])
            repl.append(rule.substitute(match_string))

            last_end = match_end

        repl.append(string[last_end:])

        return "".join(repl)
