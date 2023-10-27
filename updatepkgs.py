#!/usr/bin/python3

#
#    This file is part of the Pi Entertainment System (PES).
#
#    PES provides an interactive GUI for games console emulators
#    and is designed to work on the Raspberry Pi.
#
#    Copyright (C) 2020-2023 Neil Munday (neil@mundayweb.com)
#
#    PES is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PES is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PES.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Helper script to automatically update packages that rely on git
commit hashes.
"""

import argparse
import glob
import logging
import pathlib
import re

from github import Github

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("github").setLevel(logging.WARNING)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Automatically update packages that use git to their latest version",
        add_help=True
    )
    parser.add_argument(
        "-t", "--token", help="Personal access token for GitHub API", dest="token"
    )
    parser.add_argument(
        "-v", "--verbose", help="Turn on debug messages", dest="verbose",
        action="store_true"
    )
    args = parser.parse_args()

    log_date = "%Y/%m/%d %H:%M:%S"
    log_format = "%(asctime)s:%(levelname)s: %(message)s"
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(
        format=log_format, datefmt=log_date, level=log_level
    )

    current_dir = pathlib.Path(__file__).parents[0].absolute()

    commit_re = re.compile(r"_commit='(?P<commit>[\w]+)'")
    repo_re = re.compile(r"git\+https://github\.com/(?P<repo>(.*?)).git")

    gh = Github(login_or_token=args.token)

    for pkgbuild in glob.glob(f"{current_dir}/packages/*/PKGBUILD"):
        path = pathlib.Path(pkgbuild)
        if path.is_file():
            pkg_name = path.parent.name
            commit = None
            repo_name = None
            logging.debug("checking: %s", pkg_name)
            lines = []
            commit_line = -1
            with open(path, "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    lines.append(line)
                    match = commit_re.match(line)
                    if match:
                        commit = match.group("commit")
                        commit_line = len(lines) - 1
                        logging.debug("found commit: %s", commit)

                    if line.startswith("source=("):
                        match = repo_re.search(line)
                        if match:
                            repo_name = match.group("repo")
                            logging.debug("found repo name: %s", repo_name)
            
            if not commit or not repo_name:
                logging.debug("skipping %s, no commit usage found", pkg_name)
                continue

            branch = gh.get_repo(repo_name).get_branch("master")
            if commit == branch.commit.sha:
                logging.info("%s is up to date", pkg_name)
            else:
                logging.info("%s can be updated", pkg_name)
                with open(path, "w") as f:
                    line_counter = 0
                    for line in lines:
                        if line_counter == commit_line:
                            f.write(f"_commit='{branch.commit.sha}'\n")
                        else:
                            f.write(f"{line}")
                        line_counter += 1
