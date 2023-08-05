from collections import OrderedDict
from typing import Any, Dict

name: str = "cz_conventional_commits"
# TODO: .cz, setup.cfg, .cz.cfg should be removed in 2.0
long_term_support_config_files: list = ["pyproject.toml", ".cz.toml"]
deprcated_config_files: list = [".cz", "setup.cfg", ".cz.cfg"]
config_files: list = long_term_support_config_files + deprcated_config_files

DEFAULT_SETTINGS: Dict[str, Any] = {
    "name": "cz_conventional_commits",
    "version": None,
    "version_files": [],
    "tag_format": None,  # example v$version
    "bump_message": None,  # bumped v$current_version to $new_version
    "changelog_file": "CHANGELOG.md",
}

MAJOR = "MAJOR"
MINOR = "MINOR"
PATCH = "PATCH"

bump_pattern = r"^(BREAKING[\-\ ]CHANGE|feat|fix|refactor|perf)(\(.+\))?(!)?"
bump_map = OrderedDict(
    (
        (r"^.+!$", MAJOR),
        (r"^BREAKING[\-\ ]CHANGE", MAJOR),
        (r"^feat", MINOR),
        (r"^fix", PATCH),
        (r"^refactor", PATCH),
        (r"^perf", PATCH),
    )
)
bump_message = "bump: version $current_version → $new_version"

commit_parser = r"^(?P<change_type>feat|fix|refactor|perf|BREAKING CHANGE)(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)?"  # noqa
version_parser = r"(?P<version>([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?)"
