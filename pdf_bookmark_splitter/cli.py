from argparse import ArgumentParser
import sys

__version__ = "0.1.0"

def parse_args():
    parser = ArgumentParser(
        description="Split PDF file into chapters based on bookmarks",
        epilog="Example: pdf-split book.pdf --output-dir chapters"
    )

    parser.add_argument(
        "file",
        help="The PDF file to process"
    )

    parser.add_argument(
        "--output-dir",
        default="chapters",
        help="The directory to save the chapters (default: chapters)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except errors"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually creating files"
    )

    parser.add_argument(
        "--list-bookmarks",
        action="store_true",
        help="List all bookmarks and exit"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Validate mutually exclusive options
    if args.verbose and args.quiet:
        parser.error("--verbose and --quiet cannot be used together")

    return args
