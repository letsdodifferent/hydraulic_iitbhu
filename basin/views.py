from django.shortcuts import render
import json
from datetime import date, timedelta
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

def page(request):
    return render(request, "basin.html")

def build_day_list_range(start_iso_date, end_iso_date):
    """
    Build list of daily dates (YYYY-MM-DD) between start_iso_date and end_iso_date (inclusive).
    """
    try:
        s_year, s_month, s_day = map(int, start_iso_date.split("-"))
        e_year, e_month, e_day = map(int, end_iso_date.split("-"))
        start = date(s_year, s_month, s_day)
        end = date(e_year, e_month, e_day)
    except Exception:
        return []

    if end < start:
        return []

    days = []
    cur = start
    while cur <= end:
        days.append(cur.isoformat())
        cur += timedelta(days=1)
    return days

# Placeholder model inference
def predict_with_model(lat, lon, dates_iso_list, location_id):
    """
    Replace with your real DL model.
    dates_iso_list: ['YYYY-MM-DD', ...] (daily)
    """
    import math, random
    n = len(dates_iso_list)
    ph = [7.0 + 0.25 * math.sin(i/10.0) + random.uniform(-0.12, 0.12) for i in range(n)]
    do = [6.0 + 0.6 * math.cos(i/12.0) + random.uniform(-0.2, 0.2) for i in range(n)]
    tss = [40.0 + 9.0 * math.sin(i/15.0) + random.uniform(-3, 3) for i in range(n)]

    ph = [round(v, 3) for v in ph]
    do = [round(max(0.0, v), 3) for v in do]
    tss = [round(max(0.0, v), 3) for v in tss]
    return ph, do, tss

@require_POST
def water_predict(request):
    """
    Expects JSON:
    {
      "location_id": "assi_ghat",
      "lat": 25.2950,
      "lon": 83.0105,
      "start_date": "2025-01-10",
      "end_date": "2025-01-25"
    }

    Returns daily predictions:
      { "dates": ["2025-01-10", "2025-01-11", ...],
        "ph": [...], "do": [...], "tss": [...] }
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    location_id = body.get("location_id")
    lat = body.get("lat")
    lon = body.get("lon")
    start_date = body.get("start_date")  # 'YYYY-MM-DD'
    end_date = body.get("end_date")      # 'YYYY-MM-DD'

    if not all([location_id, lat is not None, lon is not None, start_date, end_date]):
        return HttpResponseBadRequest("Missing required parameters")

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid lat/lon")

    dates = build_day_list_range(start_date, end_date)
    if not dates:
        return HttpResponseBadRequest("Invalid date range (end date earlier than start date?)")

    ph_vals, do_vals, tss_vals = predict_with_model(lat, lon, dates, location_id)

    if not (len(dates) == len(ph_vals) == len(do_vals) == len(tss_vals)):
        return HttpResponseBadRequest("Model output length mismatch")

    return JsonResponse({
        "dates": dates,
        "ph": ph_vals,
        "do": do_vals,
        "tss": tss_vals,
    })
