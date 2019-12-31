# ----------------------------------------------------------------------
# |
# |  __init__.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2019-04-25 13:05:08
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2019
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Contains the CodeCoverageExecutor object"""

import os

import CommonEnvironment
from CommonEnvironment import Interface
from CommonEnvironment import Process

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
class CodeCoverageExecutor(Interface.Interface):
    """Object that is able to execute a command line that extracts code coverage information"""

    # ----------------------------------------------------------------------
    # |  Properties
    @Interface.abstractproperty
    def DefaultFileName(self):
        raise Exception("Abstract Property")

    @Interface.abstractproperty
    def Units(self):
        raise Exception("Abstract Property")

    # ----------------------------------------------------------------------
    # |  Methods
    @staticmethod
    @Interface.extensionmethod
    def PreprocessBinary(binary_filename, output_stream):
        """Decorate the binary if necessary.

        Returns result_code.
        """
        return 0

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.extensionmethod
    def StartCoverage(coverage_filename, output_stream):
        """Initializes code coverage functionality if necessary.

        Returns result_code.
        """
        return 0

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.extensionmethod
    def Execute(command_line, output_stream):
        """Executes the command line

        Returns result_code."""
        return Process.Execute(command_line, output_stream)

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.extensionmethod
    def StopCoverage(output_stream):
        """Stops code coverage processing and returns a data filename that contains coverage information

        Returns result_code."""
        return 0

    # ----------------------------------------------------------------------
    @staticmethod
    @Interface.abstractmethod
    def ExtractCoverageInfo(coverage_filename, binary_filename, includes, excludes, output_stream):
        pass
