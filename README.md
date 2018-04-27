# ceph-export

Simple python script to export rbd images from a ceph pool, based on the last snapshot.

````bash
$ ./export.py --help
Usage: export.py [OPTIONS] POOL [IMAGES]...

  Exports rbd images in POOL to vmdk, based on the last snapshot.

Options:
  --path TEXT           Path where to store the exported images.
  --image-pattern TEXT  Pattern to filter the images.
  --snap-pattern TEXT   Pattern to filter the snapshots.
  --debug / --no-debug  Debug and dry-run mode.
  --help                Show this message and exit.
````

## Example: Export two rbd images to `/srv/tank/vmdk`

````bash
$ ./export.py pve-images vm-100-disk-1 vm-101-disk-1 --path=/srv/tank/vmdk
$ ls -al /srv/tank/vmdk
vm-100-disk-1@autohourly180426180005.vmdk
vm-101-disk-1@autohourly180426180005.vmdk
````

## Example: Export all rbd images in pool `pve-images` to `/srv/tank/vmdk`

````bash
$ ./export.py pve-images --path=/srv/tank/vmdk
$ ls -al /srv/tank/vmdk
vm-100-disk-1@autohourly180426180005.vmdk
vm-101-disk-1@autohourly180426180005.vmdk
vm-101-disk-2@autohourly180426180005.vmdk
...
````

## Example: Export two rbd images to `/srv/tank/qcow2` using the qcow2 format

````bash
$ ./export.py pve-images vm-100-disk-1 vm-101-disk-1 --path=/srv/tank/qcow2 --format=qcow2
$ ls -al /srv/tank/qcow2
vm-100-disk-1@autohourly180426180005.qcow2
vm-101-disk-1@autohourly180426180005.qcow2
````