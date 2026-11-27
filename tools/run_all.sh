#!/usr/bin/env bash
# Runs every non-UI suite with coverage, then rebuilds all documents from the results.
set -u
cd "$(dirname "$0")/.."
mkdir -p reports
pytest -m "not ui" --junitxml=reports/junit_all.xml \
       --cov=app --cov=helpers --cov-branch \
       --cov-report=term --cov-report=html:02_White_Box_Coverage/coverage_html | tee reports/pytest_all.log
pytest -m "regression and not ui" -q --junitxml=reports/junit_regression.xml | tee reports/pytest_regression.log
python tools/build_documents.py
echo "Done. Failing tests above are the known defects (DEF-xxx). Logs in reports/."
