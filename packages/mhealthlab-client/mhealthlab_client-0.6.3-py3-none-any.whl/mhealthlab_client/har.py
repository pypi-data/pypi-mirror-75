from .constants import *
from glob import glob
from loguru import logger
import arus
import os


class Har:
    def __init__(self, root):
        self._root = root

    def check_exists(self):
        self._sg_folder = os.path.join(self._root, SIGNALIGNER_FOLDER_NAME)
        if len(glob(os.path.join(self._sg_folder, '**', '*.sensor.csv'), recursive=True)) > 0:
            return True
        else:
            return False

    def run_har(self, task):
        if not self.check_exists():
            logger.error(
                "Please convert watch files to signaligner format at first using this script before running har.")
            exit(1)
        if task == 'intensity':
            test_files = glob(os.path.join(
                self._sg_folder, '*', '*.sensor.csv'))
            for test_file in test_files:
                logger.info(f'Running {task} model on file: {test_file}')
                model_path = arus.models.get_prebuilt(task)
                predict_df, _ = arus.cli.predict_model(
                    model_path, test_file, 'signaligner')
                output_path = test_file.replace(
                    'sensors', task).replace('sensor', task)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                arus.plugins.signaligner.save_as_signaligner(
                    predict_df, output_path, arus.plugins.signaligner.FileType.ANNOTATION, labelset=task, mode='w', index=False, header=True)
                logger.info(f'Saved predictions to {output_path}')
        else:
            logger.error(f"The given task {task} is not supported.")
            exit(1)
