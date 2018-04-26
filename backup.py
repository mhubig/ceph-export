#!/usr/bin/env python3.6

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import click
import delegator


def get_list_of_images_from(pool):
    images = delegator.chain(f'rbd list {pool} |grep ^vm')
    return [pool / image for image in images.out.strip().split('\n')]


def get_latest_snap_of(image, pattern):
    snaps = delegator.chain(f'rbd snap list {image} |grep {pattern}')
    return snaps.out.strip().split('\n')[-1].split()[1]


def build_convert_command(image, snap, path):
    filename = path / f'{image.name}@{snap}.vmdk'
    return f'qemu-img convert -f rbd -O vmdk -o compat6 rbd:{image}@{snap} {filename.resolve()}'


def conversion_executor(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def converter(cmd):
    click.echo(f'Running: {cmd}')
    return delegator.run(cmd)


@click.command()
@click.argument('pool')
@click.argument('image')
@click.argument('path')
def run(pool, image, path):
    """Convert rbd images to vmdk."""
    path = Path(path)
    pool = Path(pool)

    if image == 'all':
        images = get_list_of_images_from(pool)
    else:
        images = [pool / image]

    convert_commands = []
    for image in images:
        image = Path(image)
        snap = get_latest_snap_of(image, 'autohourly')
        convert_commands.append(build_convert_command(image, snap, path))

    conversion_executor(converter, convert_commands, 4)


if __name__ == '__main__':
    run()
