"""A plugin that adds the ``query`` command to RepoBee, allowing users to query
a hook results JSON file.

.. module:: query
    :synopsis: Plugin that adds a query command to RepoBee.

.. moduleauthor:: Simon Larsén
"""
import pathlib
import sys
import collections

import daiquiri
import repobee_plug as plug

from _repobee import formatters

LOGGER = daiquiri.getLogger(__file__)


class Query(plug.Plugin, plug.cli.Command):
    __settings__ = plug.cli.command_settings(
        help="Query a hook results JSON file for information.",
        description="Query a hook results JSON file for information.",
        base_parsers=[plug.BaseParser.STUDENTS, plug.BaseParser.REPO_NAMES],
    )

    hook_results_file = plug.cli.option(
        short_name="--hf",
        help="Path to an existing hook results file.",
        required=True,
    )

    def command(self, api: plug.API) -> None:
        hook_results_file = pathlib.Path(self.hook_results_file).resolve()
        if not hook_results_file.exists():
            raise plug.PlugError(
                "no such file: {}".format(str(hook_results_file))
            )

        contents = hook_results_file.read_text(
            encoding=sys.getdefaultencoding()
        )
        hook_results_mapping = plug.json_to_result_mapping(contents)
        selected_hook_results = _filter_hook_results(
            hook_results_mapping,
            self.args.students,
            self.args.master_repo_names,
        )
        LOGGER.info(
            formatters.format_hook_results_output(selected_hook_results)
        )


def _filter_hook_results(hook_results_mapping, teams, master_repo_names):
    """Return an OrderedDict of hook result mappings for which the repo name is
    contained in the cross product of teams and master repo names.
    """
    repo_names = set(plug.generate_repo_names(teams, master_repo_names))
    selected_hook_results = collections.OrderedDict()
    for repo_name, hook_results in sorted(hook_results_mapping.items()):
        if repo_name in repo_names:
            selected_hook_results[repo_name] = hook_results
    missing_repo_names = repo_names - selected_hook_results.keys()
    _log_missing_repo_names(missing_repo_names)
    return selected_hook_results


def _log_missing_repo_names(missing_repo_names):
    if missing_repo_names:
        LOGGER.warning(
            "No hook results found for {}".format(
                ", ".join(missing_repo_names)
            )
        )
