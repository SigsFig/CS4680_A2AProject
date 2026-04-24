# CS4680 A2A Lab

Echo Agent built with FastAPI, deployed to Google Cloud Run.

**Live URL:** https://echo-a2a-agent-92609386701.us-central1.run.app

---

## File Structure

```
server/          - Echo Agent (FastAPI server)
server_reverse/  - Bonus: Reverse Agent
client/          - A2AClient + demo script + multi-agent coordinator
cloud/           - Deploy scripts for Cloud Run and Agent Engine
report.md        - Written answers
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install fastapi uvicorn httpx pydantic google-cloud-aiplatform google-auth requests
```

---

## Run Locally

```bash
# Terminal 1 - start server
cd server
uvicorn main:app --reload --port 8000

# Terminal 2 - run demo
python client/demo.py
```

Quick test:
```bash
curl http://localhost:8000/.well-known/agent.json
curl http://localhost:8000/health
```

---

## Deploy to Cloud Run

1. Set `PROJECT_ID` in `cloud/deploy_cloud_run.sh`
2. Run:
```bash
bash cloud/deploy_cloud_run.sh
```
3. Copy the printed URL, update `url` in `server/agent_card.py`, redeploy.

Run demo against live URL:
```bash
AGENT_URL=https://<SERVICE_URL> python client/demo.py
```

---

## Deploy to Agent Engine (Bonus)

```bash
gsutil mb -l us-central1 gs://<your-project-id>-a2a-staging
python cloud/deploy_agent_engine.py
python cloud/test_agent_engine.py <ENGINE_ID>
```

---

## Multi-Agent Chain (Bonus)

```bash
# Start both servers
cd server && uvicorn main:app --reload --port 8000
cd server_reverse && uvicorn main:app --reload --port 8001

# Run coordinator
ECHO_URL=http://localhost:8000 REVERSE_URL=http://localhost:8001 \
    python client/coordinator.py "Hello World"
```
