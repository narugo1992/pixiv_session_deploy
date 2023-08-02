import json
import os.path
import time
from contextlib import closing
from functools import partial

import click

from .app import get_refresh_token
from .utils import GLOBAL_CONTEXT_SETTINGS
from .utils import print_version as _origin_print_version
from .web.browser import PixivBrowser

print_version = partial(_origin_print_version, 'pixiv.web')


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Utils for pixiv web and app session.")
def cli():
    pass  # pragma: no cover


@cli.command('login', help='Login to pixiv web and app.',
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

    click.echo(click.style('Login into pixiv web ...', fg='green'))
    with closing(browser):
        cookies = browser.get_pixiv_cookie(username, password, slow_type)

    click.echo(click.style('Login into pixiv app ...', fg='green'))
    refresh_token = get_refresh_token(username, password, headless)

    with open(output, 'w', encoding='utf-8') as f:
        json.dump({
            'cookies': cookies,
            'refresh_token': refresh_token,
            'username': username,
            'timestamp': time.time(),
        }, f, indent=4, ensure_ascii=False)


@cli.command('batch', help='Batch login to pixiv web and app.',
             context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('--no-headless', 'no_headless', is_flag=True, default=False,
              help="Greet the world.", show_default=True)
@click.option('--slow-type', '-s', 'slow_type', is_flag=True, default=False,
              help='Slowly type the username and password', show_default=True)
@click.option('--output_dir', '-d', 'output_dir', type=click.Path(file_okay=False), required=True,
              help='Directory for outputting.', show_default=True)
@click.option('--index', '-i', 'index_filename', type=str, default='index.json',
              help='Index file in outputting directory.', show_default=True)
def batch(no_headless: bool, slow_type: bool, output_dir: str, index_filename: str):
    try:
        from accounts import DOWNLOAD_URL_TEMPLATE, PIXIV_ACCOUNTS
    except ImportError:
        raise ImportError('accounts.py should be placed, see accounts.py.sample for details.')

    os.makedirs(output_dir, exist_ok=True)
    session_files = []
    for (username, password), session_name in PIXIV_ACCOUNTS:
        session_file = f'{session_name}.json'

        headless = not no_headless
        browser = PixivBrowser(headless)

        click.echo(click.style(f'Login into pixiv web for {username!r} ...', fg='green'))
        with closing(browser):
            cookies = browser.get_pixiv_cookie(username, password, slow_type)

        click.echo(click.style(f'Login into pixiv app for {username!r} ...', fg='green'))
        refresh_token = get_refresh_token(username, password, headless)

        with open(os.path.join(output_dir, session_file), 'w', encoding='utf-8') as f:
            json.dump({
                'cookies': cookies,
                'refresh_token': refresh_token,
                'username': username,
                'timestamp': time.time(),
            }, f, indent=4, ensure_ascii=False)

        session_files.append(session_file)

    index_path = os.path.join(output_dir, index_filename)
    index_dir, _ = os.path.split(index_path)
    if index_dir:
        os.makedirs(index_dir, exist_ok=True)
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(session_files, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    cli()  # pragma: no cover
