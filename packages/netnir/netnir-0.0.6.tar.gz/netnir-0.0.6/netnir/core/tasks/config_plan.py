from netnir.constants import NR
from netnir.core.template import CompileTemplate
from netnir.core.networking import Networking
from netnir.helpers import output_writer, TextColor
from netnir.plugins.hier import hier_host
from netnir.helpers.common.args import filter_host
from netnir.constants import OUTPUT_DIR
from nornir.plugins.functions.text import print_result
import logging


"""config plan cli commands
"""


class ConfigPlan:
    """
    config plan cli plugin to render configuration plans, either by
    compiling from template or using hier_config to create a remediation
    plan

    :params args: type obj
    """

    def __init__(self, args):
        """
        initialize the config plan class
        """
        self.args = args
        self.nr = NR

    @staticmethod
    def parser(parser):
        """
        cli options parser

        :params parser: type obj
        """
        filter_host(parser)
        parser.add_argument(
            "--compile",
            nargs="?",
            const=True,
            help="compile configuration from template",
            required=False,
        )
        parser.add_argument(
            "--include-tags",
            action="append",
            help="hier_config include tags",
            required=False,
        )
        parser.add_argument(
            "--exclude-tags",
            action="append",
            help="hier_config exclude tags",
            required=False,
        )

    def run(self, template_file="main.conf.j2"):
        """
        cli execution

        :params template_file: type str

        :returns: result string
        """
        if self.args.host:
            self.nr = self.nr.filter(name=self.args.host)

            compiled_template = CompileTemplate(
                nr=self.nr, host=self.args.host, template=template_file
            )
            output_writer(
                nornir_results=compiled_template.render(), output_file="compiled.conf"
            )
            print_result(compiled_template.render())
        else:
            for host in self.nr.inventory.hosts:
                compiled_template = CompileTemplate(
                    nr=self.nr, host=host, template=template_file
                )
                output_writer(
                    nornir_results=compiled_template.render(),
                    output_file="compiled.conf",
                )
                print_result(compiled_template.render())

        if self.args.compile:
            if self.args.host:
                return compiled_template.render()
            message = TextColor.green("templates compiled for all hosts")
            return logging.info(message)

        networking = Networking(nr=self.nr)
        running_config = networking.fetch(commands="show running")
        output_writer(nornir_results=running_config, output_file="running.conf")
        print_result(running_config)

        result = self.nr.run(
            task=hier_host,
            include_tags=self.args.include_tags,
            exclude_tags=self.args.exclude_tags,
            running_config="running.conf",
            compiled_config="compiled.conf",
            config_path=OUTPUT_DIR,
            load_file=True,
        )

        print_result(result)
        return result
