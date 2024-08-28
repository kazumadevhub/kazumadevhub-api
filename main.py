from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.convert import convert_router

app = FastAPI(
    title="KazumaDevHub APIs",
    description="Here you will find all the information you need to get started with our API.",
    version="1.0.0",
    docs_url="/swagger",  # Swagger UI documentation
    redoc_url=None,  # Disable ReDoc UI
    openapi_url="/static/openapi.json",  # OpenAPI schema path
)

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Register the router
app.include_router(convert_router)

# Root route
@app.get("/", summary="Root", tags=["Info"])
async def read_root():
    return {"message": "Visit /swagger for the API documentation."}