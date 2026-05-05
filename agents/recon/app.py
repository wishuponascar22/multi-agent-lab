import os
import json
import time
import redis
import sys
sys.stdout.reconfigure(line_buffering=True)

# Load environment variables
agent_id = os.getenv("AGENT_ID")
redis_host = os.getenv("REDIS_HOST", "redis")
config_path = os.getenv("REALAGENTID_CONFIG", "/opt/realagentid/agents.json")

# Connect to Redis
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# Load RealAgentID policy
with open(config_path, "r") as f:
    REALAGENTID = json.load(f)

def verify_permission(action):
    """Check if this agent is allowed to perform the action."""
    agent = REALAGENTID.get(agent_id, {})
    allowed = agent.get("permissions", [])
    denied = agent.get("denied", [])

    if action in denied:
        return False

    return action in allowed

def register():
    """Announce this agent to the orchestrator."""
    info = {"agent_id": agent_id}
    r.publish("agent_register", json.dumps(info))
    print(f"[REGISTER] {agent_id}")

def main_loop():
    """Main task loop."""
    queue_name = f"queue:{agent_id}"

    print(f"[STARTED] {agent_id} is running...")

    while True:
        task_json = r.rpop(queue_name)

        if not task_json:
            time.sleep(0.5)
            continue

        task = json.loads(task_json)
        action = task.get("action")

        if not verify_permission(action):
            print(f"[DENIED] {agent_id} cannot perform action: {action}")
            continue

        print(f"[TASK RECEIVED] {agent_id} executing: {action}")

        # Placeholder for actual agent logic
        time.sleep(1)

        print(f"[DONE] {agent_id} completed: {action}")

if __name__ == "__main__":
    register()
    main_loop()
