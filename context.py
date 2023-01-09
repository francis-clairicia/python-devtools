# -*- coding: Utf-8 -*-

from __future__ import annotations

__all__ = ["Context", "load_context_from_file"]

import re
from configparser import ConfigParser
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True, kw_only=True)
class Context:
    requirements_files: MappingProxyType[str, str]
    requirements_files_extra_requires: MappingProxyType[str, tuple[str, ...] | None]


REQUIREMENTS_FILE_SECTION_PATTERN = re.compile(r"^devtools:file:(.+)")


def load_context_from_file(filepath: str) -> Context:
    config = ConfigParser(default_section="")
    config.read(filepath)

    requirements_files_dict: dict[str, str] = {}
    requirements_files_extra_requires_dict: dict[str, tuple[str, ...] | None] = {}

    for section in config.sections():
        if not (m := REQUIREMENTS_FILE_SECTION_PATTERN.match(section)):
            continue

        requirements_file: str = str(m.group(1))
        if not config.has_option(section, "input"):
            raise ValueError(f"[{section}]: 'input' option required")
        requirements_file_input: str = config.get(section, "input")
        requirements_files_dict[requirements_file] = requirements_file_input

        extra_requires: tuple[str, ...] = tuple(
            filter(None, map(lambda e: e.strip(), config.get(section, "extras", fallback="").split(",")))
        )
        if extra_requires:
            requirements_files_extra_requires_dict[requirements_file] = extra_requires

        if config.getboolean(section, "all-extras", fallback=False):
            requirements_files_extra_requires_dict[requirements_file] = None

    return Context(
        requirements_files=MappingProxyType(requirements_files_dict),
        requirements_files_extra_requires=MappingProxyType(requirements_files_extra_requires_dict),
    )
