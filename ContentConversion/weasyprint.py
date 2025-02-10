from weasyprint import HTML, CSS


HTML(file_path).write_pdf(pdf_path, stylesheets=[CSS(string="img { display: none !important; }")])
