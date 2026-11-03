"""First Draw account navigation and recoverable HTML boundary checks."""

import re
from urllib.parse import urlencode

import pytest

from app import database

DISPOSABLE_PASSWORD = "only for an isolated account test"


def form_token(client, path):
    """Read the token a normal browser form receives."""
    page = client.get(path)
    return re.search(r'name="csrf_token" value="([^"]+)"', page.text).group(1)


def signed_in_member(client):
    """Use actual HTML handlers and isolated fixture data for a signed-in state."""
    credentials = {"username": "first_draw_tester", "password": DISPOSABLE_PASSWORD}
    response = client.post(
        "/signup",
        data={**credentials, "csrf_token": form_token(client, "/signup")},
        follow_redirects=False,
    )
    assert response.status_code == 303
    response = client.post(
        "/login",
        data={**credentials, "csrf_token": form_token(client, "/login")},
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_navigation_follows_login_and_logout(client):
    """The learner's top-right entry changes with real session state."""
    assert ">Sign in</a>" in client.get("/").text
    signed_in_member(client)
    home = client.get("/").text
    assert ">My dashboard</a>" in home
    assert ">Sign in</a>" not in home
    dashboard = client.get("/dashboard")
    assert "first_draw_tester" in dashboard.text
    for path in ("/signup", "/login"):
        assert (
            client.get(path, follow_redirects=False).headers["location"] == "/dashboard"
        )
    response = client.post(
        "/logout",
        data={"csrf_token": form_token(client, "/dashboard")},
        follow_redirects=False,
    )
    assert response.headers["location"] == "/login"
    assert ">Sign in</a>" in client.get("/").text
    assert (
        client.get("/dashboard", follow_redirects=False).headers["location"] == "/login"
    )


def test_bad_logout_does_not_end_valid_session(client):
    """GET and forged form requests cannot silently log the member out."""
    signed_in_member(client)
    assert client.get("/logout").status_code == 405
    rejected = client.post("/logout", data={"csrf_token": "wrong"})
    assert rejected.status_code == 403
    assert 'role="alert"' in rejected.text
    assert client.get("/api/me").status_code == 200
    token = form_token(client, "/dashboard")
    assert client.post("/logout", data={"csrf_token": token}).status_code == 200
    assert client.get("/api/me").status_code == 401


@pytest.mark.parametrize("case", ["role", "duplicate", "oversized", "invalid"])
def test_bad_signup_forms_never_create_a_user(client, settings, case):
    """Reject role input, ambiguous fields, oversized bodies and invalid values."""
    values = {
        "username": "test_member",
        "password": DISPOSABLE_PASSWORD,
        "csrf_token": form_token(client, "/signup"),
    }
    expected = 422
    if case == "role":
        values["role"] = "admin"
    elif case == "invalid":
        values["username"] = "x"
    elif case == "oversized":
        values["password"] = "x" * 9000
        expected = 413
    body = urlencode(values)
    if case == "duplicate":
        body += "&username=another_member"
    response = client.post(
        "/signup",
        content=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == expected
    assert 'role="alert"' in response.text
    assert DISPOSABLE_PASSWORD not in response.text
    with database.connect(settings) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
