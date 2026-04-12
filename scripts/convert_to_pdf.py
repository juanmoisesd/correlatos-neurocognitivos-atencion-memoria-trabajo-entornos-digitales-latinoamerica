import os
import markdown
from fpdf import FPDF
from fpdf.html import HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    def __init__(self):
        super().__init__()
        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        font_bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        font_oblique_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf' # Using mono-oblique as fallback for italic

        self.add_font('DejaVu', '', font_path)
        self.add_font('DejaVu', 'B', font_bold_path)
        self.add_font('DejaVu', 'I', font_oblique_path)

    def header(self):
        self.set_font('DejaVu', 'B', 8)
        self.cell(0, 10, 'Meta-análisis Científico - Juan Moisés de la Serna', align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert MD to HTML
    html = markdown.markdown(md_text)

    # Fix for fpdf2 html parser (it likes tags to be balanced and specific)
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html = html.replace('<em>', '<i>').replace('</em>', '</i>')
    # Add font styling to the whole body
    html = f'<div style="font-family: DejaVu; font-size: 11pt;">{html}</div>'

    pdf = MyFPDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output(pdf_path)

md_dir = 'manuscripts/meta_analyses'
pdf_dir = 'manuscripts/pdfs'

if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

for filename in sorted(os.listdir(md_dir)):
    if filename.endswith('.md'):
        md_path = os.path.join(md_dir, filename)
        # Handle non-ascii filenames for PDF output if necessary, but here we keep them
        pdf_name = filename.replace('.md', '.pdf')
        pdf_path = os.path.join(pdf_dir, pdf_name)
        print(f'Converting {md_path} to {pdf_path}...')
        try:
            md_to_pdf(md_path, pdf_path)
        except Exception as e:
            print(f"Failed to convert {md_path}: {e}")
