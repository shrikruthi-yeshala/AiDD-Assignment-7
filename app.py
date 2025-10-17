from __future__ import annotations

import os
from pathlib import Path
from werkzeug.utils import secure_filename

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from DAL import delete_project, fetch_all_projects, fetch_project_by_id, initialize_database, insert_project

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-me-with-env-secret"
app.config["UPLOAD_FOLDER"] = Path(app.root_path) / "static" / "images"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max file size
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

initialize_database()


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


DETAIL_PAGE_PATHS = {
    "employee-productivity": "productivity-sheet.html",  # Interactive productivity sheet
    "servicenow-ai": "projects/servicenow-ai-documentation.html",
    "servicenow-platform": "projects/servicenow-documentation.html",
    "powerbi-dashboard": "projects/powerbi-dashboard.html",
    "sap-enterprise": "projects/sap-enterprise-documentation.html",
}


def _load_markdown(relative_path: str) -> tuple[str, str]:
    """Return markdown string and inferred title for project detail page."""

    markdown_path = Path(app.root_path, "templates", relative_path)
    try:
        markdown_text = markdown_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        abort(404)

    page_title = "Project Documentation"
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            page_title = stripped.lstrip("#").strip() or page_title
            break

    return markdown_text, page_title


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/resume")
def resume() -> str:
    return render_template("resume.html")


@app.route("/projects")
def projects() -> str:
    project_rows = fetch_all_projects()
    return render_template("projects.html", projects=project_rows)


@app.route("/projects/new", methods=["GET", "POST"])
def contact() -> str:
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        image_file_name = request.form.get("image_file_name", "").strip()
        detail_slug = request.form.get("detail_slug", "").strip()
        
        # Handle file upload
        uploaded_file = request.files.get("image_upload")
        
        # Determine the final image filename
        final_image_name = None
        
        if uploaded_file and uploaded_file.filename:
            # User uploaded a file
            if allowed_file(uploaded_file.filename):
                # Secure the filename and save
                filename = secure_filename(uploaded_file.filename)
                
                # Ensure upload folder exists
                app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
                
                # Save the file
                file_path = app.config["UPLOAD_FOLDER"] / filename
                uploaded_file.save(str(file_path))
                
                final_image_name = filename
                flash(f"Image '{filename}' uploaded successfully!", "success")
            else:
                flash("Invalid file type. Please upload JPG, PNG, or GIF.", "error")
                return render_template(
                    "contact.html",
                    form_data={
                        "title": title,
                        "description": description,
                        "image_file_name": image_file_name,
                        "detail_slug": detail_slug,
                    },
                )
        elif image_file_name:
            # User entered an existing filename
            final_image_name = image_file_name
        else:
            # Neither upload nor filename provided
            flash("Please either upload an image or enter an existing image filename.", "error")
            return render_template(
                "contact.html",
                form_data={
                    "title": title,
                    "description": description,
                    "image_file_name": image_file_name,
                    "detail_slug": detail_slug,
                },
            )

        # Validate required fields
        if not title or not description:
            flash("Title and description are required.", "error")
            return render_template(
                "contact.html",
                form_data={
                    "title": title,
                    "description": description,
                    "image_file_name": final_image_name,
                    "detail_slug": detail_slug,
                },
            )

        # Insert the project
        insert_project(
            title=title,
            description=description,
            image_file_name=final_image_name,
            detail_slug=detail_slug or None,
        )
        flash("Project added successfully!", "success")
        return redirect(url_for("projects"))

    return render_template("contact.html", form_data=None)


@app.route("/projects/delete/<int:project_id>", methods=["GET"])
def delete_confirmation(project_id: int) -> str:
    """Show delete confirmation page."""
    project = fetch_project_by_id(project_id)
    if not project:
        abort(404)
    return render_template("delete.html", project=project)


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def remove_project(project_id: int) -> str:
    delete_project(project_id)
    flash("Project removed.", "info")
    return redirect(url_for("projects"))


@app.route("/projects/docs/<slug>")
def project_detail(slug: str) -> str:
    relative_path = DETAIL_PAGE_PATHS.get(slug)
    if not relative_path:
        abort(404)

    # Check if the file exists
    template_path = Path(app.root_path, "templates", relative_path)
    if not template_path.exists():
        abort(404)

    # Handle markdown files
    if relative_path.endswith(".md"):
        markdown_content, page_title = _load_markdown(relative_path)
        return render_template(
            "project_detail.html",
            markdown_content=markdown_content,
            page_title=page_title,
        )

    # Handle HTML files - render them directly
    return render_template(relative_path)


if __name__ == "__main__":
    app.run(debug=True)
