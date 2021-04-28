#-*-coding:utf-8 -*-
from loguru import logger
from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str = ""  # 用户id
    screen_name: str = ""  # 昵称
    gender: str = ""  # 性别
    birthday: str = ""  # 生日
    location: str = ""  # 所在地
    study_experience: str = ""  # 学习经历
    company: str = ""  # 公司
    registration_time: str = ""  # 注册时间
    sunshine: str = ""  # 阳光信用
    statuses_count: str = ""  # 微博数
    followers_count: str = ""  # 粉丝数
    follow_count: str = ""  # 关注数
    description: str = ""  # 简介
    profile_image_url: str = ""  # 头像
    avatar_hd: str = ""  # 高清头像
    urank: str = ""  # 微博等级
    mbrank: str = ""  # 会员等级
    verified: str = ""  # 是否认证
    verified_type: str = ""  # 认证类型
    verified_reason: str = ""  # 认证信息
    profile_url: str = ""  # 主页

    def print(self):
        keymap = {
            "user_id": "用户id",
            "screen_name": "昵称",
            "gender": "性别",
            "birthday": "生日",
            "location": "所在地",
            "study_experience": "学习经历",
            "company": "公司",
            "registration_time": "注册时间",
            "sunshine": "阳光信用",
            "statuses_count": "微博数",
            "followers_count": "粉丝数",
            "follow_count": "关注数",
            "description": "简介",
            "profile_image_url": "头像",
            "avatar_hd": "高清头像",
            "urank": "微博等级",
            "mbrank": "会员等级",
            "verified": "是否认证",
            "verified_type": "认证类型",
            "verified_reason": "认证信息",
            "profile_url":"微博主页"
        }
        for k, v in self.dict().items():
            logger.info(f"{keymap.get(k, k)}={v}")


class User(BaseModel):
    info: UserInfo

    def print(self):
        self.info.print()