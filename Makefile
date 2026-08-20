.DEFAULT_GOAL := help

VENV  := venv
STAMP := $(VENV)/.installed
ZIP   := dist/pass-protection-intelligence.zip

.PHONY: help setup notebooks test serve demo \
        docker-build docker-run docker-stop \
        docs-pdf package clean

help:
	@echo "Pass Protection Intelligence — available targets"
	@echo ""
	@echo "  Quick path (uses the trained models already in artifacts/, no dataset needed):"
	@echo "    make setup         Create venv and install dependencies"
	@echo "    make test          Run the API test suite (pytest)"
	@echo "    make serve         Run the FastAPI service   -> http://127.0.0.1:8000/docs"
	@echo "    make demo          Run the Streamlit demo    -> http://127.0.0.1:8501"
	@echo ""
	@echo "  Full path (reproduce training from raw data — see README.md section 3 for"
	@echo "  where to get the dataset and place it under data/ first):"
	@echo "    make notebooks     Execute all 6 notebooks in order (can take 30-90+ min:"
	@echo "                       ~8M tracking rows per notebook, plus hyperparameter"
	@echo "                       search in 02-06 — this is expected, not a hang)"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-build  Build the serving image"
	@echo "    make docker-run    Run it              -> http://127.0.0.1:8000"
	@echo "    make docker-stop   Stop and remove the container"
	@echo ""
	@echo "  Docs:"
	@echo "    make docs-pdf      Render every .md doc to a PDF under docs/pdf/ (needs"
	@echo "                       pandoc + Google Chrome, both used only at build time —"
	@echo "                       the recipient never needs either)"
	@echo ""
	@echo "  Packaging (no git needed):"
	@echo "    make package       Zip the project for sharing — excludes venv/ and data/,"
	@echo "                       keeps the trained artifacts/ so the quick path works"
	@echo "                       for whoever you send it to. Run 'make docs-pdf' first"
	@echo "                       if you've edited any .md file since the last build."
	@echo "    make clean         Remove venv, caches, and dist/"

$(STAMP): requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	touch $(STAMP)

setup: $(STAMP)

notebooks: setup
	@echo "Running notebooks 01-06 in order. This reads the raw CSV/parquet files under"
	@echo "data/ and re-trains everything from scratch — expect this to take a while."
	$(VENV)/bin/jupyter nbconvert --to notebook --execute --inplace \
		--ExecutePreprocessor.timeout=-1 \
		notebooks/01_eda.ipynb \
		notebooks/02_model_player_role.ipynb \
		notebooks/03_model_pressure_allowed.ipynb \
		notebooks/04_model_pressure_generated.ipynb \
		notebooks/05_model_block_type.ipynb \
		notebooks/06_survival_time_to_pressure.ipynb

test: setup
	$(VENV)/bin/python -m pytest tests/ -v

serve: setup
	$(VENV)/bin/uvicorn serving.main:app --reload

demo: setup
	$(VENV)/bin/streamlit run serving/streamlit_app.py --server.headless true

docker-build:
	docker build -t pass-protection-api .

docker-run: docker-build
	docker run -d --name pass-protection-api -p 8000:8000 pass-protection-api
	@echo "Running at http://127.0.0.1:8000/docs — stop with: make docker-stop"

docker-stop:
	-docker stop pass-protection-api
	-docker rm pass-protection-api

docs-pdf:
	./scripts/build-pdfs.sh

package:
	@mkdir -p dist
	@rm -f $(ZIP)
	zip -r $(ZIP) . \
		-x "venv/*" -x "data/*" -x "dist/*" -x ".claude/*" \
		-x "*__pycache__*" -x "*.ipynb_checkpoints*" \
		-x "*.DS_Store" -x ".pytest_cache/*" -x "*.pyc" \
		-x "*feature_table.parquet"
	@echo ""
	@echo "Created $(ZIP) ($$(du -h $(ZIP) | cut -f1))"
	@echo "data/ and venv/ were excluded — the recipient runs 'make setup' themselves."
	@echo "artifacts/*/feature_table.parquet excluded too (large, EDA-only — nothing in"
	@echo "serving/ reads them; model.joblib + encoders + metrics are all still included,"
	@echo "so 'make serve' / 'make demo' work immediately without the raw dataset."

clean:
	rm -rf $(VENV) .pytest_cache dist
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
