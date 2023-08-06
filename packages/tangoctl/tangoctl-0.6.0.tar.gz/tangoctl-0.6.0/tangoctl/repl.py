import shlex
import getpass
import functools

import click
from click.exceptions import Exit as ClickExit
from click import _bashcomplete

from prompt_toolkit import PromptSession, HTML, print_formatted_text
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


from tangoctl import tangoctl

output = click.echo


class Toolbar:
    def __init__(self, db):
        self.db = db

    @property
    def db_info(self):
        return tangoctl.get_db_info(self.db)

    @property
    def db_name(self):
        return tangoctl.get_db_name(self.db)

    def __call__(self):
        db_info = self.db_info
        msg = "<b>{}</b> | #D:{} | #S:{}"
        msg = msg.format(self.db_name, len(db_info.devices), len(db_info.servers))
        return HTML(msg)


class ClickCompleter(Completer):
    def __init__(self, cli):
        self.cli = cli

    def get_completions(self, document, complete_event=None):
        # Code analogous to click._bashcomplete.do_complete

        try:
            args = shlex.split(document.text_before_cursor)
        except ValueError:
            # Invalid command, perhaps caused by missing closing quotation.
            return

        cursor_within_command = (
            document.text_before_cursor.rstrip() == document.text_before_cursor
        )

        if args and cursor_within_command:
            # We've entered some text and no space, give completions for the
            # current word.
            incomplete = args.pop()
        else:
            # We've not entered anything, either at all or for the current
            # command, so give all relevant completions for this context.
            incomplete = ""

        ctx = _bashcomplete.resolve_ctx(self.cli, "", args)
        if ctx is None:
            return

        choices = []
        for param in ctx.command.params:
            if isinstance(param, click.Option):
                for options in (param.opts, param.secondary_opts):
                    for o in options:
                        choices.append(
                            Completion(
                                str(o), -len(incomplete), display_meta=param.help
                            )
                        )
            elif isinstance(param, click.Argument):
                if isinstance(param.type, click.Choice):
                    for choice in param.type.choices:
                        choices.append(Completion(str(choice), -len(incomplete)))

        if isinstance(ctx.command, click.MultiCommand):
            for name in ctx.command.list_commands(ctx):
                command = ctx.command.get_command(ctx, name)
                choices.append(
                    Completion(
                        str(name),
                        -len(incomplete),
                        display_meta=getattr(command, "short_help"),
                    )
                )

        for item in choices:
            if item.text.startswith(incomplete):
                yield item


def Prompt(context):
    # TODO receive db name from context
    db = tangoctl._get_db()
    return PromptSession(
        completer=ClickCompleter(context.command),
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        bottom_toolbar=Toolbar(db),
        key_bindings=KeyBindings(),
        enable_history_search=True,
        message="tangoctl> ",
    )


def run_command_line(context, text):
    args = shlex.split(text)
    group = context.command
    try:
        with group.make_context(None, args, parent=context) as ctx:
            group.invoke(ctx)
            ctx.exit()
    except ClickExit:
        pass
    except SystemExit:
        pass


def step(prompt, context):
    #    prompt = context.obj['prompt']
    while True:
        text = prompt.prompt()
        # empty text would create a sub-repl. Avoid it by
        # returning to the prompt
        if not text:
            continue
        elif text == "exit":
            raise EOFError
        return run_command_line(context, text)


def run(context):
    prompt = Prompt(context)
    while True:
        try:
            step(prompt, context)
        except EOFError:
            # Ctrl-D
            break


def main():
    from tangoctl.cli import cli

    cli()


if __name__ == "__main__":
    main()
