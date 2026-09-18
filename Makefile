PYTHON ?= python3

.PHONY: validate

validate:
	$(PYTHON) scripts/validate_skills.py --root .
