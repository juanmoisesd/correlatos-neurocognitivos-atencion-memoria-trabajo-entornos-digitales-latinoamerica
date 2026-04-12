import os
import markdown
from fpdf import FPDF

class GlobalPDF(FPDF):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        # Register fonts
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')

        if lang in ['zh_Hant', 'ja', 'ko']:
            self.add_font('CJK', '', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
            self.set_font('CJK', size=11)
            self.active_font = 'CJK'
        elif lang in ['ar', 'he', 'hi']:
            # FreeSans has good coverage for many scripts
            self.add_font('FreeSans', '', '/usr/share/fonts/truetype/freefont/FreeSans.ttf')
            self.set_font('FreeSans', size=11)
            self.active_font = 'FreeSans'
        else:
            self.set_font('DejaVu', size=11)
            self.active_font = 'DejaVu'

    def header(self):
        self.set_font(self.active_font, 'B' if self.active_font == 'DejaVu' else '', 8)
        self.cell(0, 10, f'Meta-Analysis Collection ({self.lang}) - Juan Moisés de la Serna', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.active_font, '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def md_to_pdf(md_path, pdf_path, lang):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html = markdown.markdown(md_text, extensions=['extra'])
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html = html.replace('<em>', '<i>').replace('</em>', '</i>')

    pdf = GlobalPDF(lang)
    pdf.add_page()

    # We use write_html for basic formatting
    # For RTL, fpdf2 write_html has some limitations but we try
    align = "right" if lang in ['ar', 'he'] else "justify"
    styled_html = f'<div style="text-align: {align};">{html}</div>'

    pdf.write_html(styled_html)
    pdf.output(pdf_path)

if __name__ == "__main__":
    manuscripts_dir = 'manuscripts'
    for lang_dir in sorted(os.listdir(manuscripts_dir)):
        if lang_dir.startswith('meta_analyses_') and not lang_dir.endswith(('_en', '_fr')):
            lang = lang_dir.replace('meta_analyses_', '')
            md_path_dir = os.path.join(manuscripts_dir, lang_dir)
            pdf_path_dir = os.path.join(manuscripts_dir, f'pdfs_{lang}')
            if not os.path.exists(pdf_path_dir):
                os.makedirs(pdf_path_dir)
            for filename in sorted(os.listdir(md_path_dir)):
                if filename.endswith('.md'):
                    md_file = os.path.join(md_path_dir, filename)
                    pdf_file = os.path.join(pdf_path_dir, filename.replace('.md', '.pdf'))
                    print(f'Converting {md_file}...')
                    try:
                        md_to_pdf(md_file, pdf_file, lang)
                    except Exception as e:
                        print(f"Failed {md_file}: {e}")
