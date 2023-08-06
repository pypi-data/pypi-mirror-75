"""Grammalecte wrapper."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Generator, List, Union
from zipfile import ZipFile

import requests

# TODO dataclass
class GrammalecteMessage:
    def __init__(self, line: int, start: int, end: int) -> None:
        self.line = line
        self.start = start
        self.end = end

    def __str__(self):
        return f"Ligne {self.line} [{self.start}:{self.end}]"

    def __eq__(self, other: "GrammalecteMessage"):
        # TODO to sort, but misleading equality usage
        return (self.line, self.start, self.end) == (other.line, other.start, other.end)

    def __lt__(self, other: "GrammalecteMessage"):
        return (self.line, self.start, self.end) < (other.line, other.start, other.end)


class GrammalecteSpellingMessage(GrammalecteMessage):
    def __init__(self, line: int, start: int, end: int, word: str) -> None:
        super().__init__(line, start, end)
        self.word = word

    def __str__(self):
        return super().__str__() + f" Mot inconnu : {self.word}"

    @staticmethod
    def from_dict(line: int, grammalecte_dict: dict) -> "GrammalecteSpellingMessage":
        return GrammalecteSpellingMessage(
            line,
            int(grammalecte_dict["nStart"]),
            int(grammalecte_dict["nEnd"]),
            grammalecte_dict["sValue"],
        )


class GrammalecteGrammarMessage(GrammalecteMessage):
    def __init__(
        self,
        line: int,
        start: int,
        end: int,
        url: str,
        color: List[int],
        suggestions: List[str],
        message: str,
        rule: str,
        type: str,
    ) -> None:
        super().__init__(line, start, end)
        self.url = url
        self.color = color
        self.suggestions = suggestions
        self.message = message
        self.rule = rule
        self.type = type

    def __str__(self):
        ret = super().__str__() + f" [{self.rule}] {self.message}"
        if self.suggestions:
            ret += f" (Suggestions : {', '.join(self.suggestions)})"
        return ret

    @staticmethod
    def from_dict(line: int, grammalecte_dict: dict) -> "GrammalecteGrammarMessage":
        return GrammalecteGrammarMessage(
            line,
            int(grammalecte_dict["nStart"]),
            int(grammalecte_dict["nEnd"]),
            grammalecte_dict["URL"],
            grammalecte_dict["aColor"],
            grammalecte_dict["aSuggestions"],
            grammalecte_dict["sMessage"],
            grammalecte_dict["sRuleId"],
            grammalecte_dict["sType"],
        )


def grammalecte_text(text: str) -> Generator[GrammalecteMessage, None, None]:
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = Path(tmpdirname) / "file.txt"
        with open(tmpfile, "w", encoding="utf-8") as f:
            f.write(text)
        yield from grammalecte_file(tmpfile)


def grammalecte_file(
    filename: Union[str, Path]
) -> Generator[GrammalecteMessage, None, None]:
    """Run grammalecte on a file given its path, generate messages."""
    stdout = "[]"
    # TODO check existence of a file
    filename = str(filename)
    try:
        result = _run_grammalecte(filename)
        stdout = result.stdout
    except FileNotFoundError as e:
        if e.filename == "grammalecte-cli.py":
            _install_grammalecte()
            result = _run_grammalecte(filename)
            stdout = result.stdout

    warnings = json.loads(stdout)
    for warning in warnings["data"]:
        lineno = int(warning["iParagraph"])
        messages = []
        for error in warning["lGrammarErrors"]:
            messages.append(GrammalecteGrammarMessage.from_dict(lineno, error))
        for error in warning["lSpellingErrors"]:
            messages.append(GrammalecteSpellingMessage.from_dict(lineno, error))
        for message in sorted(messages):
            yield message


def _run_grammalecte(filename: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "grammalecte-cli.py",
            "-f",
            filename,
            "-off",
            "apos",
            "--json",
            "--only_when_errors",
        ],
        capture_output=True,
        text=True,
    )


def _install_grammalecte():
    """Install grammalecte CLI."""
    version = "1.11.0"
    tmpdirname = tempfile.mkdtemp(prefix="grammalecte_")
    tmpdirname = Path(tmpdirname)
    tmpdirname.mkdir(exist_ok=True)
    download_request = requests.get(
        f"https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v{version}.zip"
    )
    download_request.raise_for_status()
    zip_file = tmpdirname / f"Grammalecte-fr-v{version}.zip"
    zip_file.write_bytes(download_request.content)
    with ZipFile(zip_file, "r") as zip_obj:
        zip_obj.extractall(tmpdirname / f"Grammalecte-fr-v{version}")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            str(tmpdirname / f"Grammalecte-fr-v{version}"),
        ]
    )
