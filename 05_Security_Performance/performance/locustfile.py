"""
Week 5 - Controlled performance experiment (TC-PERF-001..005).

Objective (set BEFORE execution): response time (avg, p95), throughput (req/s)
and error rate as virtual users increase.  Pass criterion: p95 < 1,000 ms and
0% errors for every request type.

Workload: each virtual user logs in once as perf_user (100 tasks seeded by
seed_perf_user.py), then with 1-2 s think time:
    60% GET /api/tasks   30% GET /api/dashboard   10% POST /api/tasks
Environment: Flask dev server (debug on), SQLite, load generator on the SAME
2-vCPU / 8 GB machine -> results show trends, not production capacity.

Run all levels:  bash run_performance.sh
"""
import os
import sys

from locust import HttpUser, between, task

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import qa_config as C  # noqa: E402

PERF_USER = os.environ.get("PERF_USER", "perf_user")


class TodoUser(HttpUser):
    host = C.BASE_URL
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post(C.API["login"], json={"username": PERF_USER, "password": C.PASSWORD},
                         name="POST /api/login")

    @task(6)
    def list_tasks(self):
        self.client.get(C.API["tasks"], name="GET /api/tasks")

    @task(3)
    def dashboard(self):
        self.client.get(C.API["dashboard"], name="GET /api/dashboard")

    @task(1)
    def create(self):
        self.client.post(C.API["tasks"], json={C.K_TITLE: "perf task"}, name="POST /api/tasks")
