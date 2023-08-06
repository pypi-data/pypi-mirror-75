def get_metadata(locale, user=None):
    if user is None:
        user = {}
    return {
        "locale": locale,
        "user": {
            "id": user.get("id", None),
            "username": user.get("username", None)
        },
        "transaction": []
    }
