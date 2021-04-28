from typing import Dict

from happybase import Connection


class Hbase(Connection):

    def __init__(self, **kwargs):
        if "host" not in kwargs:
            kwargs['host'] = "hbase"
        if "port" not in kwargs:
            kwargs['port'] = 9090
        super().__init__(**kwargs)

    def check_create_table(self, name, families):
        if name.encode('utf-8') not in self.tables():
            self.create_table(name, families)
            return True
        return False

    def update(self, table_name: str, index: str, data_map: Dict[str, Dict[str, str]]):
        data = {}
        for item, d in data_map.items():
            for key, value in d.items():
                data[f"{item}:{key}"] = value
        return self.table(table_name).put(index, data)

    @staticmethod
    def format_dict(row: dict):
        data = {}
        for k, v in row.items():
            item, key = k.decode("utf-8").split(":")
            if item not in data:
                data[item] = {}
            data[item][key] = v.decode("utf-8")
        return data

    def get(self, table_name: str, index: str):
        return self.format_dict(self.table(table_name).row(index))


hbase = Hbase()

if __name__ == '__main__':
    from loguru import logger
    from model import User

    # 遍历 user 表
    for k, v in hbase.table("user").scan():
        logger.info('*' * 45 + k.decode("utf-8") + "*" * 45)
        User(**hbase.format_dict(v)).print()
        logger.info('*' * 100)