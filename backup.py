#!/usr/bin/env python3.6

import click
import delegator


def get_list_of_images_from(pool):
    images = delegator.chain(f'rbd list {pool} |grep ^vm')
    return list(images.out)


def get_latest_snaps_of(image, pattern):
    snaps = delegator.chain(f'rbd snap list {image} |grep {pattern}')
    return sort(list(snaps.out))


@click.command()
@click.argument('image')
def backup(image):
    """Converts a an rbd image to vmdk."""
    click.echo(get_latest_snaps_of(image, '^autosnap'))


if __name__ == '__main__':
    backup()
