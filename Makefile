requirements.txt: requirements.in uv
	./uv pip compile requirements.in -o requirements.txt

.venv/bin/activate:
	./uv venv

.PHONY: sync
sync: .venv/bin/activate requirements.txt
	./uv pip sync requirements.txt

run: sync
	./uv run python main.py

test: sync
	./uv run pytest -vvv