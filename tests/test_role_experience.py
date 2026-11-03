"""First Draw's recovery link and live role-aware navigation."""

from app import database


def sign_in(client):
    """Create a disposable member in the isolated request-test database."""
    credentials = {"username": "role_tester", "password": "disposable role test phrase"}
    token = client.get("/api/csrf").json()["csrf_token"]
    headers = {"X-CSRF-Token": token}
    assert (
        client.post("/api/signup", json=credentials, headers=headers).status_code == 201
    )
    assert (
        client.post("/api/login", json=credentials, headers=headers).status_code == 200
    )


def test_denied_page_offers_home_without_admin_content(client):
    """A direct request returns a real denial plus the learner's recovery link."""
    sign_in(client)
    denied = client.get("/admin")
    assert denied.status_code == 403
    assert "Your member account does not have access to this page." in denied.text
    assert 'href="/">Return to homepage' in denied.text
    assert "Welcome to the First Draw admin space." not in denied.text
    assert client.get("/").status_code == 200
    assert client.get("/dashboard").status_code == 200


def test_navigation_and_access_follow_role_changes_without_relogin(client, settings):
    """An existing session gains and loses both admin access and navigation."""
    sign_in(client)
    assert 'href="/admin"' not in client.get("/").text
    assert database.set_role(settings, "role_tester", "admin")
    assert 'href="/admin"' in client.get("/").text
    assert "Welcome to the First Draw admin space." in client.get("/admin").text
    assert client.get("/api/admin").json() == {
        "detail": "Welcome to First Draw administration."
    }
    assert database.set_role(settings, "role_tester", "member")
    assert 'href="/admin"' not in client.get("/").text
    assert client.get("/admin").status_code == 403
    assert client.get("/api/admin").status_code == 403
    assert client.get("/dashboard").status_code == 200
