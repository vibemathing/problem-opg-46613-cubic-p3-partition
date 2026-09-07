.PHONY: check check-full

check:
	python3 scripts/validate_mathematical_reasoning_discipline.py --project-root .
	python3 scripts/validate_web_problem_harness.py --project-root .
	python3 scripts/validate_web_attempt.py --project-root . --all-inbox
	python3 scripts/validate_math_knowledge_registry.py --project-root .
	python3 scripts/validate_obligation_graphs.py --project-root .

check-full: check
	python3 scripts/test_obligation_harness.py
