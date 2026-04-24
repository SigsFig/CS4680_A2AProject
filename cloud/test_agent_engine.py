import sys

import vertexai
from vertexai.preview import reasoning_engines

PROJECT_ID = 'a2a-lab-nhoang'
REGION = "us-central1"

if len(sys.argv) < 2:
    print("Usage: python test_agent_engine.py <ENGINE_ID>")
    sys.exit(1)

ENGINE_ID = sys.argv[1]
RESOURCE_NAME = (
    f"projects/{PROJECT_ID}/locations/{REGION}"
    f"/reasoningEngines/{ENGINE_ID}"
)

vertexai.init(project=PROJECT_ID, location=REGION)

agent = reasoning_engines.ReasoningEngine(RESOURCE_NAME)

print(f"Calling Agent Engine: {RESOURCE_NAME}")
response = agent.query(message_text="Hello from Agent Engine!")
print("Response:", response)

response2 = agent.query(message_text="!summarise This is a test document.")
print("Summarise response:", response2)
