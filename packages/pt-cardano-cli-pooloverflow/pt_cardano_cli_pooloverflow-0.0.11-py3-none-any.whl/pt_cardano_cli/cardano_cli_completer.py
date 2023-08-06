#!/usr/bin/env python

import re

from typing import List, Optional, Dict, Iterable

from prompt_toolkit.document import Document
from prompt_toolkit.completion import (
    Completer,
    Completion,
    WordCompleter,
    FuzzyCompleter
)


class CardanoCliCompleter(Completer):
    def __init__(
        self,
        cli_dict: Dict,
        meta_dict: Optional[Dict[str, str]] = None,
        WORD: bool = False,
    ) -> None:

        self.cli_dict = cli_dict
        self.meta_dict = meta_dict or {}
        self.WORD = WORD
        self.pattern = "^[a-zA-Z0-9-_ ]*"

        self.word_completer = WordCompleter(
            words=self.cli_dict.keys(),
            WORD=self.WORD,
            meta_dict=self.meta_dict,
        )

        self.fuzzy_completer = FuzzyCompleter(
            self.word_completer,
            WORD=self.WORD,
            pattern=self.pattern
        )

    def get_typing_words_arr(
        self, document: Document
    ) -> List[str]:

        typing_line = document.text
        if document.on_first_line:
            typing_line = document.current_line_before_cursor

        typing_words_arr = re.split(r'\s+', typing_line)
        return typing_words_arr

    def get_matching_line(
        self, document: Document
    ) -> str:
        typing_words_arr = self.get_typing_words_arr(document)
        for cl in self.cli_dict.keys():
            cli_words_arr = re.split(r'\s+', cl)
            if len(typing_words_arr) >= len(cli_words_arr):
                prefix_match = all(
                    typing_words_arr[idx] == word
                    for idx, word in enumerate(cli_words_arr)
                )
                if prefix_match:
                    return ' '.join(typing_words_arr[:len(cli_words_arr)])
        return None

    def get_para_completion(
        self, document: Document, matching_line: str
    ) -> Iterable[Completion]:

        if matching_line:
            typing_words_arr = self.get_typing_words_arr(document)
            last_para_word = typing_words_arr[-1]
            for p in list(self.cli_dict[matching_line]):
                yield Completion(
                    p,
                    start_position=-len(last_para_word)
                )

    def get_completions(
        self, document: Document, complete_event
    ) -> Iterable[Completion]:

        matching_line = self.get_matching_line(document)

        if matching_line:
            return self.get_para_completion(document, matching_line)
        return self.fuzzy_completer.get_completions(document, complete_event)
