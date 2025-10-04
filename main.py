from fastapi import FastAPI
from app.routers import assignments, ask

app = FastAPI(
    title="MCP Server",
    description="Backend server for Canvas AI Assistant",
    version="1.0.0"
)

# Register routers
app.include_router(assignments.router)
app.include_router(ask.router)

@app.get("/")
def root():
    return {"message": "MCP Server running 🚀"}
