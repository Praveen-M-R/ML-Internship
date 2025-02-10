# Content Conversion

## Overview
1. **Markdown to HTML** – Useful for formatting email bodies.
2. **HTML to PDF** – Useful for generating printable documents from web pages.

### 1. Converting Markdown to HTML
Markdown is a simple formatting language commonly used for writing emails and documentation. We use the **markdown2** library to convert Markdown content into properly formatted HTML.

#### Example Usage:
```python
import markdown2

# Sample Markdown content
markdown_body = """
# Welcome!
This is a test email.
- Item 1
- Item 2
"""

# Convert Markdown to HTML
email_body_html = markdown2.markdown(markdown_body)
print(email_body_html)
```

### 2. Converting HTML to PDF
We use **WeasyPrint** to convert HTML files into PDFs while also allowing custom styling. In this example, images are hidden using CSS.

#### Example Usage:
```python
from weasyprint import HTML, CSS

# Define file paths
file_path = "example.html"
pdf_path = "output.pdf"

# Convert HTML to PDF with custom styling
HTML(file_path).write_pdf(pdf_path, stylesheets=[CSS(string="img { display: none !important; }")])

print("PDF generated successfully!")
```

## Installation
Ensure you have the required libraries installed:
```sh
pip install markdown2 weasyprint
```
