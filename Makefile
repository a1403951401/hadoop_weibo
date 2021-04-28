POD?=$(shell docker ps -q -a)
IMAGES?=$(shell docker images -q)

build:
	docker build -t hadoop/base -f ./docker/base/Dockerfile ./docker/base
	docker build -t hadoop/datanode -f ./docker/datanode/Dockerfile ./docker/datanode
	docker build -t hadoop/historyserver -f ./docker/historyserver/Dockerfile ./docker/historyserver
	docker build -t hadoop/namenode -f ./docker/namenode/Dockerfile ./docker/namenode
	docker build -t hadoop/nodemanager -f ./docker/nodemanager/Dockerfile ./docker/nodemanager
	docker build -t hadoop/resourcemanager -f ./docker/resourcemanager/Dockerfile ./docker/resourcemanager

up:
	docker-compose up -d namenode datanode datanode2 resourcemanager nodemanager historyserver

run:
	docker-compose exec namenode bash -c "hadoop dfsadmin -safemode leave"
	docker-compose up dev

show:
	docker-compose up show

kill:
	docker-compose kill

delete:
	docker-compose down --volumes

clean:
	docker-compose down --volumes --rmi all
	docker rmi hadoop/base