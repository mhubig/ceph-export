from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import click
import delegator


def get_list_of_supported_formats(debug):
    formats = delegator.chain("qemu-img --help |grep 'Supported formats:'")
    return formats.out.split(':')[1].strip().split()


def get_list_of_images_from(pool, pattern, debug):
    images = delegator.chain(f'rbd list {pool} |grep {pattern}')
    return [pool / image for image in images.out.strip().split('\n')]


def get_latest_snap_of(image, pattern, debug):
    snaps = delegator.run(f'rbd snap list {image}').out.strip().split('\n')
    snaps = [snap for snap in snaps if pattern in snap]

    if not snaps:
        return ''

    return snaps[-1].strip().split()[1]


def build_convert_command(image, snap, path, format, debug):
    if snap:
        filename = path / f'{image.name}@{snap}.{format}'
        imagename = f'{image}@{snap}'
    else:
        filename = path / f'{image.name}.{format}'
        imagename = f'{image}'
    return f'qemu-img convert -f rbd -O {format} -o compat6 rbd:{imagename} {filename.resolve()}'


def conversion_executor(func, args, workers, debug):
    if debug:
        func = click.echo
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def converter(cmd):
    return delegator.run(cmd)


@click.command()
@click.argument('pool')
@click.argument('images', nargs=-1)
@click.option('--path', default='./', help='Path where to store the exported images.')
@click.option('--format', default='vmdk', help='Format of the converted image.')
@click.option('--image-pattern', default='^vm', help='Pattern to filter the images.')
@click.option('--snap-pattern', default='autohourly', help='Pattern to filter the snapshots.')
@click.option('--debug/--no-debug', default=False, help='Debug and dry-run mode.')
def cli(pool, images, path, image_pattern, snap_pattern, format, debug):
    """Exports rbd images from a ceph pool, based on the last snapshot."""

    if format not in get_list_of_supported_formats(debug):
        raise click.BadParameter(f'Format {format} not supported by the installed qemu-img.')

    path = Path(path)
    pool = Path(pool)

    if not images:
        images = get_list_of_images_from(pool, image_pattern, debug)
    else:
        images = [pool / image for image in images]

    convert_commands = []
    for image in images:
        image = Path(image)
        snap = get_latest_snap_of(image, snap_pattern, debug)
        convert_commands.append(build_convert_command(image, snap, path, format, debug))

    conversion_executor(converter, convert_commands, 4, debug)
