# CS4680 A2A Lab — Report

## Section 3:

### Q26

If the network drops after sending a request, the client doesn't know if the server ran it. Since the client picked the ID, it can safely resend with the same ID and a server that caches by ID will return the cached result instead of running it again. Server-generated IDs would need an extra round-trip and still have the same problem.

### Q27

When a task takes too long and the server can't finish before a gateway timeout (e.g. a slow LLM call). The client should poll `GET /tasks/{id}` with backoff and not resend the task since it may still be running.

### Q28

Groups related tasks so the server can maintain context across them.

Example — two follow-up questions to a doc Q&A agent:
- Task 1: `{"id": "t-001", "sessionId": "sess-abc", "message": {"parts": [{"text": "What is the total revenue in Q3?"}]}}`
- Task 2: `{"id": "t-002", "sessionId": "sess-abc", "message": {"parts": [{"text": "How does that compare to Q2?"}]}}`

Task 2 is only answerable using Task 1's result. The shared `sessionId` tells the server to look up that context.

### Q29
A realistic multi-agent workflow could be as follows:
1. **User → IngestAgent** — `file` part (PDF) + `text` part (instructions)
2. **IngestAgent → SummaryAgent** — `text` part (extracted body) + `data` part (metadata like page count, DOI)
3. **SummaryAgent → User** — `text` part (summary) + `data` part (citation info)

---

## Section 4:

### (a)

This would make the service fully public (no token needed) and grants `roles/run.invoker` to `allUsers`. 

### (b)

Cloud Run shuts down idle containers after ~15 minutes. The next request has to pull the image and start the container, which takes 2–10 seconds. Fixes:
- `--min-instances=1` to keep one instance warm
- Send a `/health` ping first to absorb the cold start

---

## Section 5:

### (a)

Cloud Run gives you full control to manage the Dockerfile, server, and routing, which works for any language but takes more effort. Agent Engine is higher-level: you just implement `set_up()` and `query()` and Google handles packaging and deployment. Cloud Run requires manual logging setup while Agent Engine has built-in traces in the Vertex AI console. You should use Cloud Run when you need custom networking or aren't using Python, while you should use Agent Engine when you want to ship a Python agent fast without dealing with infrastructure.

### (b)

Agent Engine calls `query()` as a plain sync function — returning a coroutine would break it. `asyncio.run(handle_task(...))` creates a temporary event loop, runs the coroutine, and returns the result as a plain value.

---

## Section 6:

### Log output

```
[A2AClient] GET https://echo-a2a-agent-92609386701.us-central1.run.app/.well-known/agent.json
[A2AClient] Card received: {'id': 'echo-agent-v1', 'name': 'Echo Agent', 'version': '1.0.0', 'description': 'A simple agent that echoes back any text it receives.', 'url': 'https://echo-a2a-agent-92609386701.us-central1.run.app...

Agent name : Echo Agent
Agent ID   : echo-agent-v1
Agent URL  : https://echo-a2a-agent-92609386701.us-central1.run.app

Skills (2):
  - echo: Returns the user message verbatim.
  - summarise: Returns a one-sentence summary of the provided text.

Sending task: 'Hello from the client!'
[A2AClient] POST https://echo-a2a-agent-92609386701.us-central1.run.app/tasks/send
[A2AClient] Payload: {'id': 'c414dd18-f993-4f96-b4c6-36fceda5780d', 'sessionId': None, 'message': {'role': 'user', 'parts': [{'type': 'text', 'text': 'Hello from the client!'}]}}
[A2AClient] Response: {'id': 'c414dd18-f993-4f96-b4c6-36fceda5780d', 'status': {'state': 'completed'}, 'artifacts': [{'parts': [{'type': 'text', 'text': 'Hello from the client!'}]}]}
Echo response: Hello from the client!

Sending summarise task: '!summarise This is a long text.'
[A2AClient] POST https://echo-a2a-agent-92609386701.us-central1.run.app/tasks/send
[A2AClient] Payload: {'id': 'a9350bd4-a0b9-4123-954d-1b3a555da7e5', 'sessionId': None, 'message': {'role': 'user', 'parts': [{'type': 'text', 'text': '!summarise This is a long text.'}]}}
[A2AClient] Response: {'id': 'a9350bd4-a0b9-4123-954d-1b3a555da7e5', 'status': {'state': 'completed'}, 'artifacts': [{'parts': [{'type': 'text', 'text': 'This text discusses a topic and presents key ideas concisely.'}]}]}
Summary response: This text discusses a topic and presents key ideas concisely.
```

### Q46 

1. Wait a short backoff period
2. Resend the exact same payload with the same `id`
3. The server returns the cached result if it already ran the task

The `id` field makes this safe, since the client generates it, the same UUID can be reused on every retry.

---

## Section 7:

### (a)

Each Cloud Run service should require an OIDC token. The coordinator fetches one and passes it as a header:

```python
import google.auth.transport.requests
import google.oauth2.id_token

def get_id_token(audience: str) -> str:
    request = google.auth.transport.requests.Request()
    return google.oauth2.id_token.fetch_id_token(request, audience)

headers = {"Authorization": f"Bearer {get_id_token(self.agent_url)}"}
resp = self._http.post(url, json=payload, headers=headers)
```

Each service account only gets `roles/run.invoker` on the specific service it calls — least privilege.

### (b) 

The schema already supports it. The coordinator generates one UUID and passes it to every agent:

```python
session_id = str(uuid.uuid4())
echo_resp = echo_client.send_task(text,   session_id=session_id)
rev_resp  = rev_client.send_task(echoed,  session_id=session_id)
```

For shared state across agents, each would look up a store like Firestore keyed by `sessionId`.
