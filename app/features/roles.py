"""APP-003: enforce current admin permission for page and API requests."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from app import security

router = APIRouter()


@router.get("/api/admin", dependencies=[Depends(security.require_admin)])
def admin_api():
    """Only a currently authorized administrator receives this result."""
    return {"detail": "Welcome to First Draw administration."}


@router.get("/admin", include_in_schema=False)
def admin_page(request: Request):
    """Offer login to visitors and a helpful 403 page to ordinary members."""
    try:
        security.require_admin(request)
    except HTTPException as failure:
        if failure.status_code == 401:
            return RedirectResponse("/login", status_code=303)
        if failure.status_code != 403:
            raise
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="admin.html",
            context={"allowed": False},
            status_code=403,
        )
    return request.app.state.templates.TemplateResponse(
        request=request, name="admin.html", context={"allowed": True}
    )
