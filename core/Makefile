test:
	uv run --no-sync pytest tests --cov=Final2x_core --cov-report=xml --cov-report=html

lint:
	uv run --no-sync pre-commit install
	uv run --no-sync pre-commit run --all-files

gen:
	uv run --no-sync python scripts/gen_config.py

gen-ts:
	uv run --no-sync python scripts/gen_pretrained_model_name.py --output ../src/renderer/src/utils/modelOptions.ts

pyinstaller:
	uv run --no-sync pyinstaller --noconfirm --name Final2x-core --icon assets/favicon.ico --distpath dist --workpath build Final2x_core/__main__.py
	uv run --no-sync python scripts/post_pyinstaller.py
