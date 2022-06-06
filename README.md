# Writer Tool

The **Writer Tool** helps the user to flash recovery SD card releases from the
Variscite FTP server into SD card devices.

## Quick Installation

1. Install the following packages:

```bash
apt install python3-stdeb fakeroot python-all
```

2. Clone the **var-writer** tool, and generate the debian package:

```bash
git clone https://github.com/dorta/var-writer && cd var-writer
python3 setup.py --command-packages=stdeb.command bdist_deb
```

3. Then, install the debian (.deb) package:

```
cd deb_dist
dpkg -i python3-varwriter_<version>.deb
```

## Flashing Recovery SD Card

To flash a recovery SD card using the **var-writer** tool, please use the
following arguments:

```bash
varwriter --som <som_name> --device <device_name>
```
* --som (choose one of the following system on the modules)

```bash
{DART-MX8M,DART-MX8M-MINI,DART-MX8M-PLUS,VAR-SOM-MX8,VAR-SOM-MX8X,VAR-SOM-MX8M-NANO}
```

* --device (specify the SD card device path, for example: _/dev/sd<x>_)

For more information, please run the **var-writer** with the helper argument:

```bash
varwriter --help
```

__NOTE:__ The **var-writer** tool must be executed with root privileges.


## Copyright and License

Copyright 2022 Variscite LTD. Free use of this software is granted under
the terms of the [BSD 3-Clause License](https://github.com/dorta/var-writer/blob/master/LICENSE).
