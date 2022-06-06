#!/usr/bin/env python3
"""
Variscite Writer Tool - Copyright 2022 Variscite LTD

SPDX-License-Identifier: BSD-3-Clause
"""

import argparse
import ftplib
from hashlib import sha1
import gzip
import itertools
import logging
import os
import socket
import sys
import textwrap

try:
    from tqdm import tqdm
except ImportError:
    sys.exit("No TQDM module found! Please run: pip3 install tdqm\n")

from varwriter.config import *

logging.basicConfig(level=logging.WARNING)

def get_sha1_hash(recovery_file_path):
    with open(recovery_file_path, "rb") as file:
        data = file.read()
    return sha1(data).hexdigest()

def write_bsp_image_permanent_device(image_path, device):
    bytes_read = 0
    _, bsp_name = os.path.split(image_path)
    sys.stdout.write(f"Writing {bsp_name} to the {device} device...\n")
    dev_fd = os.open(device, os.O_WRONLY)
    with os.fdopen(dev_fd, 'wb') as dev:
        with gzip.open(image_path, 'rb') as f:
            data = f.read(CHUNK)
            while len(data):
                dev.write(data)
                bytes_read += len(data)
                print(f'\rBytes written: {bytes_read}', end='', flush=True)
                data = f.read(CHUNK)
        sys.stdout.write(
            "\n[INFO]: Please wait while synching BSP image to permanent device...")
        return os.fsync(dev_fd)
    return False

def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        logging.error(f"Error trying to establish internet connection: {ex}")
        return False

def connect_ftp(
             ftp_host_name="ftp.variscite.com",
             ftp_user_name="customerv",
             ftp_passwd="Variscite1",
             ftp_timeout=100,
             msg=None):
    sys.stdout.write(f"{msg}")
    try:
        ftp = ftplib.FTP(ftp_host_name, timeout=ftp_timeout)
        ftp.login(user=ftp_user_name, passwd=ftp_passwd)
    except ftplib.all_errors as error:
        logging.error(f"Fail to connect to {ftp_host_name}: {error}\n")
        return False
    except KeyboardInterrupt:
        logging.error("Keyboard Interrupt by user\n")
        ftp.quit()
    return ftp

def retrieve_remote_file(ftp_r, file_name, cwd=None, leave=True):
    local_file = os.path.join(CACHEDIR, file_name)
    if os.path.exists(local_file):
        os.remove(local_file)
    try:
        ftp_r.cwd(cwd)
        with open(local_file, "wb") as f:
            total_size = ftp_r.size(file_name)
            with tqdm(
                   unit_scale=True,
                   leave=leave,
                   miniters=1,
                   desc=f"[FTP]: Retrieving {file_name} from the ftp.variscite.com: ",
                   total=total_size) as tqdm_instance:
                res = ftp_r.retrbinary(
                            f"RETR {file_name}",
                            callback=lambda sent: (f.write(sent),
                            tqdm_instance.update(len(sent))), blocksize=1024)
                if not res.startswith("226 Transfer complete"):
                    os.remove(local_file)
                    return False
    except ftplib.all_errors as error:
        logging.error(f"[FTP]: Fail to retrieve '{local_file}': {error}\n")
        ftp_r.quit()
        return False
    ftp_r.quit()
    return local_file

def args_parser():
    parser = argparse.ArgumentParser(
                      prog='varwriter',
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      epilog=textwrap.dedent(
                             '''Copyright 2022 Variscite LTD''')
    )
    parser.add_argument(
           "--som", choices=VAR_SYSTEM_ON_MODULES,
           help='List of Available System on Modules (DART/VAR-SOM)',
           type=str, required=True
    )
    parser.add_argument(
           "--device",
           help='SD card device (e.g /dev/sd*)',
           type=str, required=True
    )
    return parser, parser.parse_args()
