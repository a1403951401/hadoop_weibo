"""
消费者，负责读取 hadoop 内容，然后执行
"""
import os
import shutil
import time

from loguru import logger
from pyhdfs import HdfsHttpException

from config import config
from hadoop import hadoop


def clean_path(path: str):
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            shutil.rmtree(os.path.join(path, f))
        else:
            os.remove(os.path.join(path, f))


def main():
    # 清理日志
    hadoop.delete(config.HADOOP_LOG_PATH, recursive=True)
    clean_path(config.LOCAL_LOG_PATH)
    # 清理 output 目录
    hadoop.clean_dir(config.HADOOP_OUTPUT_PATH)
    clean_path(config.LOCAL_OUTPUT_PATH)
    # 上传文件
    hadoop.copy_path_from_local(config.LOCAL_INPUT_PATH)
    # 执行运行语句
    hadoop.streaming("count.py", "/input/input.txt")
    logger.info("hadoop streaming success, download output ...")
    # 下载执行结果
    hadoop.copy_path_to_local(config.HADOOP_OUTPUT_PATH)
    logger.info("download logs ...")
    # 下载执行 log
    for _ in range(600):
        if hadoop.download_log():
            break
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        main()
    except HdfsHttpException as e:
        logger.exception("Waiting for the service to start")
        time.sleep(1)
    except Exception as e:
        logger.exception("start job error")
