from typing import List, Tuple
from pypdf import PdfReader, PdfWriter
import os

class PdfSplitter:
    def __init__(self, file_path: str, prefix: str):
        self.file_path = file_path
        self.prefix = prefix

        self.reader = PdfReader(file_path)

    def get_chapter_info(self ) -> List[Tuple[str, int]]:
        """
        Extracts chapter information from the PDF document's outline.

        This method processes the PDF outline/bookmarks to find chapters and their corresponding page numbers.
        Only processes entries that start with "Chapter".

        Returns:
            List[Tuple[str, int]]: A list of tuples containing:
                - str: Chapter title
                - int: Corresponding page number in the PDF

        Returns empty list if outline is empty or invalid.

        Example:
            >>> pdf.get_chapter_info()
            [('Chapter 1', 1), ('Chapter 2', 15), ('Chapter 3', 30)]
        """
        outline = self.reader.outline
        titles: List[Tuple[str, int]] = []

        if not outline or not isinstance(outline, list):
            # ? Throw an exception here ?
            return titles

        for item in outline:
            if isinstance(item, list):
                continue

            title = item.get('/Title', 'No Title')
            page_number = self.reader.get_destination_page_number(item)

            if title.startswith(self.prefix):
                titles.append((title, page_number))

        return titles

    def split_chapters(self, output_dir: str) -> None:
        """
        Splits a PDF file into separate chapters based on bookmarks and saves them to the specified output directory.
        Args:
            output_dir (str): The directory path where the split PDF chapters will be saved.
                             If the directory doesn't exist, it will be created.
        Returns:
            None

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
        os.makedirs(output_dir, exist_ok=True)
        
        chapters = self.get_chapter_info()
        if not chapters:
            print("No chapters found")
            return
        
        total_pages = len(self.reader.pages)
        
        for i, (current_chapter, current_page) in enumerate(chapters):
            end_page = chapters[i + 1][1] if i < len(chapters) - 1 else total_pages
            
            writer = PdfWriter()
            for page_num in range(current_page, end_page):
                writer.add_page(self.reader.pages[page_num])
            
            output_file = os.path.join(output_dir, f"{current_chapter}.pdf")
            with open(output_file, "wb") as output:
                writer.write(output)

            
