import click

from cli.utils import Spotify
from cli.utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '-t', '--to', type=int, default=0,
    help='Set volume to <int> percent.',
    metavar='<int>'
)
@click.option(
    '-u', '--up', type=int, default=0,
    help='Increase volume by <int> percent.',
    metavar='<int>'
)
@click.option(
    '-d', '--down', type=int, default=0,
    help='Decrease volume by <int> percent.',
    metavar='<int>'
)
def volume(to, up, down):
    """Control the active device's volume level."""
    num_options = (bool(up) + bool(down) + bool(to))
    if num_options != 1:
        raise InvalidVolumeInput

    if to:
        new_volume = to
    else:
        from cli.commands.status import status
        device = status.callback(raw=True, verbose=-1).get('device')
        current_volume = device['volume_percent']
        new_volume = current_volume + up - down
        if new_volume > 100:
            new_volume = 100
        elif new_volume < 0:
            new_volume = 0


    Spotify.request(
        'me/player/volume?volume_percent={}'.format(new_volume),
        method='PUT',
        handle_errs={403: DeviceOperationRestricted}
    )
    click.echo('Volume set to {}%'.format(new_volume))
    return
