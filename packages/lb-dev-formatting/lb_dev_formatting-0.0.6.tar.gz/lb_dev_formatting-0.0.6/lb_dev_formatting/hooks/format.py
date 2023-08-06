from lb_dev_formatting.commands.format import format_files
from lb_utils.git_utils import GitUtils
from lb_utils.log_utils import set_up_logging
from lb_dev_formatting import constants

import logging
import argparse
from typing import Optional
from typing import Sequence

log = logging.getLogger(__name__)

def format(argv: Optional[Sequence[str]] = None):
    set_up_logging(10)

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    return format_files(args.filenames, constants.CLANG_FORMAT_VERSION, '0.24.0', True, None, False, None)