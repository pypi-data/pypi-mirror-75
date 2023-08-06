
import enum
import os
from tqdm import tqdm
from loguru import logger
import pyzipper
import glob
import pysftp
import pkg_resources


class Client:
    class Status(enum.Enum):
        DISCONNECTED = enum.auto()
        CONNECTED = enum.auto()

    def __init__(self):
        self._hostname = 'wockets.ccs.neu.edu'
        self._username = 'sftpuser'
        self._password = 'mHealth@NEU'
        self._status = Client.Status.DISCONNECTED
        self._data_folder = '.'
        self._studies = ['MICROT', 'LML']
        self._client = None

    def connect(self, pwd):
        try:
            extra_known_hosts = pkg_resources.resource_filename(
                'mhealthlab_client', 'known_hosts')
            cnopts = pysftp.CnOpts(knownhosts=extra_known_hosts)
            self._client = pysftp.Connection(host=self._hostname,
                                             username=self._username,
                                             password=pwd,
                                             cnopts=cnopts)
        except Exception as e:
            logger.error("Failed to connect to the server via SFTP.")
            logger.error(e)
            exit(1)
        self._status = Client.Status.CONNECTED
        logger.info('Connected to the server')

    def validate_study_name(self, study_name):
        if study_name not in self._studies:
            logger.error('Study name is not supported: {}', study_name)
            return False
        return True

    def validate_participant_name(self, project, pid):
        found = len(self.find_participants(project, pid)) > 0
        if found:
            return True
        else:
            logger.error(f"Participant {pid} is not found for study {project}")
            return False

    def get_participants(self, project):
        assert self._status == Client.Status.CONNECTED
        with self._client.cd(f'./{project}'):
            participants = self._client.listdir()
        return participants

    def find_participants(self, project, keyword):
        participants = self.get_participants(project)
        pids = list(filter(lambda pid: keyword in pid, participants))
        return pids

    def download_all(self, project, to, pwd=None):
        folder = os.path.join(self._data_folder, project)
        self._download(folder, to)
        if pwd is None:
            return
        else:
            failed_files = self._decrypt(to, pwd)

            if failed_files is not None:
                logger.error("Failed to decrypt these files: ")
                for f, e in failed_files:
                    logger.error('{}, {}', f, e)
            else:
                logger.info("All files are decrypted successfully")

    def download_by_participant(self, project, pid, to, pwd=None):
        # Must use '/' because this is the path for the remote server
        folder = self._data_folder + '/' + project + '/' + pid
        to = os.path.join(to, pid)
        self._download(folder, to)
        if pwd is None:
            return
        else:
            failed_files = self._decrypt(to, pwd)

            if failed_files is not None:
                logger.error("Failed to decrypt these files: ")
                for f, e in failed_files:
                    logger.error('{}, {}', f, e)
            else:
                logger.info("All files are decrypted successfully")

    def _decrypt_file(self, f, to, pwd):
        ref = None
        try:
            ref = pyzipper.AESZipFile(
                f, mode='r', compression=pyzipper.ZIP_DEFLATED)
            os.makedirs(to, exist_ok=True)
            try:
                ref.extractall(to)
            except RuntimeError as e:
                ref.extractall(to, pwd=pwd)
            except Exception as e:
                ref.extractall(to, pwd=pwd)
            ref.close()
            if os.path.dirname(f) != to:
                failed_files = self._decrypt(to, pwd, progress_bar=False)
                if failed_files is not None:
                    return failed_files
                else:
                    return None
            else:
                return None
        except Exception as e:
            if ref is not None:
                ref.close()
            if e is not None:
                return f, e
            else:
                return f, ""

    def _decrypt(self, folder, pwd, progress_bar=True):
        local_files = glob.glob(os.path.join(
            folder, '**', '*.zip'), recursive=True)
        n = len(local_files)
        if progress_bar:
            bar = tqdm(total=n)
        failed_files = []
        for f in local_files:
            if os.path.basename(f).count('.') > 1:
                to = os.path.dirname(f)
            else:
                to = os.path.join(os.path.dirname(
                    f), os.path.basename(f).split('.')[0])
            result = self._decrypt_file(f, to, pwd)
            if result is not None:
                if type(result) is list:
                    failed_files += result
                else:
                    failed_files.append(result)
            else:
                os.remove(f)
                # create an empty file as a marker indicating that this zip file has been decrypted.
                with open(f + '.done', 'w'):
                    pass
            if progress_bar:
                bar.update()
                bar.set_description(f'Decrypting {f}')
        if progress_bar:
            bar.close()
        if len(failed_files) == 0:
            return None
        return failed_files

    def _get_files(self, folder):
        files = []
        logger.info(
            'Analyzing the total amount of files to be downloaded for this participant...')
        self._client.walktree(folder,
                              lambda f: files.append(
                                  f),
                              lambda d: d,
                              lambda u: u)
        logger.info(
            f'Found {len(files)} files.')
        return files

    def _download(self, folder, to):
        assert self._status == Client.Status.CONNECTED
        files = self._get_files(folder)
        n = len(files)
        bar = tqdm(total=n)
        for f in files:
            local = f.replace(folder, to)
            local_name = os.path.basename(local).replace(':', '')
            local = os.path.join(os.path.dirname(local), local_name)
            if os.path.exists(local) or os.path.exists(local + '.done'):
                bar.update()
                bar.set_description(f"File {local} was already downloaded.")
                continue
            os.makedirs(os.path.dirname(local), exist_ok=True)
            self._client.get(f, local)
            bar.update()
            bar.set_description(f'Downloaded file: {local}')
        bar.close()

    @staticmethod
    def extract_participant_list(filepath):
        with open(filepath, mode='r') as f:
            pids = f.readlines()
        pids = list(map(lambda pid: pid.strip('\n'), pids))
        return pids
