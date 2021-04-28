FROM python:3.8

MAINTAINER Martin <1403951401@qq.com>

# 安装 python 运行环境
COPY ./pyproject.toml /pyproject.toml

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY hadoop* /tmp/

# 安装 java 环境
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update && \
    apt-get install -y \
        software-properties-common \
        net-tools \
        wget \
        curl \
        netcat \
        gnupg \
        libsnappy-dev && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    rm -rf /var/lib/apt/lists/*

# 安装 hadoop and 文件不存在则下载
RUN set -x && \
    curl -O https://dist.apache.org/repos/dist/release/hadoop/common/KEYS && \
    gpg --import KEYS && \
    if [ ! -f /tmp/hadoop-3.2.1.tar.gz.asc ]; then curl -fSL "https://www.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz.asc" -o /tmp/hadoop-3.2.1.tar.gz.asc; fi && \
    if [ ! -f /tmp/hadoop-3.2.1.tar.gz ]; then curl -fSL "https://www.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz" -o /tmp/hadoop-3.2.1.tar.gz; fi && \
    gpg --verify /tmp/hadoop-3.2.1.tar.gz.asc && \
    tar -xvf /tmp/hadoop-3.2.1.tar.gz -C /opt/ && \
    rm /tmp/hadoop-3.2.1*

# 配置环境变量
ENV HADOOP_VERSION 3.2.1
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
ENV HADOOP_HOME=/opt/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV MULTIHOMED_NETWORK=1
ENV USER=root
ENV PATH $HADOOP_HOME/bin/:$PATH

# 创建软连接、目录
RUN ln -s /opt/hadoop-$HADOOP_VERSION/etc/hadoop /etc/hadoop && \
    mkdir /opt/hadoop-$HADOOP_VERSION/logs && \
    mkdir /hadoop-data

ADD ./entrypoint.sh /entrypoint.sh

RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
