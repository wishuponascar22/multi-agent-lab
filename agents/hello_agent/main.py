from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Temporary identity registry (later replaced by RealAgentID Core)
AGENT_ID = "agent-hello-001"
PERMISSIONS = ["say_hello"]

@app.middleware("http")
async def identity_middleware(request: Request, call_next):
    # Extract identity header
    incoming_id = request.headers.get("X-RealAgentID")
    if incoming_id != AGENT_ID:
        raise HTTPException(status_code=401, detail="Invalid or missing RealAgentID")

    # Extract permission header
    incoming_perm = request.headers.get("X-RealAgent-Permission")
    if incoming_perm not in PERMISSIONS:
        raise HTTPException(status_code=403, detail="Permission denied")

    return await call_next(request)

@app.get("/hello")
def hello():
    return {"message": "Hello, I am a governed agent with RealAgentID."}
