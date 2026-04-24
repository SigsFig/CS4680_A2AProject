"""End-to-end demo: discover the Echo Agent, send a task, print the result."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from client import A2AClient  # noqa: E402

AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:8000")


def main():
    with A2AClient(AGENT_URL) as client:
        card = client.fetch_agent_card()
        print(f"\nAgent name : {card['name']}")
        print(f"Agent ID   : {card['id']}")
        print(f"Agent URL  : {card['url']}")

        skills = client.get_skills()
        print(f"\nSkills ({len(skills)}):")
        for skill in skills:
            print(f"  - {skill['id']}: {skill['description']}")

        print("\nSending task: 'Hello from the client!'")
        response = client.send_task("Hello from the client!")
        result = A2AClient.extract_text(response)
        print(f"Echo response: {result}")

        print("\nSending summarise task: '!summarise This is a long text.'")
        response2 = client.send_task("!summarise This is a long text.")
        result2 = A2AClient.extract_text(response2)
        print(f"Summary response: {result2}")


if __name__ == "__main__":
    main()
