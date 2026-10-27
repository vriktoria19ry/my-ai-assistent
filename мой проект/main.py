with GigaChat(
    credentials=key,
    scope=scope,
    model="GigaChat-2",
    verify=False,
    timeout=60,
    allow_unsafe_connections=True
) as client:
    response = client.chat.create(request)