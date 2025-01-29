# PDF Bookmark Splitter

A Python utility that splits a PDF file into multiple files based on its bookmarks.

## Features

- Splits PDF files using existing bookmarks
- Creates separate PDF files for each bookmark
- Maintains original PDF quality
- Preserves bookmark hierarchy

## Requirements

- Python 3.6+
- PyPDF (automatically installed with package)

## Installation

You can install the package directly from the repository:

```bash
pip install git+https://github.com/leejss/pdf-bookmark-splitter.git
```

Or install in development mode:

```bash
git clone https://github.com/leejss/pdf-bookmark-splitter.git
cd pdf-bookmark-splitter
pip install -e .
```

## Usage

After installation, you can use the command-line tool:

```bash
pdf-split input.pdf
```

This will create separate PDF files in the current directory, named according to the bookmarks in the input PDF.

## Development

To contribute to the project:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
