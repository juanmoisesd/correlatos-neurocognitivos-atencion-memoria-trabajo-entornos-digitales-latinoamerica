import os
import markdown
from fpdf import FPDF
from fpdf.html import HTMLMixin
import sys

class MyFPDF(FPDF, HTMLMixin):
    def __init__(self):
        super().__init__()
        font_locations = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/TTF/DejaVuSans.ttf',
            'DejaVuSans.ttf'
        ]
        font_path = None
        for loc in font_locations:
            if os.path.exists(loc):
                font_path = loc
                break

        if not font_path:
            self.set_font("helvetica", size=11)
        else:
            self.add_font('DejaVu', '', font_path)

            font_bold_path = font_path.replace('.ttf', '-Bold.ttf')
            if os.path.exists(font_bold_path):
                self.add_font('DejaVu', 'B', font_bold_path)
            else:
                self.add_font('DejaVu', 'B', font_path)

            font_italic_path = font_path.replace('.ttf', '-Oblique.ttf')
            if os.path.exists(font_italic_path):
                self.add_font('DejaVu', 'I', font_italic_path)
            else:
                self.add_font('DejaVu', 'I', font_path)

    def header(self):
        try:
            self.set_font('DejaVu', 'B', 8)
        except:
            self.set_font('helvetica', 'B', 8)
        self.cell(0, 10, 'Collection de Méta-Analyses Scientifiques - Juan Moisés de la Serna', align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        try:
            self.set_font('DejaVu', '', 8)
        except:
            self.set_font('helvetica', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html = markdown.markdown(md_text, extensions=['extra'])
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html = html.replace('<em>', '<i>').replace('</em>', '</i>')

    font_family = "DejaVu" if "DejaVu" in MyFPDF().fonts else "helvetica"
    styled_html = f'<div style="font-family: {font_family}; font-size: 11pt; text-align: justify;">{html}</div>'

    pdf = MyFPDF()
    pdf.add_page()
    pdf.write_html(styled_html)
    pdf.output(pdf_path)

def process_dir(md_dir, pdf_dir):
    if not os.path.exists(md_dir):
        return
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    for filename in sorted(os.listdir(md_dir)):
        if filename.endswith('.md'):
            md_path = os.path.join(md_dir, filename)
            pdf_path = os.path.join(pdf_dir, filename.replace('.md', '.pdf'))
            print(f'Converting {md_path} to {pdf_path}...')
            try:
                md_to_pdf(md_path, pdf_path)
            except Exception as e:
                print(f"Failed to convert {md_path}: {e}")

if __name__ == "__main__":
    process_dir('manuscripts/meta_analyses', 'manuscripts/pdfs')
    process_dir('manuscripts/meta_analyses_en', 'manuscripts/pdfs_en')
    process_dir('manuscripts/meta_analyses_fr', 'manuscripts/pdfs_fr')
