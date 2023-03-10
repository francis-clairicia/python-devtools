from __future__ import annotations

__all__ = ["RepoCommand"]

from argparse import ArgumentParser
from typing import Any, final

from ..context import Context
from .abc import AbstractCommand, Configuration
from .piptools import PipCompileCommand, PipSyncCommand
from .venv import VenvCommand


@final
class RepoCommand(AbstractCommand):
    def __init__(self, config: Configuration) -> None:
        super().__init__(config)

    @classmethod
    def get_parser_kwargs(cls) -> dict[str, Any]:
        return super().get_parser_kwargs() | {"help": "Setup the repository for development"}

    @classmethod
    def register_to_parser(cls, parser: ArgumentParser, context: Context) -> None:
        parser.add_argument("-s", "--no-sync", dest="pip_sync", action="store_false", help="Do not run 'pip-sync'")

    def run(self, args: Any, /) -> int:
        self.setup(pip_sync=args.pip_sync)
        return 0

    def setup(self, pip_sync: bool = True) -> None:
        config: Configuration = self.config

        if config.venv_dir is not None:
            VenvCommand(config).create()
        self.ensure_piptools()
        PipCompileCommand(config).compile_all(list(config.context.requirements_files))
        if pip_sync:
            PipSyncCommand(config).sync()
