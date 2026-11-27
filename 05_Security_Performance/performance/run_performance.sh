#!/usr/bin/env bash
# Runs TC-PERF-001..005. Start the app first in another terminal: cd app && python app.py
set -e
cd "$(dirname "$0")"
mkdir -p results
python seed_perf_user.py
for u in 1 10 25 50; do                               # load levels, all users start at once
  locust -f locustfile.py --headless -u $u -r $u -t 40s --csv results/u$u --only-summary
done
locust -f locustfile.py --headless -u 100 -r 10 -t 40s --csv results/u100 --only-summary   # stress, ramp 10/s
python summarise_results.py
