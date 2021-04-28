#!/usr/bin/python
import os
import sys
from pathlib import Path

from mrjob.step import MRStep

worker_file = str(Path(__file__).resolve())
worker_path = str(Path(__file__).parent.resolve())

sys.path.append(worker_path)

from loguru import logger
from mrjob.job import MRJob

logger.info(f"------- 开始执行 -------")
logger.info(f"worker_file:{worker_file}")
logger.info(f"worker_path:{worker_path}")
logger.info(f"file_list:{os.listdir(worker_path)}")
logger.info(f"----------------------")
from weibo import Weibo


class HadoopWeiBo(MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_user_id,
                reducer=self.reducer_get_user_info
            )
        ]

    # user_id 去重
    def mapper_get_user_id(self, _, line):
        yield line, 1

    def reducer_get_user_info(self, key, _):
        config = {
            "user_id_list": [key],
            "filter": 1,
            "since_date": "2021-01-01",
            "start_page": 1,
            "write_mode": ["csv"],
            "original_pic_download": 0,
            "retweet_pic_download": 0,
            "original_video_download": 0,
            "retweet_video_download": 0,
            "result_dir_name": 0,
        }
        # 避免代理失效
        for _ in range(3):
            try:
                wb = Weibo(config)
                wb.start()
                logger.info(wb.user.json())
                yield key, wb.user.json()
            except:
                logger.error(f"{key} eroor")
        else:
            yield key, "fail"


if __name__ == '__main__':
    HadoopWeiBo.run()
