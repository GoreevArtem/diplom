build:
	docker-compose build

up:
	docker-compose up -d

debug:
	docker-compose up --build

stop:
	docker-compose down

down:
	docker-compose down -v

rebuild:
	docker-compose down -v && docker-compose up --build


###Сборка под ARM32v7
armbuild:
	docker-compose -f docker-compose-arm32v7.yml build

armup:
	docker compose -f docker-compose-arm32v7.yml docker-compose.yml up -d

armdebug:
	docker compose -f docker-compose-arm32v7.yml docker-compose.yml up --build

armstop:
	docker compose -f docker-compose-arm32v7.yml docker-compose.yml down

armdown:
	docker compose -f docker-compose-arm32v7.yml docker-compose.yml down -v
