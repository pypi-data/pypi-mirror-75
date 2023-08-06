#!/usr/bin/env python

import os
import subprocess
import re
from subprocess import PIPE, STDOUT

from pt_cardano_cli.cardano_cli_prompt import CardanoCliPrompt
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit import print_formatted_text, HTML


def main(cardano_cli):
    ccp = CardanoCliPrompt()
    session = PromptSession()

    while True:
        try:
            command = session.prompt(
                ccp.message,
                completer=ccp.completer,
                complete_while_typing=True,
                complete_style=CompleteStyle.MULTI_COLUMN,
                auto_suggest=AutoSuggestFromHistory(),
                enable_suspend=True,
                rprompt=ccp.get_rprompt,
                bottom_toolbar=ccp.bottom_toolbar,
                multiline=True,
                prompt_continuation=ccp.prompt_continuation,
                complete_in_thread=True,
                style=ccp.style
            )
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            cmd = cardano_cli + ' ' + re.sub(r'\n', ' ', command)
            p = subprocess.Popen(
                cmd,
                shell=True,
                stdout=PIPE,
                stderr=STDOUT
            )
            outs, errs = p.communicate()
            print_formatted_text(
                HTML('<ansiwhite> %s </ansiwhite>' % outs.decode("ascii"))
            )
            if errs:
                print_formatted_text(
                    HTML('<ansired> %s </ansired>' % errs.decode("ascii"))
                )

    print("GoodBye")


if __name__ == "pt_cardano_cli.__main__":
    CARDANO_CLI = os.getenv('CARDANO_CLI_PATH')
    if CARDANO_CLI:
        print("Env CARDANO_CLI_PATH: %s" % CARDANO_CLI)
        cardano_cli = CARDANO_CLI
    else:
        print(
            "Environment Variable CARDANO_CLI_PATH "
            "not found, using default."
        )
        cardano_cli = 'cardano-cli'

    main(cardano_cli)
