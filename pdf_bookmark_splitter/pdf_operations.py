import os
import re
from typing import List, Tuple
from pypdf import PdfReader, PdfWriter


class PdfSplitter:
    def __init__(self, file_path: str, verbose: bool = False, quiet: bool = False):
        self.file_path = file_path
        self.reader = PdfReader(file_path)
        self.verbose = verbose
        self.quiet = quiet

    def _print(self, message: str, force: bool = False):
        """Print message unless quiet mode is enabled."""
        if force or not self.quiet:
            print(message)

    def _print_verbose(self, message: str):
        """Print message only in verbose mode."""
        if self.verbose:
            print(f"[VERBOSE] {message}")

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing or replacing invalid characters.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for all operating systems
        """
        # Replace invalid characters with underscore
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        sanitized = re.sub(invalid_chars, '_', filename)

        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')

        # Limit length to 200 characters to avoid filesystem limits
        if len(sanitized) > 200:
            sanitized = sanitized[:200]

        # Ensure filename is not empty
        if not sanitized:
            sanitized = "unnamed"

        return sanitized

    def _extract_outline_recursive(self, outline_items: list, titles: List[Tuple[str, int]]) -> None:
        """
        Recursively extracts all bookmark entries from nested outline structure.
        
        Args:
            outline_items: List of outline items (can contain nested lists)
            titles: Accumulator list to store extracted (title, page_number) tuples
        """
        for item in outline_items:
            if isinstance(item, list):
                # Recursively process nested outline
                self._extract_outline_recursive(item, titles)
            else:
                # Extract title and page number from bookmark
                title = item.get("/Title", "No Title")
                page_number = self.reader.get_destination_page_number(item)
                titles.append((title, page_number))

    def get_chapter_info(self) -> List[Tuple[str, int]]:
        """
        Extracts chapter information from the PDF document's outline.

        This method processes the PDF outline/bookmarks to find chapters and their corresponding page numbers.
        Processes ALL outline entries including nested sub-outlines recursively.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing:
                - str: Chapter title
                - int: Corresponding page number in the PDF
            
            The list is sorted by page number in ascending order.

        Returns empty list if outline is empty or invalid.

        Example:
            >>> pdf.get_chapter_info()
            [('Chapter 1', 1), ('Chapter 1.1', 3), ('Chapter 2', 15), ('Chapter 2.1', 17)]
        """
        outline = self.reader.outline
        titles: List[Tuple[str, int]] = []

        if not outline or not isinstance(outline, list):
            # fail to get outline. return empty list
            return titles

        # Recursively extract all bookmarks
        self._extract_outline_recursive(outline, titles)
        
        # Sort by page number to ensure correct splitting order
        titles.sort(key=lambda x: x[1])

        return titles

    def split_chapters(self, output_dir: str, dry_run: bool = False) -> List[str]:
        """
        Splits a PDF file into separate chapters based on bookmarks and saves them to the specified output directory.
        Args:
            output_dir (str): The directory path where the split PDF chapters will be saved.
                             If the directory doesn't exist, it will be created.
            dry_run (bool): If True, only show what would be done without creating files.
        Returns:
            List[str]: List of created file paths (empty if dry_run or no chapters)

        The method will:
        1. Create the output directory if it doesn't exist
        2. Get chapter information from bookmarks
        3. Split the PDF into chapters based on bookmark page numbers
        4. Save each chapter as a separate PDF file named after the chapter title
        If no chapters (bookmarks) are found, it will print a message and return without splitting.
        Example:
            pdf_splitter.split_chapters("output/chapters/")
            # Creates PDFs like: output/chapters/Chapter1.pdf, output/chapters/Chapter2.pdf, etc.
        """
        chapters = self.get_chapter_info()

        if not chapters:
            self._print("No chapters found", force=True)
            return []

        if not dry_run:
            os.makedirs(output_dir, exist_ok=True)
            self._print_verbose(f"Created output directory: {output_dir}")

        total_pages = len(self.reader.pages)
        created_files = []
        used_filenames = {}

        self._print(f"\nProcessing {len(chapters)} chapter(s)...")

        for i, (current_chapter, current_page) in enumerate(chapters, 1):
            end_page = chapters[i - 1 + 1][1] if (i - 1) < len(chapters) - 1 else total_pages
            page_count = end_page - current_page

            # Sanitize filename and handle duplicates
            sanitized_name = self.sanitize_filename(current_chapter)
            if sanitized_name in used_filenames:
                used_filenames[sanitized_name] += 1
                sanitized_name = f"{sanitized_name}_{used_filenames[sanitized_name]}"
            else:
                used_filenames[sanitized_name] = 1

            output_file = os.path.join(output_dir, f"{sanitized_name}.pdf")

            if dry_run:
                self._print(f"[DRY RUN] Would create: {output_file}")
                self._print_verbose(f"  Chapter: {current_chapter}")
                self._print_verbose(f"  Pages: {current_page} to {end_page - 1} ({page_count} page(s))")
            else:
                self._print_verbose(f"[{i}/{len(chapters)}] Processing: {current_chapter}")
                self._print_verbose(f"  Pages: {current_page} to {end_page - 1} ({page_count} page(s))")

                writer = PdfWriter()
                for page_num in range(current_page, end_page):
                    writer.add_page(self.reader.pages[page_num])

                with open(output_file, "wb") as output:
                    writer.write(output)

                self._print(f"✓ Created: {output_file}")
                created_files.append(output_file)

        if not dry_run:
            self._print(f"\nSuccessfully created {len(created_files)} file(s) in '{output_dir}'")

        return created_files
