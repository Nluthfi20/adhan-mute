"""Fetch today's prayer (adhan) times from the Aladhan API."""
import urllib.request
import urllib.parse
import json
from datetime import datetime

PRAYER_NAMES = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]


def get_today_times(lat: float, lon: float, method: int = 2) -> dict:
    """Return {"Fajr": "05:12", "Dhuhr": "13:05", ...} in 24h local time (HH:MM)."""
    params = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "method": method})
    url = f"https://api.aladhan.com/v1/timings?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    timings = data["data"]["timings"]
    return {name: timings[name].split(" ")[0] for name in PRAYER_NAMES}


def next_prayer(times: dict, now: datetime | None = None):
    """Return (name, datetime) of the next upcoming prayer today, or None if all passed."""
    now = now or datetime.now()
    today = now.date()
    upcoming = []
    for name, hhmm in times.items():
        hour, minute = map(int, hhmm.split(":"))
        dt = datetime(today.year, today.month, today.day, hour, minute)
        if dt > now:
            upcoming.append((name, dt))
    if not upcoming:
        return None
    return min(upcoming, key=lambda x: x[1])


if __name__ == "__main__":
    from location import get_location

    loc = get_location()
    times = get_today_times(loc["lat"], loc["lon"])
    print(times)
    print(next_prayer(times))
