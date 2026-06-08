PYTHON ?= python3
DATE := $(shell date +%Y-%m-%d)

.PHONY: validate test eval-layer1 eval-layer3 eval-layer3-all eval-layer3-summary eval-readme

validate:
	$(PYTHON) -m evals.harness.validate_prompts

test:
	$(PYTHON) -m pytest evals/harness/tests/ scripts/ -v

eval-layer1:
	$(PYTHON) -m evals.harness.run_eval --adapter $(ADAPTER) --layer 1 --write-results

# Single model, both configs
# Usage: make eval-layer3 MODEL=claude-sonnet-4-6
eval-layer3:
	@if [ -z "$(MODEL)" ]; then echo "Usage: make eval-layer3 MODEL=<model-id>"; exit 2; fi
	$(PYTHON) -m evals.harness.run_layer3 --models $(MODEL) --workers 4 --write-summary

# All three target models, both configs
eval-layer3-all:
	$(PYTHON) -m evals.harness.run_layer3 \
		--models claude-sonnet-4-6 claude-haiku-4-5 gpt-5.5 \
		--workers 4 --write-summary

# Re-aggregate already-written run files into summary.json
eval-layer3-summary:
	$(PYTHON) -c "from pathlib import Path; from evals.harness.runners.aggregate import aggregate_results; import json; d = Path('evals/results/$(DATE)/layer3'); s = aggregate_results(d); (d/'summary.json').write_text(json.dumps(s, indent=2)); print('Wrote', d/'summary.json')"

# Regenerate the README Layer 3 section from today's summary.json
eval-readme:
	$(PYTHON) scripts/update_readme_eval_table.py \
		--models claude-sonnet-4-6 claude-haiku-4-5 gpt-5.5
