"""APP-002: shared account services behind HTML forms and JSON endpoints."""

from urllib.parse import parse_qsl

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from app import security
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()


def _api_csrf(request: Request):
    """Guard every state-changing JSON request using its session token."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))


def _create_member(request: Request, credentials: SignupInput):
    """Share signup limits and member-only creation across both entry points."""
    security.limit_signup(request)
    return security.signup(
        request.app.state.settings, credentials.username, credentials.password
    )


def _page(request: Request, name: str, context=None, status_code=200):
    """Render a form with a session-bound CSRF token and no password echo."""
    cookie_response = Response()
    values = dict(context or {})
    values["csrf_token"] = security.csrf_token(request, cookie_response)
    response = request.app.state.templates.TemplateResponse(
        request=request, name=name, context=values, status_code=status_code
    )
    for key, value in cookie_response.raw_headers:
        if key.lower() == b"set-cookie":
            response.raw_headers.append((key, value))
    return response


async def _form_data(request: Request):
    """Bound these small URL-encoded forms before parsing or password hashing."""
    content_type = request.headers.get("content-type", "").split(";", 1)[0]
    if content_type != "application/x-www-form-urlencoded":
        raise HTTPException(415, "Use the form on this page to continue.")
    body = bytearray()
    async for chunk in request.stream():
        if len(body) + len(chunk) > 8192:
            raise HTTPException(413, "The form is too large. Please try again.")
        body.extend(chunk)
    try:
        pairs = parse_qsl(
            body.decode("utf-8"),
            keep_blank_values=True,
            max_num_fields=3,
            errors="strict",
        )
    except (UnicodeError, ValueError) as error:
        raise HTTPException(422, "Check the form fields and try again.") from error
    values = dict(pairs)
    if len(values) != len(pairs):
        raise HTTPException(422, "Send each form field only once.")
    security.require_csrf(request, values.pop("csrf_token", None))
    return values


@router.get("/api/csrf")
def api_csrf(request: Request, response: Response):
    """Start or reuse a pre-login session without exposing its cookie value."""
    return {"csrf_token": security.csrf_token(request, response)}


@router.post(
    "/api/signup",
    response_model=PublicUser,
    status_code=201,
    dependencies=[Depends(_api_csrf)],
)
def api_signup(request: Request, credentials: SignupInput):
    """Create a regular member from validated credentials."""
    return _create_member(request, credentials)


@router.post("/api/login", response_model=PublicUser, dependencies=[Depends(_api_csrf)])
def api_login(request: Request, response: Response, credentials: LoginInput):
    """Authenticate and set the prepared HttpOnly session cookie."""
    return security.login(request, response, credentials.username, credentials.password)


@router.get("/api/me", response_model=PublicUser)
def api_me(request: Request):
    """Return public identity only when the server session is still valid."""
    return security.require_user(request)


@router.post("/api/logout", dependencies=[Depends(_api_csrf)])
def api_logout(request: Request, response: Response):
    """Invalidate the server session as well as clearing the browser cookie."""
    security.require_user(request)
    security.logout(request, response)
    return {"detail": "Logged out."}


@router.get("/signup", include_in_schema=False)
def signup_page(request: Request):
    """Offer signup to visitors who are not already signed in."""
    if security.authenticate(request):
        return RedirectResponse("/dashboard", status_code=303)
    return _page(request, "account.html", {"signup": True})


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    """Offer a fresh login form, including after signup or logout."""
    if security.authenticate(request):
        return RedirectResponse("/dashboard", status_code=303)
    return _page(request, "account.html", {"signup": False})


async def _submit_account(request: Request, signup: bool):
    """Keep HTML errors recoverable while reusing validated account services."""
    username = ""
    try:
        values = await _form_data(request)
        schema = SignupInput if signup else LoginInput
        credentials = schema.model_validate(values)
        username = credentials.username
        if signup:
            await run_in_threadpool(_create_member, request, credentials)
            return RedirectResponse("/login", status_code=303)
        response = RedirectResponse("/dashboard", status_code=303)
        await run_in_threadpool(
            security.login, request, response, username, credentials.password
        )
        return response
    except ValidationError:
        error = "Check the username and password requirements below."
        status = 422
        headers = {}
    except HTTPException as failure:
        error = failure.detail
        status = failure.status_code
        headers = failure.headers or {}
    response = _page(
        request,
        "account.html",
        {"signup": signup, "username": username, "error": error},
        status_code=status,
    )
    response.headers.update(headers)
    return response


@router.post("/signup", include_in_schema=False)
async def signup_form(request: Request):
    """Create an account, then invite the visitor to log in."""
    return await _submit_account(request, signup=True)


@router.post("/login", include_in_schema=False)
async def login_form(request: Request):
    """Send a successful login to the private dashboard."""
    return await _submit_account(request, signup=False)


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request):
    """Enforce access on direct visits, not merely through navigation links."""
    user = security.authenticate(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return _page(request, "dashboard.html", {"user": user})


@router.post("/logout", include_in_schema=False)
async def logout_form(request: Request):
    """Reject unsafe logout requests and revoke successful ones server-side."""
    try:
        values = await _form_data(request)
        if values:
            raise HTTPException(422, "Use the Log out button to continue.")
        security.require_user(request)
    except HTTPException as failure:
        user = security.authenticate(request)
        template = "dashboard.html" if user else "account.html"
        return _page(
            request,
            template,
            {"user": user, "signup": False, "error": failure.detail},
            status_code=failure.status_code,
        )
    response = RedirectResponse("/login", status_code=303)
    security.logout(request, response)
    return response
