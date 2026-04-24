# server/handlers.py
async def handle_task(request) -> str:
    text_parts = [p.text for p in request.message.parts if p.type == 'text']
    combined = ' '.join(text_parts)

    if combined.split() and combined.split()[0] == '!summarise':
        return 'This text discusses a topic and presents key ideas concisely.'

    # ECHO skill: return the input unchanged
    return combined
