from .cli import parse_args
from .pdf_operations import PdfSplitter

def main():
    args = parse_args()
    splitter = PdfSplitter(args.file, args.prefix)
    splitter.split_chapters(args.output_dir)

if __name__ == "__main__":
    main()
