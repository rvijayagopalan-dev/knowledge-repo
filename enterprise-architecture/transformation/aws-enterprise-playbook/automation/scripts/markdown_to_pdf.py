#!/usr/bin/env python3
"""
Markdown to PDF Converter for Enterprise Transformation Playbook
Converts markdown artifacts to professional PDF documents
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, Image, KeepTogether
    )
    from reportlab.lib.colors import HexColor
    import markdown
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] Required libraries not installed. Installing...")
    os.system("pip install reportlab markdown beautifulsoup4 lxml")
    print("[OK] Libraries installed. Please run the script again.")
    sys.exit(1)


class MarkdownToPDFConverter:
    """Convert markdown files to professional PDF documents"""

    def __init__(self, pagesize=letter):
        """Initialize converter with page settings"""
        self.pagesize = pagesize
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#1f2937'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#374151'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#4b5563'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#1f2937'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))

        # Code block
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Code'],
            fontSize=9,
            textColor=HexColor('#1f2937'),
            backColor=HexColor('#f3f4f6'),
            spaceAfter=8,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20
        ))

        # Bullet list
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#1f2937'),
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=4
        ))

    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML"""
        return markdown.markdown(
            markdown_text,
            extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists']
        )

    def parse_html_to_flowables(self, html: str) -> List:
        """Parse HTML to reportlab flowables"""
        soup = BeautifulSoup(html, 'html.parser')
        flowables = []

        for element in soup.find_all(recursive=False):
            if element.name == 'h1':
                flowables.append(Paragraph(element.get_text(), self.styles['CustomTitle']))
                flowables.append(Spacer(1, 0.2 * inch))

            elif element.name == 'h2':
                flowables.append(Spacer(1, 0.15 * inch))
                flowables.append(Paragraph(element.get_text(), self.styles['CustomHeading1']))
                flowables.append(Spacer(1, 0.1 * inch))

            elif element.name == 'h3':
                flowables.append(Spacer(1, 0.1 * inch))
                flowables.append(Paragraph(element.get_text(), self.styles['CustomHeading2']))

            elif element.name == 'h4':
                flowables.append(Paragraph(element.get_text(), self.styles['CustomHeading3']))

            elif element.name == 'p':
                text = element.get_text()
                if text.strip():
                    flowables.append(Paragraph(text, self.styles['CustomBodyText']))

            elif element.name == 'ul':
                for li in element.find_all('li', recursive=False):
                    text = f"• {li.get_text()}"
                    flowables.append(Paragraph(text, self.styles['CustomBullet']))

            elif element.name == 'ol':
                for idx, li in enumerate(element.find_all('li', recursive=False), 1):
                    text = f"{idx}. {li.get_text()}"
                    flowables.append(Paragraph(text, self.styles['CustomBullet']))

            elif element.name == 'pre':
                code_text = element.get_text()
                # Split long lines for better formatting
                lines = code_text.split('\n')
                for line in lines:
                    if line.strip():
                        flowables.append(Paragraph(line, self.styles['CustomCode']))

            elif element.name == 'table':
                table_data = []

                # Extract headers
                headers = element.find('thead')
                if headers:
                    header_row = []
                    for th in headers.find_all('th'):
                        header_row.append(Paragraph(th.get_text(), self.styles['CustomHeading3']))
                    table_data.append(header_row)

                # Extract rows
                tbody = element.find('tbody') or element
                for tr in tbody.find_all('tr'):
                    row = []
                    for td in tr.find_all('td'):
                        row.append(Paragraph(td.get_text(), self.styles['CustomBodyText']))
                    if row:
                        table_data.append(row)

                if table_data:
                    table = Table(table_data, hAlign='LEFT')
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1f2937')),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f9fafb')])
                    ]))
                    flowables.append(table)
                    flowables.append(Spacer(1, 0.2 * inch))

            elif element.name == 'hr':
                flowables.append(Spacer(1, 0.1 * inch))
                flowables.append(Paragraph('_' * 100, self.styles['CustomBodyText']))
                flowables.append(Spacer(1, 0.1 * inch))

            elif element.name == 'blockquote':
                quote_style = ParagraphStyle(
                    'Quote',
                    parent=self.styles['CustomBodyText'],
                    leftIndent=30,
                    rightIndent=30,
                    fontName='Helvetica-Oblique',
                    textColor=HexColor('#6b7280')
                )
                flowables.append(Paragraph(element.get_text(), quote_style))

        return flowables

    def add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        canvas.saveState()

        # Header
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(HexColor('#6b7280'))
        canvas.drawString(
            inch,
            doc.height + doc.topMargin + 0.3 * inch,
            "AWS Enterprise Transformation Playbook"
        )

        # Footer
        canvas.setFont('Helvetica', 8)
        footer_text = f"Page {doc.page} | Generated: {datetime.now().strftime('%Y-%m-%d')}"
        canvas.drawRightString(
            doc.width + inch,
            0.5 * inch,
            footer_text
        )

        canvas.restoreState()

    def convert_file(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Convert a markdown file to PDF

        Args:
            input_file: Path to markdown file
            output_file: Path to output PDF (optional)

        Returns:
            Path to generated PDF
        """
        # Read markdown content
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Generate output filename if not provided
        if not output_file:
            output_file = str(Path(input_file).with_suffix('.pdf'))

        # Create PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=self.pagesize,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )

        # Convert markdown to HTML
        html = self.convert_markdown_to_html(markdown_content)

        # Parse HTML to flowables
        flowables = self.parse_html_to_flowables(html)

        # Add cover page
        cover = [
            Spacer(1, 2 * inch),
            Paragraph("AWS Enterprise", self.styles['CustomTitle']),
            Paragraph("Transformation Playbook", self.styles['CustomTitle']),
            Spacer(1, 0.5 * inch),
            Paragraph(
                Path(input_file).stem.replace('-', ' ').replace('_', ' ').title(),
                self.styles['CustomHeading1']
            ),
            Spacer(1, 1 * inch),
            Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y')}",
                self.styles['CustomBodyText']
            ),
            PageBreak()
        ]

        # Build PDF
        all_flowables = cover + flowables
        doc.build(all_flowables, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)

        return output_file

    def convert_directory(self, input_dir: str, output_dir: Optional[str] = None) -> List[str]:
        """
        Convert all markdown files in a directory to PDF

        Args:
            input_dir: Directory containing markdown files
            output_dir: Directory for output PDFs (optional)

        Returns:
            List of generated PDF paths
        """
        input_path = Path(input_dir)

        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = input_path

        generated_pdfs = []

        # Find all markdown files
        md_files = list(input_path.glob('**/*.md'))

        print(f"\n[INFO] Found {len(md_files)} markdown files\n")

        for md_file in md_files:
            try:
                # Generate output path
                relative_path = md_file.relative_to(input_path)
                output_file = output_path / relative_path.with_suffix('.pdf')
                output_file.parent.mkdir(parents=True, exist_ok=True)

                print(f"--> Converting: {md_file.name}")
                pdf_path = self.convert_file(str(md_file), str(output_file))
                generated_pdfs.append(pdf_path)
                print(f"   [OK] Created: {pdf_path}\n")

            except Exception as e:
                print(f"   [ERROR] Error converting {md_file.name}: {e}\n")

        return generated_pdfs


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='Convert Markdown artifacts to professional PDF documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file
  python markdown_to_pdf.py --input README.md --output README.pdf

  # Convert single file (auto-generate output name)
  python markdown_to_pdf.py --input business-case/business-case-template.md

  # Convert all markdown files in directory
  python markdown_to_pdf.py --directory ../../ --output-dir ./pdfs

  # Convert with A4 page size
  python markdown_to_pdf.py --input README.md --pagesize A4

  # Convert specific playbooks
  python markdown_to_pdf.py --directory playbooks/ --output-dir pdf-playbooks/
        """
    )

    parser.add_argument('--input', '-i', type=str,
                       help='Input markdown file')
    parser.add_argument('--output', '-o', type=str,
                       help='Output PDF file (optional)')
    parser.add_argument('--directory', '-d', type=str,
                       help='Directory containing markdown files')
    parser.add_argument('--output-dir', type=str,
                       help='Output directory for PDFs (optional)')
    parser.add_argument('--pagesize', type=str, default='letter',
                       choices=['letter', 'A4'],
                       help='Page size (default: letter)')

    args = parser.parse_args()

    # Validate inputs
    if not args.input and not args.directory:
        parser.error("Either --input or --directory must be specified")

    # Set page size
    pagesize = A4 if args.pagesize == 'A4' else letter

    # Create converter
    converter = MarkdownToPDFConverter(pagesize=pagesize)

    print("\n" + "="*80)
    print("AWS ENTERPRISE TRANSFORMATION PLAYBOOK - PDF GENERATOR".center(80))
    print("="*80 + "\n")

    try:
        if args.input:
            # Convert single file
            if not os.path.exists(args.input):
                print(f"[ERROR] Error: Input file not found: {args.input}")
                sys.exit(1)

            print(f"--> Converting: {args.input}")
            output_path = converter.convert_file(args.input, args.output)
            print(f"[OK] PDF created: {output_path}\n")

        elif args.directory:
            # Convert directory
            if not os.path.exists(args.directory):
                print(f"[ERROR] Error: Directory not found: {args.directory}")
                sys.exit(1)

            pdfs = converter.convert_directory(args.directory, args.output_dir)

            print("="*80)
            print(f"[OK] Successfully converted {len(pdfs)} files")
            print("="*80 + "\n")

            if pdfs:
                print("Generated PDFs:")
                for pdf in pdfs:
                    print(f"    - {pdf}")
                print()

    except Exception as e:
        print(f"\n[ERROR] Error: {e}\n")
        sys.exit(1)

    print("[SUCCESS] PDF generation complete!\n")


if __name__ == '__main__':
    main()
