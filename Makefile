build:
	docker-compose -f docker-compose.yml build

build-no-cache:
	docker-compose -f docker-compose.yml build --no-cache

rebuild:
	docker-compose -f docker-compose.yml up -d --build

start:
	docker-compose -f docker-compose.yml up -d

stop:
	docker-compose -f docker-compose.yml stop

bash:
	docker-compose -f docker-compose.yml exec app bash

logs:
	docker-compose -f docker-compose.yml logs -f app

run-script:
	docker-compose -f docker-compose.yml exec app bash -c "python lambda_function.py"

create-zip:
	cd venv/lib/python3.9/site-packages \
	&& zip -r ${OLDPWD}/function.zip . \
	&& cd ${OLDPWD} \
	&& zip -g function.zip lambda_function.py \
	summaries_information/* \
	db/*
