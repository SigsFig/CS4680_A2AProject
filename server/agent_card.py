# server/agent_card.py
AGENT_CARD = {
    'id': 'echo-agent-v1',
    'name': 'Echo Agent',
    'version': '1.0.0',
    'description': 'A simple agent that echoes back any text it receives.',
    'url': 'https://echo-a2a-agent-92609386701.us-central1.run.app',  # updated at deploy time  # noqa: E501
    'capabilities': {
        'streaming': False,
        'pushNotifications': False
    },
    'defaultInputModes': ['text/plain'],
    'defaultOutputModes': ['text/plain'],
    'skills': [
        {
            'id': 'echo',
            'name': 'Echo',
            'description': 'Returns the user message verbatim.',
            'inputModes': ['text/plain'],
            'outputModes': ['text/plain']
        },
        {
            'id': 'summarise',
            'name': 'Summarise',
            'description': 'Returns a one-sentence summary of the provided text.',
            'inputModes': ['text/plain'],
            'outputModes': ['text/plain']
        }
    ],
    'contact': {
        'email': 'agent-admin@example.com'
    }
}


def validate_card(card: dict) -> bool:
    '''Return True if all required Agent Card fields are present.'''
    required = {'id', 'name', 'version', 'description', 'url',
                'capabilities', 'defaultInputModes', 'defaultOutputModes',
                'skills'}
    return required.issubset(card.keys())
