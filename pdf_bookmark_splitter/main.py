import sys
import os
from .cli import parse_args
from .pdf_operations import PdfSplitter


def main():
    try:
        args = parse_args()

        # Validate input file
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            return 1

        if not os.path.isfile(args.file):
            print(f"Error: '{args.file}' is not a file", file=sys.stderr)
            return 1

        # Check file extension
        if not args.file.lower().endswith('.pdf'):
            print(f"Warning: '{args.file}' may not be a PDF file", file=sys.stderr)

        # Initialize splitter with verbose/quiet options
        try:
            splitter = PdfSplitter(args.file, verbose=args.verbose, quiet=args.quiet)
        except Exception as e:
            print(f"Error: Failed to read PDF file: {e}", file=sys.stderr)
            return 1

        # Handle --list-bookmarks option
        if args.list_bookmarks:
            chapters = splitter.get_chapter_info()
            if not chapters:
                print("No bookmarks found in the PDF")
                return 0

            print(f"\nFound {len(chapters)} bookmark(s):\n")
            for i, (title, page) in enumerate(chapters, 1):
                print(f"{i:3}. Page {page:4}: {title}")
            print()
            return 0

        # Split the PDF
        created_files = splitter.split_chapters(args.output_dir, dry_run=args.dry_run)

        # Return success if files were created (or would be created in dry-run)
        if created_files or args.dry_run:
            return 0
        else:
            # No files created (likely no bookmarks)
            return 1

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user", file=sys.stderr)
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
