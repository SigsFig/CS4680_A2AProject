# server_reverse/agent_card.py
AGENT_CARD = {
    'id': 'reverse-agent-v1',
    'name': 'Reverse Agent',
    'version': '1.0.0',
    'description': 'An agent that returns the words of the input in reverse order.',
    'url': 'http://localhost:8001',  # updated at deploy time
    'capabilities': {
        'streaming': False,
        'pushNotifications': False
    },
    'defaultInputModes': ['text/plain'],
    'defaultOutputModes': ['text/plain'],
    'skills': [
        {
            'id': 'reverse',
            'name': 'Reverse',
            'description': 'Returns input words in reverse order.',
            'inputModes': ['text/plain'],
            'outputModes': ['text/plain']
        }
    ],
    'contact': {
        'email': 'agent-admin@example.com'
    }
}


def validate_card(card: dict) -> bool:
    """Return True if all required Agent Card fields are present."""
    required = {'id', 'name', 'version', 'description', 'url',
                'capabilities', 'defaultInputModes', 'defaultOutputModes',
                'skills'}
    return required.issubset(card.keys())
