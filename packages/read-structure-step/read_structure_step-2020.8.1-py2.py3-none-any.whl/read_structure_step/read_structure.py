# -*- coding: utf-8 -*-

"""Non-graphical part of the Read Structure step in a SEAMM flowchart

In addition to the normal logger, two logger-like printing facilities are
defined: 'job' and 'printer'. 'job' send output to the main job.out file for
the job, and should be used very sparingly, typically to echo what this step
will do in the initial summary of the job.

'printer' sends output to the file 'step.out' in this steps working
directory, and is used for all normal output from this step.
"""

import configargparse
import logging
import seamm
from seamm import data  # noqa: F401
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import read_structure_step
from .read import read

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('Read Structure')


def upcase(string):
    """Return an uppercase version of the string.

    Used for the type argument in argparse/
    """
    return string.upper()


class ReadStructure(seamm.Node):

    def __init__(self, flowchart=None, title='Read Structure', extension=None):
        """A step for Read Structure in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters:
            flowchart: The flowchart that contains this step.
            title: The name displayed in the flowchart.

            extension: ??

        Returns:
            None
        """
        logger.debug('Creating Read Structure {}'.format(self))

        # Argument/config parsing
        self.parser = configargparse.ArgParser(
            auto_env_var_prefix='',
            default_config_files=[
                '/etc/seamm/read_structure_step.ini',
                '/etc/seamm/seamm.ini',
                '~/.seamm/read_structure_step.ini',
                '~/.seamm/seamm.ini',
            ]
        )

        self.parser.add_argument(
            '--seamm-configfile',
            is_config_file=True,
            default=None,
            help='a configuration file to override others'
        )

        # Options for this plugin
        self.parser.add_argument(
            "--read-structure-step-log-level",
            default=configargparse.SUPPRESS,
            choices=[
                'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            ],
            type=upcase,
            help="the logging level for the Read Structure step"
        )

        self.options, self.unknown = self.parser.parse_known_args()

        # Set the logging level for this module if requested
        if 'read_structure_step_log_level' in self.options:
            logger.setLevel(self.options.read_structure_step_log_level)

        super().__init__(
            flowchart=flowchart, title='Read Structure', extension=extension
        )

        self.parameters = read_structure_step.ReadStructureParameters()

    @property
    def version(self):
        """The semantic version of this module.
        """
        return read_structure_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return read_structure_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Keyword arguments:
            P: An optional dictionary of the current values of the control
               parameters.
        """

        if not P:
            P = self.parameters.values_to_dict()

        if P['file'] == '' and self.unknown != '':
            P['file'] = self.unknown[1]
        text = 'Read structure from {}'.format(P['file'])

        return text

    def run(self):
        """Run a Read Structure step.
        """

        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )
        if P['file'] == '' and self.unknown != '':
            P['file'] = self.unknown[1]

        # Temporary code just to print the parameters. You will need to change
        # this!
        for key in P:
            printer.normal(
                __(
                    '{key:>15s} = {value}',
                    key=key,
                    value=P[key],
                    indent=4 * ' ',
                    wrap=False,
                    dedent=False
                )
            )

        # Analyze the results
        structure = read(P['file'])

        seamm.data.structure = structure

        self.analyze()

        return next_node

    def analyze(self, indent='', **kwargs):
        """Do any analysis of the output from this step.

        Also print important results to the local step.out file using
        'printer'.

        Parameters:
            indent: An extra indentation for the output

            kwargs: Other arguments.

        Returns
            None
        """
        printer.normal(
            __(
                'This is a placeholder for the results from the '
                'Read Structure step',
                indent=4 * ' ',
                wrap=True,
                dedent=False
            )
        )
