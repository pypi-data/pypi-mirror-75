import subprocess
from lb_dev.commands.copyright.check_copyright_comment.check_copyright_comment import check_copyright
from lb_utils.log_utils import set_up_logging

import argparse
from typing import Optional
from typing import Sequence

def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    result = check_copyright(files=args.filenames)

    exit(result)