# adhan-mute

CLI that fetches your local adhan (prayer) times and mutes system audio (Spotify, YouTube, anything) for a few minutes at each prayer time, so you can hear the call to prayer.

Works on macOS, Windows, and Linux.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

`pycaw`/`comtypes` (Windows-only, for volume control) install automatically on Windows via `uv sync`, and are skipped elsewhere.
Linux also needs `alsa-utils` installed (provides `amixer`) — usually present by default.

## Run

```bash
uv run main.py
```

Options:

```bash
uv run main.py --mute-minutes 5 --poll-seconds 60
```

- `--mute-minutes`: how long to keep audio muted at each prayer time (default 5)
- `--poll-seconds`: how often to check the clock while waiting (default 60)

Leave it running in a terminal, or set it up as a background service (see below).

## How it works

1. Detects your location via IP geolocation (`ip-api.com`, no key needed).
2. Fetches today's 5 prayer times from the Aladhan API for that location.
3. Sleeps until the next prayer time.
4. Mutes system volume, waits `--mute-minutes`, restores your previous volume.
5. Repeats, refetching times daily.

## Run in the background

**macOS/Linux** — run under `nohup` or a simple `launchd`/`systemd` user service.

**Windows** — run via Task Scheduler at login, or just leave the terminal open.
