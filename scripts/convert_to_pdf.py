import os
import markdown
from fpdf import FPDF

class AcademicPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.cell(0, 10, 'Scientific Meta-Analysis - Juan Moisés de la Serna', align='C', new_x='LMARGIN', new_y='NEXT')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdfs():
    for root, dirs, files in os.walk('manuscripts'):
        if 'meta_analyses' in root and 'pdfs' not in root:
            pdf_dir = root.replace('meta_analyses', 'pdfs')
            os.makedirs(pdf_dir, exist_ok=True)
            for f in sorted(files):
                if f.endswith('.md'):
                    md_path = os.path.join(root, f)
                    pdf_path = os.path.join(pdf_dir, f.replace('.md', '.pdf'))
                    with open(md_path, 'r', encoding='utf-8') as fp:
                        html = markdown.markdown(fp.read())
                    pdf = AcademicPDF()
                    pdf.add_page()
                    pdf.write_html(f'<div style="text-align: justify;">{html}</div>')
                    pdf.output(pdf_path)

if __name__ == "__main__":
    generate_pdfs()
