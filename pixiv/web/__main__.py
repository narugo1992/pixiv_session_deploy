import json
import time
from contextlib import closing
from functools import partial

import click

from .browser import PixivBrowser
from ..utils import GLOBAL_CONTEXT_SETTINGS
from ..utils import print_version as _origin_print_version

print_version = partial(_origin_print_version, 'pixiv.web')


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Utils for pixiv web session.")
def cli():
    pass  # pragma: no cover


@cli.command('login', help='Login to pixiv web.',
             context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('--username', '-u', 'username', type=str, required=True,
              help='Username for pixiv.')
@click.option('--password', '-p', 'password', type=str, required=True,
              help='Password for pixiv.')
@click.option('--no-headless', 'no_headless', is_flag=True, default=False,
              help="Greet the world.", show_default=True)
@click.option('--slow-type', '-s', 'slow_type', is_flag=True, default=False,
              help='Slowly type the username and password', show_default=True)
@click.option('--output', '-o', 'output', type=click.Path(dir_okay=False), required=True,
              help='File to output the cookies data')
def login(username: str, password: str, no_headless: bool, slow_type: bool, output: str):
    headless = not no_headless
    browser = PixivBrowser(headless)
    with closing(browser):
        cookies, raw_cookies = browser.get_pixiv_cookie(username, password, slow_type)

    with open(output, 'w', encoding='utf-8') as f:
        json.dump({
            'cookies': cookies,
            'raw_cookies': raw_cookies,
            'username': username,
            'timestamp': time.time(),
        }, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    cli()  # pragma: no cover
