### 安装说明

> 涉及到的安装包均在 install 目录下

#### 1、安装 Docker

> 启用 windows wsl 并安装 wsl_update_x64.msi 启动后如图2一样绿色即可
>
> 如果无法安装，请参考以下微软官方教程
>
> [在 Windows 10 上安装 WSL | Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package)

![image-20210426092932882](image\image-20210426092932882.png)

![image-20210426093433211](image\image-20210426093433211.png)

#### 2、安装 python 以及 docker-compose

```
# 任意版本的 python 均可
pip install docker-compose
```

####  3、运行流程[使用cmd]

> ##### 1. 构建所有 docker 环境

```
make build
```

> ##### 2. 启动 hadoop 环境 [启动后需要稍等一下，如果发现爬虫执行完报错 / 没数据，就是服务没启动完成 30-60s 左右]

```
make up
```

> ##### 3. 执行爬虫脚本[+爬的用户在 ./input/input.txt 一行一个]

```
make run
```

> ##### 4.查看结果

```
make show
```

