# ---开发环境---
build_dev:
	TAG=develop docker-compose -f docker-compose.yml build

push_dev:
	TAG=develop docker-compose -f docker-compose.yml push

pull_dev:
	TAG=develop docker-compose -f docker-compose.yml pull

up_dev:
	TAG=develop docker-compose --compatibility -f docker-compose.yml up -d --remove-orphans

down_dev:
	TAG=develop docker-compose -f docker-compose.yml down --remove-orphans

restart_dev:
	TAG=develop docker-compose -f docker-compose.yml down --remove-orphans
	TAG=develop docker-compose --compatibility -f docker-compose.yml up -d --remove-orphans
