#!/usr/bin/env python3.6

import delegator


def get_list_of_images_from(pool):
    images = delegator.chain(f'rbd list {pool} |grep ^vm')
    return list(images.out)


def get_snaps_of(image, pattern):
    snaps = delegator.chain(f'rbd snap list {image} |grep {pattern}')
    return list(snaps.out)
