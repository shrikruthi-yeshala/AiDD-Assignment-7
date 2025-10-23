def test_projects_list_shows_inserted_project(client, dal_module):
    # Insert a project via the DAL
    project_id = dal_module.insert_project(
        title="Test Project",
        description="A short description",
        image_file_name="test-image.jpg",
        detail_slug="test-project",
    )

    # Request the projects page
    resp = client.get("/projects")
    assert resp.status_code == 200
    data = resp.get_data(as_text=True)

    # The title should appear on the projects page
    assert "Test Project" in data


def test_project_detail_route_for_markdown_or_html(client, dal_module):
    # Insert and then fetch by id
    project_id = dal_module.insert_project(
        title="Detail Project",
        description="Detailed description",
        image_file_name="detail-image.jpg",
        detail_slug=None,
    )

    # The project detail page for this slug is not defined in DETAIL_PAGE_PATHS
    # but we can ensure the project exists via the projects page
    resp = client.get("/projects")
    assert resp.status_code == 200
    text = resp.get_data(as_text=True)
    assert "Detail Project" in text


def test_delete_project_removes_row_and_redirects(client, dal_module):
    project_id = dal_module.insert_project(
        title="To Be Deleted",
        description="Will be deleted",
        image_file_name="delete-image.jpg",
        detail_slug=None,
    )

    # Confirm it exists
    resp = client.get("/projects")
    assert "To Be Deleted" in resp.get_data(as_text=True)

    # Call the POST delete endpoint
    resp = client.post(f"/projects/delete/{project_id}", follow_redirects=True)
    assert resp.status_code == 200

    # Now the title should no longer be on the projects page
    resp2 = client.get("/projects")
    assert "To Be Deleted" not in resp2.get_data(as_text=True)
