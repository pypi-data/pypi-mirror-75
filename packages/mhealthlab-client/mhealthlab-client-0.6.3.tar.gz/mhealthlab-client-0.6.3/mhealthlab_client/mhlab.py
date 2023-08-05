"""mHealth Lab client

Usage:
  mhlab download STUDY [--sftp=<pwd>] [--pid=<id_or_file>] [--decrypt=<pwd>] [--folder=<folder>] [--debug]
  mhlab signaligner --folder=<folder> --pid=<pid> --sr=<sampling_rate> [--date_range=<date_range>] [--debug]
  mhlab har --task=<task> --folder=<folder>
  mhlab --help
  mhlab --version

Arguments:
  STUDY                                     Study name. It should match the folder name used to store datasets on the server.

Options:
  -h, --help                                Show help message
  -v, --version                             Show program version
  -p <pid>, --pid <pid>                     The participant ID or a txt file with list of participant IDs each on a separate line
  --sftp <pwd>                              The password to connect to the server.
  -d <pwd>, --decrypt <pwd>                 Use <pwd> to decrypt the downloaded files.
  -f <folder>, --folder <folder>            Local folder for downloaded dataset.
  -s <sampling_rate>, --sr <sampling_rate>  The sampling rate of the converted sensor file in Actigraph csv format used for signaligner.
  --date_range <date_range>                 The start and stop date of the data to be converted. E.g., "--date_range=2020-06-01,2020-06-10", "--date_range=2020-06-01", or "--date_range=,2020-06-10".
  -t <task>, --task <task>                  The HAR task, currently it supports "intensity" to classify activity intensity.
"""

from docopt import docopt
from .client import Client
from .android_watch import AndroidWatch
from .har import Har
from loguru import logger
import os
import arus
import sys
from outdated import check_outdated, utils
import pkg_resources
import tempfile


def mhlab():
    ver = pkg_resources.get_distribution("mhealthlab-client").version
    print('\n')
    print(f'mHealth Lab Client {ver}\n')
    check_client_outdated(ver)
    arguments = docopt(__doc__, version=f'mHealth Lab Client {ver}')
    if arguments['--debug']:
        logger.remove()
        logger.add(sys.stderr, level='DEBUG')
    else:
        logger.remove()
        logger.add(sys.stderr, level='INFO')
    logger.debug(arguments)
    if arguments['download']:
        study_name = arguments['STUDY']
        pwd = str.encode(
            arguments['--decrypt']) if arguments['--decrypt'] is not None else None
        sftp_pwd = arguments['--sftp']
        if sftp_pwd is None:
            logger.error(
                'You must provide a valid sftp password to run the script using `--sftp <pwd>` option.')
            return

        to = arguments['--folder'] or './' + study_name
        if arguments['--pid'] is None:
            pid = None
        else:
            pid = arguments['--pid']
            if os.path.exists(pid):
                pid = Client.extract_participant_list(pid)
        logger.add(to + "/mhlab_download.log", rotation="500 MB")
        if pid is None:
            download_all(study_name, to, pwd, sftp_pwd)
        elif type(pid) is list:
            download_by_participant_list(study_name, pid, to, pwd, sftp_pwd)
        else:
            download_by_participant(study_name, pid, to, pwd, sftp_pwd)
    elif arguments['signaligner']:
        to = arguments['--folder']
        sr = int(arguments['--sr'])
        pid = arguments['--pid']
        date_range = arguments['--date_range'].split(
            ',') if arguments['--date_range'] is not None else None
        convert_sensor_files(to, pid, sr, date_range)
    elif arguments['har']:
        to = arguments['--folder']
        task = arguments['--task']
        run_har_on_watch_files(to, task)


def remove_update_cache(package):
    cache_file = os.path.join(tempfile.gettempdir(),
                              utils.get_cache_filename(package))
    if os.path.exists(cache_file):
        logger.info(f'Remove update checking cache for {package}')
        os.remove(cache_file)


def check_client_outdated(ver):

    # remove caches
    remove_update_cache('mhealthlab-client')
    remove_update_cache('arus')

    is_outdated, latest_version = check_outdated(
        'mhealthlab-client', ver)
    arus_ver = pkg_resources.get_distribution("arus").version
    is_arus_outdated, latest_arus_version = check_outdated('arus', arus_ver)
    if is_outdated:
        logger.warning(
            f'The client version {ver} is outdated. The latest version is {latest_version}')
        logger.warning(
            f'Please run "pip install -U mhealthlab-client" or "pip3 install -U mhealthlab-client" to update.')
        exit(1)

    if is_arus_outdated:
        logger.warning(
            f'The client core dependency arus {arus_ver} is outdated. The latest version is {latest_arus_version}')
        logger.warning(
            f'Please run "pip install -U arus" or "pip3 install -U arus" to update.')
        exit(1)


def download_all(study_name, to, pwd, connect_pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect(pwd=connect_pwd)
    client.download_all(study_name, to, pwd)


def download_by_participant(study_name, pid, to, pwd, connect_pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect(pwd=connect_pwd)
    if not client.validate_participant_name(study_name, pid):
        exit(1)
    client.download_by_participant(study_name, pid, to, pwd)


def download_by_participant_list(study_name, pids, to, pwd, connect_pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect(pwd=connect_pwd)
    for pid in pids:
        logger.info("Download data for {}".format(pid))
        client.download_by_participant(study_name, pid, to, pwd)


def convert_sensor_files(to, pid, sr, date_range):
    watch = AndroidWatch(to, pid)
    watch.convert_to_actigraph(date_range=date_range, sr=sr)


def run_har_on_watch_files(to, task):
    har = Har(to)
    har.run_har(task)


if __name__ == '__main__':
    mhlab()
