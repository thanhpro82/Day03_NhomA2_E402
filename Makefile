.PHONY: dev test seed reset docker-up docker-down

dev:
	.venv/bin/streamlit run src/app.py

test:
	PYTHONPATH=. .venv/bin/pytest src/tests/ -v

seed:
	PYTHONPATH=. .venv/bin/python src/database/seed.py

reset:
	rm -f cupid_agent.db
	PYTHONPATH=. .venv/bin/python src/database/seed.py

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
