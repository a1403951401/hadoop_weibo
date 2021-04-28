#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List

from pydantic import BaseSettings


class Config(BaseSettings):
    HADOOP_USERNAME: str = 'root'
    HADOOP_HOST: str = "namenode"
    HADOOP_PORT: int = 9870

    HADOOP_INPUT_PATH: str = "/input"
    HADOOP_OUTPUT_PATH: str = "/output"
    HADOOP_LOG_PATH: str = "/app-logs"

    LOCAL_INPUT_PATH: str = "/input"
    LOCAL_OUTPUT_PATH: str = "/output"
    LOCAL_LOG_PATH: str = "/app-logs"
    FILE: List[str] = sys.argv[1:]

    class JAR:
        MAPREDUCE_EXAMPLES: str = "/opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar"
        STREAMING: str = "/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

    @property
    def HADOOP_URL(self) -> str:
        return f"{self.HADOOP_HOST}:{self.HADOOP_PORT}"


config = Config()
if __name__ == '__main__':
    for k, v in config.dict().items():
        print(k, v)
