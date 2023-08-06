#!/usr/bin/env python

from pt_cardano_cli.cli_lines import cli_cmd_lines
from pt_cardano_cli.cardano_cli_completer import CardanoCliCompleter
from prompt_toolkit.styles import Style


class CardanoCliPrompt():
    def __init__(
        self
    ) -> None:
        self.message = [
            ('class:arrow', '➜ '),
            ('class:cardano-cli', 'cardano-cli '),
        ]

        self.completer = CardanoCliCompleter(
            cli_cmd_lines,
            meta_dict={},
        )

        self.style = Style.from_dict({
            'arrow': '#00FF00',
            'cardano-cli': '#0D93FF',
            'bottom-toolbar': 'bg:#FFFFFF #222',
            'bottom-toolbar-shortcut': 'bg:#FF0066 #222',
            'rprompt': '#FFFFFF bg:#FF0066',
        })

    def bottom_toolbar(self):
        return [
            ('class:bottom-toolbar-shortcut', '[Meta+Enter]'),
            ('class:bottom-toolbar', ' Send Input |'),
            ('class:bottom-toolbar-shortcut', ' [Tab]'),
            ('class:bottom-toolbar', ' Auto Complete |'),
            ('class:bottom-toolbar-shortcut', ' [Ctrl+C + Ctrl+D]'),
            ('class:bottom-toolbar', ' Exit '),
        ]

    def prompt_continuation(self, width, line_number, is_soft_wrap):
        return '> '

    def get_rprompt(self):
        return 'for v1.18.0'
