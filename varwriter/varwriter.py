#!/usr/bin/env python3
"""
Variscite Writer Tool - Copyright 2022 Variscite LTD

SPDX-License-Identifier: BSD-3-Clause
"""

import os
import sys
import yaml

from varwriter.config import *
from varwriter.utils import *

def main():
    if os.getuid():
        sys.exit(f"[INFO]: Use root privileges to run the '{sys.argv[0]}' program.")

    if not is_connected():
        sys.exit("[INFO]: System has no internet connection.")

    parser, args = args_parser()
    if len(sys.argv) == 1:
        sys.exit(parser.print_help())

    yaml_file_name = MX8_YAML_FILES[args.som]

    sys.stdout.write("="*46 + "\n| Writer Tool - " \
                     "Copyright 2022 Variscite LTD |\n" + "="*46 + "\n\n")

    if not (ftp_r := connect_ftp(msg="[FTP]: Connection to the Variscite FTP...\r")):
        sys.exit("[INFO]: Could not establish FTP connection using the credentials.")

    if not (yaml_local_file_path := retrieve_remote_file(
                                             ftp_r, yaml_file_name,
                                             cwd=VAR_WRITER_FOLDER, leave=False)):
        sys.exit(f"[INFO]: Something went wrong remotely with {yaml_file_name} file.")

    sys.stdout.write(f"[INFO]: Available (Yocto/Debian/B2Qt) BSP images for '{args.som}':\n\n")
    if os.stat(yaml_local_file_path).st_size == 0:
        sys.exit(f"\nNo BSP image available for {args.som}.\n")

    with open(yaml_local_file_path, "r") as fp:
        configs = list(enumerate(yaml.safe_load_all(fp)))

    for index, config in configs:
        sys.stdout.write(f"[{index}]: {config[6]['RECOVERY_SDCARD_FILE_SIZE']:>8}\t" \
                         f"{config[5]['RECOVERY_SDCARD_UPLOAD_DATE']}\t" \
                         f"{config[1]['RECOVERY_SDCARD_OS_TYPE']}\t" \
                         f"{config[0]['RECOVERY_SDCARD_NAME']}\n")
    sys.stdout.write("\n")

    msg = f"[QUESTION]: Please enter the BSP image number (0 - {len(configs) - 1}): "
    while (shift := int(input(msg))) not in range (0, len(configs)):
        continue

    for index, config in configs:
        if shift == index:
            if not (ftp_r := connect_ftp(msg="[FTP]: Connection to the Variscite FTP...\r")):
                sys.exit("[INFO]: Could not establish FTP connection using the credentials.")
            remote_recovery_sdcard_file_name = config[0]['RECOVERY_SDCARD_NAME']
            remote_recovery_sdcard_folder_path = config[2]['RECOVERY_SDCARD_FOLDER_PATH']
            remote_recovery_sdcard_sha1_hash = config[4]['RECOVERY_SDCARD_SHA1_HASH']

            if not (local_recovery_sdcard_file_path := retrieve_remote_file(
                                                ftp_r,
                                                remote_recovery_sdcard_file_name,
                                                cwd=remote_recovery_sdcard_folder_path,
                                                leave=True)):
                sys.exit(f"[INFO]: Something went wrong remotely with {local_recovery_sdcard_file_path} file.")

    local_recovery_sdcard_sha1_hash = get_sha1_hash(local_recovery_sdcard_file_path)

    sys.stdout.write(f"[INFO]: Remote SHA1 Hash:\t'{remote_recovery_sdcard_sha1_hash}'\n")
    sys.stdout.write(f"[INFO]: Local SHA1 Hash:\t'{local_recovery_sdcard_sha1_hash}'\n")
    if not local_recovery_sdcard_sha1_hash == remote_recovery_sdcard_sha1_hash:
        sys.exit("[INFO]: SHA1 Hashes are not equal. File corrupted.\n")
    sys.stdout.write("[INFO]: SHA1 Hashes matched.\n")

    if write_bsp_image_permanent_device(local_recovery_sdcard_file_path, args.device) is False:
        sys.exit(f"\n[INFO]: Something went wrong when writing '{local_recovery_sdcard_file_path}' to the '{args.device}' device.\n")
    sys.stdout.write(f"\n[INFO]: The '{local_recovery_sdcard_file_path}' was successfully written to the '{args.device}' device.\n")
    sys.stdout.write(f"[INFO]: Done.\n")

if __name__ == "__main__":
    main()
