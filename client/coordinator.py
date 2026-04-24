import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from client import A2AClient  # noqa: E402


ECHO_URL = os.environ.get("ECHO_URL", "http://localhost:8000")
REVERSE_URL = os.environ.get("REVERSE_URL", "http://localhost:8001")


def run_chain(input_text: str) -> str:
    with A2AClient(ECHO_URL) as echo_client:
        echo_card = echo_client.fetch_agent_card()
        print(f"[Coordinator] EchoAgent   : {echo_card['name']}")

        echo_resp = echo_client.send_task(input_text)
        echoed = A2AClient.extract_text(echo_resp)
        print(f"[Coordinator] Echo output : {echoed!r}")

    with A2AClient(REVERSE_URL) as rev_client:
        rev_card = rev_client.fetch_agent_card()
        print(f"[Coordinator] ReverseAgent: {rev_card['name']}")

        rev_resp = rev_client.send_task(echoed)
        reversed_text = A2AClient.extract_text(rev_resp)
        print(f"[Coordinator] Final output: {reversed_text!r}")

    return reversed_text


def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello World"
    print(f"\nInput : {text!r}")
    result = run_chain(text)
    print(f"Result: {result!r}")


if __name__ == "__main__":
    main()
