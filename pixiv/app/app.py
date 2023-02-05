from gppt import GetPixivToken


def get_refresh_token(username, password, headless: bool) -> str:
    app = GetPixivToken()
    retval = app.login(headless, username, password)
    return retval['refresh_token']
