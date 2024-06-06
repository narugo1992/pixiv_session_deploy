from gppt import GetPixivToken


def get_refresh_token(username, password, headless: bool) -> str:
    app = GetPixivToken(headless=headless)
    retval = app.login(username=username, password=password)
    return retval['refresh_token']
