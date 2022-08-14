.PHONY: delete_allure
delete_allure:
	rm allure-results -r


.PHONY: pytest_run
pytest_run: delete_allure
	python -m pytest --alluredir=allure-results -s -v

.PHONY: generate
generate: pytest_run
	allure generate --clean

.PHONY: run
run: generate
	allure serve -p 30000