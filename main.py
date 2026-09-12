"""Adhan-mute CLI: mutes system audio during prayer time so you can hear the adhan."""
import time
import argparse
from datetime import datetime, timedelta

from location import get_location
from prayer_times import get_today_times, next_prayer
from mute import mute, unmute, get_current_volume


def run(mute_minutes: int, poll_seconds: int):
    print("Detecting location...")
    loc = get_location()
    print(f"Location: {loc['city']} ({loc['lat']:.4f}, {loc['lon']:.4f})")

    times = None
    fetched_date = None

    while True:
        now = datetime.now()
        if fetched_date != now.date():
            print("Fetching today's prayer times...")
            times = get_today_times(loc["lat"], loc["lon"])
            fetched_date = now.date()
            print(f"Today's times: {times}")

        nxt = next_prayer(times, now)
        if nxt is None:
            # all prayers passed today; sleep until midnight then refetch
            tomorrow = (now + timedelta(days=1)).replace(
                hour=0, minute=1, second=0, microsecond=0
            )
            sleep_s = (tomorrow - now).total_seconds()
            print(f"All prayers done for today. Sleeping {sleep_s/3600:.1f}h until refetch.")
            time.sleep(sleep_s)
            continue

        name, when = nxt
        wait_s = (when - now).total_seconds()
        print(f"Next: {name} at {when.strftime('%H:%M')} (in {wait_s/60:.1f} min)")

        if wait_s > poll_seconds:
            time.sleep(poll_seconds)
            continue

        if wait_s > 0:
            time.sleep(wait_s)

        original_volume = get_current_volume()
        print(f"{name} — muting for {mute_minutes} min.")
        mute()
        time.sleep(mute_minutes * 60)
        unmute(original_volume)
        print(f"Unmuted (restored volume to {original_volume}).")


def main():
    parser = argparse.ArgumentParser(description="Mute system audio at adhan time.")
    parser.add_argument(
        "--mute-minutes", type=int, default=5, help="How long to keep audio muted (default: 5)"
    )
    parser.add_argument(
        "--poll-seconds",
        type=int,
        default=60,
        help="How often to check the clock while waiting (default: 60)",
    )
    args = parser.parse_args()
    run(args.mute_minutes, args.poll_seconds)


if __name__ == "__main__":
    main()
