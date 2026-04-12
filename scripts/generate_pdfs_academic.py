import os
import glob
from fpdf import FPDF
import re

class AcademicPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Academic Policy Brief | Series: Neuroscience and Governance', 0, 0, 'L')
        self.cell(0, 10, 'Juan Moises de la Serna, PhD', 0, 1, 'R')
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.cell(0, 10, f'Page {self.page_no()} | UNIR | ORCID: 0000-0002-8401-8018', 0, 0, 'C')

def clean_text(text):
    # Replace common unicode characters that cause issues with latin-1
    text = text.replace('\u2013', '-').replace('\u2014', '--')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2026', '...')
    # Remove accents for Juan Moisés in header if needed, but helvetica/latin-1 handles some
    return text

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = clean_text(content)

    pdf = AcademicPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    epw = pdf.w - 2*25

    lines = content.split('\n')
    in_author_block = True

    for line in lines:
        line = line.strip()
        if line.startswith('---'):
            in_author_block = False
            pdf.ln(5)
            continue

        if in_author_block:
            if not line: continue
            pdf.set_font('helvetica', 'B' if 'Juan' in line else '', 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(epw, 5, line, align='L')
            continue

        if not line:
            pdf.ln(4)
            continue

        if line.startswith('# '):
            pdf.set_font('helvetica', 'B', 18)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(epw, 10, line[2:], align='L')
            pdf.ln(5)
        elif line.startswith('### '):
            pdf.ln(4)
            pdf.set_font('helvetica', 'B', 14)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(epw, 10, line[4:], align='L')
            pdf.ln(2)
        elif line.startswith('#### '):
            pdf.set_font('helvetica', 'B', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(epw, 8, line[5:], align='L')
        elif line.startswith('**') and line.endswith('**'):
            pdf.set_font('helvetica', 'B', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(epw, 7, line.replace('**', ''), align='L')
        elif line.startswith('* '):
            pdf.set_font('helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(epw, 7, f"- {line[2:]}", align='J')
        elif 'References' in line or '9.' in line:
            pdf.ln(10)
            pdf.set_font('helvetica', 'B', 14)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(epw, 10, line, align='L')
        else:
            pdf.set_font('helvetica', '', 11)
            pdf.set_text_color(0, 0, 0)
            clean_line = re.sub(r'\*\*|\*', '', line)
            try:
                clean_line = clean_line.encode('latin-1', 'replace').decode('latin-1')
            except:
                pass
            pdf.multi_cell(epw, 6.5, clean_line, align='J')

    pdf.output(pdf_path)

if __name__ == "__main__":
    md_files = glob.glob('results/policy_briefs/en/*.md')
    os.makedirs('results/policy_briefs/en/pdf', exist_ok=True)
    for md_file in md_files:
        filename = os.path.basename(md_file).replace('.md', '.pdf')
        pdf_path = os.path.join('results/policy_briefs/en/pdf', filename)
        print(f"Generating Academic PDF: {pdf_path}...")
        md_to_pdf(md_file, pdf_path)
