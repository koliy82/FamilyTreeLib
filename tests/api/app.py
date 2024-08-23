import uvicorn
from fastapi import FastAPI

from tests.api.router import router

app = FastAPI(
    title="[TEST] FamilyTree API",
    summary="API for build nodes from user_id and send image with family tree",
)

@app.get("/status")
def get_status():
    return {"status": "ok"}
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)