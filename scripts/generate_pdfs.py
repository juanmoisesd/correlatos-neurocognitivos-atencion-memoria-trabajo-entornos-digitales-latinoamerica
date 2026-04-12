import os
import glob
from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Policy Brief - Juan Moises de la Serna', align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('helvetica', '', 11)

    # Effective width
    epw = pdf.w - 2*pdf.l_margin

    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue

        if line.startswith('# '):
            pdf.set_font('helvetica', 'B', 16)
            pdf.multi_cell(epw, 10, line[2:])
            pdf.ln(5)
        elif line.startswith('### '):
            pdf.set_font('helvetica', 'B', 14)
            pdf.multi_cell(epw, 10, line[4:])
            pdf.ln(2)
        elif line.startswith('**') and line.endswith('**'):
            pdf.set_font('helvetica', 'B', 11)
            pdf.multi_cell(epw, 8, line.replace('**', ''))
        elif line.startswith('---'):
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + epw, pdf.get_y())
            pdf.ln(2)
        else:
            pdf.set_font('helvetica', '', 11)
            clean_line = re.sub(r'\*\*|\*', '', line)
            clean_line = clean_line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(epw, 7, clean_line)

    pdf.output(pdf_path)

if __name__ == "__main__":
    md_files = glob.glob('results/policy_briefs/*.md')
    os.makedirs('results/policy_briefs/pdf', exist_ok=True)
    for md_file in md_files:
        filename = os.path.basename(md_file).replace('.md', '.pdf')
        pdf_path = os.path.join('results/policy_briefs/pdf', filename)
        print(f"Generating {pdf_path}...")
        md_to_pdf(md_file, pdf_path)
