"""
Dashboard data service — generates realistic mock metrics and chart data.
Swap the return values here for real DB / API calls without touching the UI.
"""

import random
from datetime import datetime, timedelta


# ── KPI cards ────────────────────────────────────────────────────────────────

def get_kpis() -> dict:
    return {
        "orders":     {"value": random.randint(320, 420),  "delta": random.randint(-15, 25),  "unit": ""},
        "revenue":    {"value": random.randint(48000, 72000), "delta": random.randint(-3000, 8000), "unit": "€"},
        "shipments":  {"value": random.randint(80, 140),   "delta": random.randint(-10, 20),  "unit": ""},
        "throughput": {"value": random.randint(88, 99),    "delta": round(random.uniform(-2, 3), 1), "unit": "%"},
    }


# ── Revenue line chart — last 30 days ────────────────────────────────────────

def get_revenue_series() -> dict:
    days = [(datetime.today() - timedelta(days=29 - i)).strftime("%d %b") for i in range(30)]
    revenue  = [round(random.uniform(1200, 3800), 0) for _ in range(30)]
    forecast = [None] * 25 + [round(random.uniform(2000, 4000), 0) for _ in range(5)]
    return {"days": days, "revenue": revenue, "forecast": forecast}


# ── Order status donut ────────────────────────────────────────────────────────

def get_order_status() -> list[dict]:
    shipped    = random.randint(120, 180)
    pending    = random.randint(40, 80)
    processing = random.randint(30, 60)
    cancelled  = random.randint(5, 20)
    return [
        {"name": "Shipped",    "value": shipped},
        {"name": "Pending",    "value": pending},
        {"name": "Processing", "value": processing},
        {"name": "Cancelled",  "value": cancelled},
    ]


# ── Daily orders bar — last 7 days ───────────────────────────────────────────

def get_daily_orders() -> dict:
    days = [(datetime.today() - timedelta(days=6 - i)).strftime("%a") for i in range(7)]
    completed = [random.randint(30, 70) for _ in range(7)]
    returned  = [random.randint(1, 10)  for _ in range(7)]
    return {"days": days, "completed": completed, "returned": returned}


# ── Production throughput area — last 24 h ───────────────────────────────────

def get_throughput_series() -> dict:
    hours  = [f"{i:02d}:00" for i in range(24)]
    actual = [round(random.uniform(70, 98), 1) for _ in range(24)]
    target = [92.0] * 24
    return {"hours": hours, "actual": actual, "target": target}
