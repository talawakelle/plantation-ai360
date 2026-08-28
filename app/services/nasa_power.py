from datetime import datetime
import requests
from app.core.config import get_settings

PARAMETERS = "PRECTOTCORR,T2M_MIN,T2M_MAX,T2M,RH2M,ALLSKY_SFC_SW_DWN,WS2M"


def fetch_daily(lat: float, lon: float, start: str, end: str) -> list[dict]:
    settings = get_settings()
    params = {
        "parameters": PARAMETERS,
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    response = requests.get(settings.nasa_power_base_url, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    p = payload.get("properties", {}).get("parameter", {})
    dates = sorted(set().union(*(v.keys() for v in p.values() if isinstance(v, dict))))
    out = []
    for d in dates:
        def clean(name):
            value = p.get(name, {}).get(d)
            if value in (-999, -999.0, None):
                return None
            return value
        out.append({
            "record_date": datetime.strptime(d, "%Y%m%d").date(),
            "rainfall_mm": clean("PRECTOTCORR"),
            "temp_min_c": clean("T2M_MIN"),
            "temp_max_c": clean("T2M_MAX"),
            "temp_mean_c": clean("T2M"),
            "humidity_pct": clean("RH2M"),
            "solar_mj_m2": clean("ALLSKY_SFC_SW_DWN"),
            "wind_m_s": clean("WS2M"),
        })
    return out
