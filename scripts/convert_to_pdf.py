import os
import markdown
from fpdf import FPDF

class GlobalPDF(FPDF):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        if os.path.exists(font_path):
            self.add_font('DejaVu', '', font_path)
            self.set_font('DejaVu', size=11)
            self.active_font = 'DejaVu'
        else:
            self.set_font('helvetica', size=11)
            self.active_font = 'helvetica'

    def header(self):
        self.set_font(self.active_font, size=8)
        self.cell(0, 10, f'Scientific Meta-Analysis - Juan Moisés de la Serna ({self.lang})', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.active_font, size=8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def process_all():
    for root, dirs, files in os.walk('manuscripts'):
        if 'meta_analyses' in root and 'pdfs' not in root:
            lang = root.split('_')[-1] if '_' in root else 'es'
            pdf_dir = root.replace('meta_analyses', 'pdfs')
            if not os.path.exists(pdf_dir): os.makedirs(pdf_dir)
            for f in sorted(files):
                if f.endswith('.md'):
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as fp:
                        html = markdown.markdown(fp.read())
                        pdf = GlobalPDF(lang)
                        pdf.add_page()
                        # Use a styled block for justify
                        styled_html = f'<div style="text-align: justify;">{html}</div>'
                        pdf.write_html(styled_html)
                        pdf.output(os.path.join(pdf_dir, f.replace('.md', '.pdf')))
                    print(f"Generated PDF for {f} ({lang})")

if __name__ == "__main__":
    process_all()
