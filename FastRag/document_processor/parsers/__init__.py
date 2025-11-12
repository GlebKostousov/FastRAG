"""Module for parse all type off input file"""

from document_processor.parsers.code_parser import CodeParser
from document_processor.parsers.html_parser import HTMLParser
from document_processor.parsers.pdf_parser import PDFParser

__all__ = (
    "CodeParser",
    "HTMLParser",
    "PDFParser",
)
