FROM registry.cn-shanghai.aliyuncs.com/martin_hadoop/base:latest

MAINTAINER Martin <1403951401@qq.com>

HEALTHCHECK CMD curl -f http://localhost:8042/ || exit 1

ADD run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8042

CMD ["/run.sh"]
