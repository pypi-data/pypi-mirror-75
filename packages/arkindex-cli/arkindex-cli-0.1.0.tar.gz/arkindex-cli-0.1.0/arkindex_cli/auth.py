# -*- coding: utf-8 -*-
import logging
import os
from collections import namedtuple
from pathlib import Path
from typing import Optional

import yaml
from arkindex import ArkindexClient

logger = logging.getLogger("auth")

Profile = namedtuple("Profile", ["slug", "url", "token"])


class Profiles(dict):
    def __init__(self, path: Optional[Path] = None) -> None:
        if not path:
            # Use $XDG_CONFIG_HOME/arkindex/cli.yaml or $HOME/.config/arkindex/cli.yaml
            path = (
                Path(os.environ.get("XDG_CONFIG_HOME") or "~/.config").expanduser()
                / "arkindex"
                / "cli.yaml"
            )
        self.path = path
        self.default_profile_name = None

        if self.path.exists():
            self.load()

    def load(self) -> None:
        try:
            with self.path.open() as f:
                data = yaml.safe_load(f)
        except (IOError, yaml.YAMLError) as e:
            logger.error(f"Failed to load profiles file: {e}")
            return

        for slug, host_data in data.get("hosts", {}).items():
            self[slug] = Profile(slug, host_data["url"], host_data["token"])

        self.default_profile_name = data.get("default_host")

    def get_default_profile(self) -> Optional[Profile]:
        if self.default_profile_name in self:
            return self[self.default_profile_name]

    def set_default_profile(self, name: str) -> None:
        assert name in self, f"Profile {name} does not exist"
        self.default_profile_name = name

    def add_profile(self, slug: str, url: str, token: str) -> None:
        self[slug] = Profile(slug, url, token)

    def get_default_client(self) -> Optional[ArkindexClient]:
        profile = self.get_default_profile()
        if profile:
            return ArkindexClient(base_url=profile.url, token=profile.token)

    def save(self) -> None:
        data = {
            "default_host": self.default_profile_name,
            "hosts": {
                profile.slug: {"url": profile.url, "token": profile.token}
                for profile in self.values()
            },
        }

        # Create parent folders if needed
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
