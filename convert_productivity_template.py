"""
Convert standalone productivity-sheet.html to Flask template extending base.html
"""
from pathlib import Path
import re

source_file = Path("templates/productivity-sheet.html")
output_file = Path("templates/productivity-sheet-flask.html")

# Read the original file
content = source_file.read_text(encoding="utf-8")

# Extract the styles from the <style> tag
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
styles = style_match.group(1) if style_match else ""

# Extract the main content (everything inside <main> tags)
main_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
main_content = main_match.group(1) if main_match else ""

# Extract the JavaScript from the <script> tag at the end
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
scripts = script_match.group(1) if script_match else ""

# Create the Flask template
flask_template = f'''
{{% extends "base.html" %}}

{{% block title %}}Employee Productivity Sheet - Shrikruthi Yeshala{{% endblock %}}

{{% block extra_css %}}
<style>
{styles}
</style>
{{% endblock %}}

{{% block content %}}
{main_content}
{{% endblock %}}

{{% block extra_js %}}
<script>
{scripts}
</script>
{{% endblock %}}
'''.strip()

# Write the new template
output_file.write_text(flask_template, encoding="utf-8")
print(f"✅ Created Flask template: {output_file}")
print(f"   Styles: {len(styles)} characters")
print(f"   Content: {len(main_content)} characters")
print(f"   Scripts: {len(scripts)} characters")
