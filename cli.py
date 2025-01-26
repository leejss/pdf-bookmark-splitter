from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="Split PDF file into chapters based on bookmarks")

    parser.add_argument("file", required=True, help="The PDF file to process")
    parser.add_argument("--prefix", default="Chapter", help="Prefix for output filenames")
    parser.add_argument("--output-dir", default="chapters", help="The directory to save the chapters")

    return parser.parse_args()
