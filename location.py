"""Resolve the machine's approximate location via IP geolocation."""
import urllib.request
import json


def get_location() -> dict:
    """Return {"lat": float, "lon": float, "city": str, "timezone": str}."""
    req = urllib.request.Request(
        "http://ip-api.com/json/",
        headers={"User-Agent": "adhan-mute/1.0"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    if data.get("status") != "success":
        raise RuntimeError(f"Location lookup failed: {data}")
    return {
        "lat": data["lat"],
        "lon": data["lon"],
        "city": data.get("city", "unknown"),
        "timezone": data.get("timezone", "UTC"),
    }


if __name__ == "__main__":
    print(get_location())
