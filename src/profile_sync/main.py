
from fastapi import FastAPI

from profile_sync.config import Settings
from profile_sync.presentation.api.routers.imports import router


def create_app() -> FastAPI:

    settings = Settings()

    swagger_enabled = (
        settings.SWAGGER_ENABLED
        and settings.APP_ENVIRONMENT.lower() == "development"
    )

    app = FastAPI(
        title="Profile Synchronization Service",
        description=(
            "Secure AI-assisted Screening Sheet "
            "and Participant Profile Synchronization API"
        ),
        version="0.1.0",
        docs_url="/swagger" if swagger_enabled else None,
        redoc_url="/redoc" if swagger_enabled else None,
        openapi_url="/openapi.json" if swagger_enabled else None,
        swagger_ui_parameters={
            "persistAuthorization": False,
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
        },
    )

    @app.get("/health/live", tags=["Health"])
    async def live():
        return {"status": "healthy"}

    app.include_router(router)

    return app


app = create_app()
