# How to Convert Markdown to PDF with Mermaid Diagrams

This guide provides a step-by-step method to convert a Markdown (`.md`) file to a PDF while processing and embedding Mermaid diagrams.

## Prerequisites

Ensure you have the required dependencies installed:

### Install `mermaid-cli` (for Mermaid diagram conversion)
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Install Python dependencies
```bash
pip install markdown2 weasyprint
```

## Python Script to Convert Markdown to PDF

Save the following script as `convert_md_to_pdf.py`:

```python
import re
import os
import subprocess
import markdown2
from weasyprint import HTML

# Input and output files
md_file = "readme.md"
output_pdf = "readme.pdf"

# Read the Markdown file
with open(md_file, "r", encoding="utf-8") as file:
    content = file.read()

# Find all Mermaid code blocks
mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", content, re.DOTALL)

# Create a directory for diagrams
os.makedirs("diagrams", exist_ok=True)

# Process Mermaid diagrams
for i, mermaid_code in enumerate(mermaid_blocks, start=1):
    mermaid_file = f"diagrams/diagram_{i}.mmd"
    png_file = f"diagrams/diagram_{i}.png"

    # Save the Mermaid code to a file
    with open(mermaid_file, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    print(f"Converting {mermaid_file} to PNG...")
    try:
        subprocess.run(["mmdc", "-i", mermaid_file, "-o", png_file], check=True)
        print(f"✅ {png_file} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting {mermaid_file}: {e}")

# Replace Mermaid blocks with image references
for i in range(1, len(mermaid_blocks) + 1):
    content = re.sub(r"```mermaid\n(.*?)\n```", f"![Diagram {i}](diagrams/diagram_{i}.png)", content, 1, flags=re.DOTALL)

# Convert Markdown to HTML using markdown2
html_body = markdown2.markdown(content)

# Create full HTML structure
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to PDF</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 10px auto; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        code {{ font-family: monospace; background: #f4f4f4; padding: 3px; border-radius: 3px; }}
        h1, h2, h3, h4, h5, h6 {{ color: #333; }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

# Save HTML file
html_file = "readme.html"
with open(html_file, "w", encoding="utf-8") as file:
    file.write(html_template)

# Convert HTML to PDF using WeasyPrint
print("Converting HTML to PDF...")
try:
    HTML(html_file).write_pdf(output_pdf)
    print(f"✅ {output_pdf} created successfully.")
except Exception as e:
    print(f"❌ Error converting HTML to PDF: {e}")
```

## Running the Script

Run the script using:
```bash
python convert_md_to_pdf.py
```

This will generate `readme.pdf` with embedded images for Mermaid diagrams.

## Summary
- Extracts Mermaid diagrams from `readme.md`.
- Converts them into PNG images using `mmdc`.
- Replaces Mermaid code blocks with image references.
- Converts Markdown to HTML using `markdown2`.
- Converts the final HTML to a PDF using `WeasyPrint`.

Use this script whenever you need to generate a **PDF** from a Markdown file with Mermaid diagrams! 🚀

