import os
import argparse
import re
from datetime import datetime
from cli_formatter.output_formatting import error, info


def __is_root() -> bool:
    """ checks if the script is running with sudo rights"""
    return os.geteuid() == 0


def __get_first_unused_loop_device() -> str:
    """ returns the path to the first unused loop device (e.g. /dev/loop4) """
    return os.popen('losetup -f').read().strip()


def __get_default_name_of_mounting_directory() -> str:
    return os.path.join('/mnt', datetime.now().strftime('%Y.%m.%d_%H.%M'))


def __escape_path(path: str):
    return path.replace('"', '\\"')


def __final_mount_procedure(source_path: str, target_path: str, partition_number: int):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    mount_options = list()

    while True:
        user_input = input('Mount in readonly mode (y/n) [y]: ')
        if len(user_input) == 0 or user_input == 'y':
            mount_options.append('ro')
            break
        elif user_input == 'n':
            break
        else:
            error(message='input not valid.')
            print()

    mount_options.append('show_sys_files')

    while True:
        user_input = input('Mount as NTFS filesystem (y/n) [y]: ')
        if len(user_input) == 0 or user_input == 'y':
            mount_options.append('streams_interface=windows')
            break
        elif user_input == 'n':
            break
        else:
            error(message='input not valid.')
            print()

    # generate mount command
    mount_options_string = ','.join(mount_options)

    mount_command = 'mount -o {} "{}" "{}" >/dev/null 2>&1'.format(mount_options_string, __escape_path(source_path), __escape_path(target_path))

    if int(os.system(mount_command)) == 0:
        info(message='Partition {} was mounted under "{}"'.format(partition_number, __escape_path(target_path)))
    else:
        error('An Error occurred. Partition could not be mounted')


def program(input_path: str, mounting_path: str):
    # create directory which contains all mounting endpoints
    if not os.path.exists(mounting_path):
        try:
            os.makedirs(mounting_path)
        except PermissionError:
            error('Permission denied for creating directory "{}"'.format(mounting_path))
            exit()

    # mount the ewf file
    mounting_path_ewf_dir = os.path.join(mounting_path, '.ewf')
    if not os.path.exists(mounting_path_ewf_dir):
        try:
            os.makedirs(mounting_path_ewf_dir, exist_ok=True)
        except PermissionError:
            error('Permission denied for creating directory "{}"'.format(mounting_path_ewf_dir))
            exit()

    if int(os.system('ewfmount "{}" "{}" >/dev/null 2>&1'.format(
            __escape_path(input_path),
            __escape_path(mounting_path_ewf_dir)
       ))) != 0:
        error(message='An error occurred while mounting ewf file to "{}". Exiting.'.format(mounting_path_ewf_dir))
        exit()
    else:
        info(message='ewf file mounted to "{}"'.format(mounting_path_ewf_dir))

    # get the path to the ewf file
    path_to_the_mounted_ewf_file = None
    for file_path in os.listdir(mounting_path_ewf_dir):
        path_to_the_mounted_ewf_file = os.path.join(mounting_path_ewf_dir, file_path)
    if path_to_the_mounted_ewf_file is None:
        info(message='Could not find mounted ewf file. Exiting.')
        exit()

    # Mount ewf tile to unused loop device
    path_to_loop_device = __get_first_unused_loop_device()
    if int(os.system('losetup -Pv "{}" "{}" >/dev/null 2>&1'.format(
            __escape_path(path_to_loop_device),
            __escape_path(path_to_the_mounted_ewf_file)
       ))) != 0:
        info(message='An error occurred while mounting ewf file to loop back device. Exiting.')
        exit()

    while True:
        info(message='Select Partition to mount:')
        os.system('fdisk -l "{}"'.format(__escape_path(path_to_loop_device)))
        print()
        selected_partition_number = input('select number of partition (0 for complete disk) [1] > ')

        if len(selected_partition_number) == 0:     # Default value
            selected_partition_number = 1
        else:
            # check if partition number is an integer
            try:
                selected_partition_number = int(selected_partition_number)
            except ValueError:
                error('The partition number must be an integer')
                print()
                continue

        if selected_partition_number == 0:
            selected_partition_path = path_to_loop_device
            info(message='selected the complete disk "{}"'.format(__escape_path(selected_partition_path)))
        else:
            selected_partition_path = '{}p{}'.format(path_to_loop_device, selected_partition_number)
            info(message='selected partition "{}"'.format(__escape_path(selected_partition_path)))

        bitlocker_key = input('Bitlocker Recovery Key (if encrypted otherwise empty) > ')

        if len(bitlocker_key) > 0:

            # check if provided key is valid
            if re.fullmatch(r'((\d){6}-){7}(\d{6})', bitlocker_key) is None:
                error('The format of the recovery key you typed in is invalid.')
                info('The key must be in the format: DDDDDD-DDDDDD-DDDDDD-DDDDDD-DDDDDD-DDDDDD-DDDDDD')
                print()
                continue

            mounting_path_dislocker = os.path.join(mounting_path, '.partition_{}_encrypted'.format(selected_partition_number))
            if not os.path.exists(mounting_path_dislocker):
                os.makedirs(mounting_path_dislocker)
            if int(os.system('dislocker -v -V "{}" -p{} "{}" >/dev/null 2>&1'.format(
                    __escape_path(selected_partition_path),
                    bitlocker_key,
                    __escape_path(mounting_path_dislocker)
               ))) != 0:
                info(message='An Error occurred. Partition could not be decrypted')
            else:
                mounting_path_dislocker_file = os.path.join(mounting_path_dislocker, 'dislocker-file')
                mounting_path_decrypted = os.path.join(mounting_path, 'partition_{}_decrypted'.format(selected_partition_number))
                __final_mount_procedure(source_path=mounting_path_dislocker_file, target_path=mounting_path_decrypted, partition_number=selected_partition_number)
        else:
            mounting_path_partition = os.path.join(mounting_path, 'partition_{}'.format(selected_partition_number))
            __final_mount_procedure(source_path=selected_partition_path, target_path=mounting_path_partition, partition_number=selected_partition_number)
        print()
        input('Press ENTER to mount another partition')


def main():
    print('pyEWFmount by Florian Wahl, 03.08.2020')
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help="path to a EWF file which should be mounted")
    parser.add_argument('-o', '--output', type=str, help="Specify the name of the mounted directory (default: /mnt/YYYY.MM.DD_hh.mm)", default=__get_default_name_of_mounting_directory())
    arguments = parser.parse_args()

    if arguments.input is None or len(arguments.input) == 0:
        parser.print_help()
        exit()

    input_path = os.path.abspath(arguments.input)
    mounting_path = os.path.abspath(arguments.output)

    if not __is_root():
        error(message='The script needs sudo rights. Exiting.')
        exit()

    try:
        program(input_path=input_path, mounting_path=mounting_path)
    except KeyboardInterrupt:
        error(message='Keyboard Interrupt. Exiting.')


if __name__ == '__main__':
    main()
