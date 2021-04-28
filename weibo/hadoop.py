import os
import shutil

from loguru import logger
from pyhdfs import HdfsClient

from config import config


class Hadoop(HdfsClient):

    def __init__(self, *args, **kwargs):
        super().__init__(
            hosts=kwargs.get("hosts", config.HADOOP_URL),
            user_name=kwargs.get("user_name", config.HADOOP_USERNAME)
        )
        logger.info(f"init hadoop success, node={self.get_active_namenode()}, path={self.get_home_directory()}")

    def clean_dir(self, path, create=False):
        if self.exists(path):
            self.delete(path, recursive=True)
        if create:
            self.mkdirs(path)

    def copy_path_from_local(self, path: str, upload_path: str = None):
        if not upload_path:
            upload_path = config.LOCAL_INPUT_PATH
        self.clean_dir(upload_path, create=True)
        for file in os.listdir(path):
            logger.info(f"uploading {os.path.join(path, file)} -> {os.path.join(upload_path, file)}")
            if os.path.isdir(os.path.join(path, file)):
                self.copy_path_from_local(os.path.join(path, file), os.path.join(upload_path, file))
            else:
                self.copy_from_local(os.path.join(path, file), os.path.join(upload_path, file))

    def copy_path_to_local(self, path: str, download_path: str = None, ext="") -> int:
        num = 0
        if not download_path:
            download_path = config.LOCAL_OUTPUT_PATH
            for f in os.listdir(config.LOCAL_OUTPUT_PATH):
                if os.path.isdir(os.path.join(config.LOCAL_OUTPUT_PATH, f)):
                    shutil.rmtree(os.path.join(config.LOCAL_OUTPUT_PATH, f))
                else:
                    os.remove(os.path.join(config.LOCAL_OUTPUT_PATH, f))
        if hadoop.exists(path):
            for file in hadoop.listdir(path):
                if self.get_file_status(os.path.join(path, file)).type == "DIRECTORY":
                    num += self.copy_path_to_local(os.path.join(download_path, file), os.path.join(path, file), ext)
                else:
                    logger.info(f"download {os.path.join(path, file)} -> {os.path.join(download_path, file)}")
                    if not os.path.exists(download_path):
                        os.makedirs(download_path)
                    try:
                        self.copy_to_local(os.path.join(path, file), os.path.join(download_path, file) + ext)
                        num += 1
                    except:
                        logger.warning(f"download {os.path.join(path, file)} error")
        return num

    def download_log(self) -> int:
        for f in os.listdir(config.LOCAL_LOG_PATH):
            shutil.rmtree(os.path.join(config.LOCAL_LOG_PATH, f))
        return self.copy_path_to_local(config.HADOOP_LOG_PATH, config.LOCAL_LOG_PATH, ".txt")

    @staticmethod
    def run(command: str):
        logger.info(f'command:{command}')
        return os.system(command)

    @classmethod
    def wordcount(cls, file: str, output: str):
        return cls.run(f"hadoop jar {config.JAR.MAPREDUCE_EXAMPLES} wordcount {file} {output}")

    def streaming(self, run: str, input_file: str, output: str = None):
        logger.info(self.open(os.path.join(config.HADOOP_INPUT_PATH, run)).read().decode("utf-8"))
        return self.run(f'hadoop jar {config.JAR.STREAMING} '
                        f'-files "{",".join([os.path.join(config.HADOOP_INPUT_PATH, f) for f in os.listdir(config.HADOOP_INPUT_PATH)])}" '
                        f'-mapper "python {run}" '
                        f'-reducer "python {run}" '
                        f'-input {input_file} '
                        f'-output {output or config.HADOOP_OUTPUT_PATH}')


hadoop = Hadoop()
