run:
	flask run

init_migration:
	flask db init

new_migration:
	flask db migrate -m ${name}

upgrade:
	flask db upgrade

upgrade_test:
	flask db upgrade

clean_test:
	docker-compose stop
	docker-compose rm -fs test_db
test:
	make clean_test
	docker-compose up -d test_db
	sleep 1
	make upgrade_test
	pytest
	make clean_test