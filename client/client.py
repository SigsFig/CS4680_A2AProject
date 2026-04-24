# client/client.py
import httpx
import uuid
from typing import Optional


class A2AClient:
    """Minimal A2A-compliant client."""

    def __init__(self, agent_url: str):
        self.agent_url = agent_url.rstrip('/')
        self._card = None      # cached Agent Card
        self._http = httpx.Client(timeout=30)

    # ── 1. Discovery ─────────────────────────────────────────────────
    def fetch_agent_card(self) -> dict:
        """Fetch and cache the Agent Card."""
        if self._card is None:
            url = f'{self.agent_url}/.well-known/agent.json'
            print(f'[A2AClient] GET {url}')
            resp = self._http.get(url)
            resp.raise_for_status()
            self._card = resp.json()
            print(f'[A2AClient] Card received: {str(self._card)[:200]}...')
        return self._card

    def get_skills(self) -> list:
        """Return the skills list from the cached Agent Card."""
        return self.fetch_agent_card().get('skills', [])

    # ── 2. Request Construction ───────────────────────────────────────
    def _build_task(self, text: str,
                    task_id: Optional[str] = None,
                    session_id: Optional[str] = None) -> dict:
        """Build a conformant A2A task payload."""
        return {
            'id': task_id or str(uuid.uuid4()),
            'sessionId': session_id,
            'message': {
                'role': 'user',
                'parts': [{'type': 'text', 'text': text}]
            }
        }

    # ── 3. Send & Parse ──────────────────────────────────────────────
    def send_task(self, text: str, **kwargs) -> dict:
        """Send a task and return the parsed response."""
        self.fetch_agent_card()  # ensure card is cached
        payload = self._build_task(text, **kwargs)
        url = f'{self.agent_url}/tasks/send'
        print(f'[A2AClient] POST {url}')
        print(f'[A2AClient] Payload: {str(payload)[:200]}')
        resp = self._http.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        print(f'[A2AClient] Response: {str(data)[:200]}')
        state = data.get('status', {}).get('state')
        if state != 'completed':
            raise RuntimeError(
                f"Task did not complete successfully. State: {state!r}"
            )
        return data

    # ── 4. Helper: extract result text ───────────────────────────────
    @staticmethod
    def extract_text(response: dict) -> str:
        """Pull the first text part from artifacts."""
        artifacts = response.get('artifacts', [])
        for artifact in artifacts:
            for part in artifact.get('parts', []):
                if part.get('type') == 'text':
                    return part['text']
                if part.get('type') == 'file':
                    return part.get('url', '')
        return ''

    # ── 5. Lifecycle ─────────────────────────────────────────────────
    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
