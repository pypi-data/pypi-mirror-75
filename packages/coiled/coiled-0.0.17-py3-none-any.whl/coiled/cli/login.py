import asyncio

import click

from .utils import CONTEXT_SETTINGS
from ..utils import handle_credentials


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-s", "--server", help="Coiled server to use")
def login(server):
    """ Configure your Coiled account credentials
    """
    try:
        asyncio.run(handle_credentials(server, save=True))
        print(
            '\nNext: see the "Run your first computation" guide at ... \n'
            "https://docs.coiled.io/getting_started.html#run-your-first-computation"
        )
    except ImportError as e:
        print(e)
