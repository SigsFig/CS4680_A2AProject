# server_reverse/handlers.py
async def handle_task(request) -> str:
    text_parts = [p.text for p in request.message.parts if p.type == 'text']
    combined = ' '.join(text_parts)

    # REVERSE skill: return the words in reverse order
    return ' '.join(reversed(combined.split()))
