# Copyright 2020 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

"""Provide all help texts."""

import textwrap


# the summary of the whole program, already indented so it represents the real
# "columns spread", for easier human editing.
SUMMARY = """
    Charmcraft provides a streamlined, powerful, opinionated, and
    flexible tool to develop, package, and manage the lifecycle of
    Juju charm publication, focused particularly on charms written
    within the Operator Framework.
"""
# XXX Facundo 2020-07-13: we should add an extra (separated) line with:
#   See <url> for additional documentation.


#FIXME: help command!
#FIXME: help --all


def get_full_help(command_groups):
    """Produce the text for the default help.

    The default help has the following structure:

    - usage
    - summary (link to docs)
    - common commands listed and described shortly
    - coomands grouped and listed
    - more help
    """
    textblocks = []

    # title
    textblocks.append(textwrap.dedent("""\
        Usage:
            charmcraft [help] <command>
    """))

    # summary
    textblocks.append("Summary:" + SUMMARY)

    # collect common commands
    common_commands = []
    for commands in command_groups:
        for cmd in commands:
            common_commands.append(cmd)

    # column is dictated by longest common commands names and groups names
    max_len = 0
    common_commands





    # join all stripped blocks, leaving ONE empty blank line
    text = '\n\n'.join(block.strip() for block in textblocks) + '\n'
    return text
