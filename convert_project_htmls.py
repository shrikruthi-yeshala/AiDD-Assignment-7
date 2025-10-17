"""Convert standalone project HTML files to Flask templates."""

from pathlib import Path

def convert_html_to_template(file_path: Path, title: str) -> None:
    """Convert a standalone HTML file to extend base.html."""
    
    content = file_path.read_text(encoding='utf-8')
    
    # Find the title
    title_start = content.find('<title>') + 7
    title_end = content.find('</title>')
    original_title = content[title_start:title_end] if title_start > 6 and title_end > 0 else title
    
    # Find the styles section
    style_start = content.find('<style>')
    style_end = content.find('</style>') + 8
    styles = content[style_start:style_end] if style_start >= 0 else ""
    
    # Find main content (between opening body and footer)
    body_start = content.find('<body>')
    if body_start < 0:
        print(f"Could not find <body> in {file_path.name}")
        return
    
    # Skip header/nav section
    nav_end = content.find('</header>')
    if nav_end < 0:
        nav_end = content.find('</nav>')
    
    main_start = content.find('<main', body_start)
    if main_start < 0:
        # If no <main>, look for first div after nav
        main_start = content.find('<div class="', nav_end if nav_end > 0 else body_start)
    else:
        # Skip the <main> tag itself
        main_start = content.find('>', main_start) + 1
    
    # Find where footer starts
    footer_start = content.find('<footer>')
    if footer_start < 0:
        footer_start = content.find('</main>')
    
    # Extract main content
    main_content = content[main_start:footer_start].strip()
    
    # Remove </main> if it exists at the end
    if main_content.endswith('</main>'):
        main_content = main_content[:-7].strip()
    
    # Build new template
    new_template = f"""{{% extends "base.html" %}}

{{% block title %}}{original_title}{{% endblock %}}

{{% block extra_css %}}
{styles}
{{% endblock %}}

{{% block content %}}
{main_content}
{{% endblock %}}
"""
    
    # Replace {{ with proper Flask syntax if needed (for back to projects link)
    new_template = new_template.replace('href="projects.html"', 'href="{{ url_for(\'projects\') }}"')
    
    # Write back
    file_path.write_text(new_template, encoding='utf-8')
    print(f"✅ Converted {file_path.name}")


if __name__ == "__main__":
    templates_dir = Path(__file__).parent / "templates" / "projects"
    
    files_to_convert = [
        ("servicenow-ai-documentation.html", "ServiceNow AI Documentation"),
        ("servicenow-documentation.html", "ServiceNow Documentation"),
        ("sap-enterprise-documentation.html", "SAP Enterprise Documentation"),
    ]
    
    for filename, title in files_to_convert:
        file_path = templates_dir / filename
        if file_path.exists():
            print(f"Converting {filename}...")
            convert_html_to_template(file_path, title)
        else:
            print(f"⚠️  File not found: {filename}")
    
    print("\n✨ Conversion complete!")
