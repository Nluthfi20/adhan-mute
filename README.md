<div align="center">

# adhan-mute

**Mute your music at prayer time.**

A small command-line tool that looks up your local adhan times and quiets
system audio — Spotify, YouTube, anything — for a few minutes at each
prayer, then hands your volume back.

[![CI](https://img.shields.io/github/actions/workflow/status/wailbentafat/adhan-mute/ci.yml?branch=main&label=CI)](https://github.com/wailbentafat/adhan-mute/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/wailbentafat/adhan-mute?label=release)](https://github.com/wailbentafat/adhan-mute/releases/latest)
[![License: MIT](https://img.shields.io/github/license/wailbentafat/adhan-mute)](LICENSE)
[![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-informational)](#install)
[![uv](https://img.shields.io/badge/packaging-uv-de5fe9)](https://docs.astral.sh/uv/)

[Website](https://wailbentafat.github.io/adhan-mute/) · [Releases](https://github.com/wailbentafat/adhan-mute/releases) · [Report an issue](https://github.com/wailbentafat/adhan-mute/issues)

</div>

---

```
$ adhan-mute
Detecting location...
Location: Algiers (36.7538, 3.0588)
Fetching today's prayer times...
Today's times: Fajr 05:15 · Dhuhr 12:44 · Asr 16:17 · Maghrib 18:59 · Isha 20:12
Next: Maghrib at 18:59 (in 42.0 min)
Maghrib — muting for 5 min.
Unmuted (restored volume to 35).
```

## Features

- **Zero setup** — detects your location via IP geolocation, no accounts or permissions
- **Accurate timing** — pulls daily prayer times from the [Aladhan API](https://aladhan.com/prayer-times-api)
- **Cross-platform** — native mute/restore on macOS, Windows, and Linux
- **Non-destructive** — remembers your exact volume and restores it afterward
- **No dependencies to run** — prebuilt binaries need nothing installed

## Install

### Option 1 — prebuilt binary (recommended)

Download the binary for your OS from the [latest release](https://github.com/wailbentafat/adhan-mute/releases/latest) and run it directly:

```bash
./adhan-mute-macos      # macOS
./adhan-mute-linux      # Linux
adhan-mute-windows.exe  # Windows
```

### Option 2 — from source, with [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/wailbentafat/adhan-mute
cd adhan-mute
uv sync
uv run main.py
```

Linux also needs `alsa-utils` installed (provides `amixer`) — usually preinstalled.

## Usage

```bash
adhan-mute --mute-minutes 5 --poll-seconds 60
```

| Flag | Description | Default |
|---|---|---|
| `--mute-minutes` | How long to keep audio muted at each prayer time | `5` |
| `--poll-seconds` | How often to check the clock while waiting | `60` |

Leave it running in a terminal, or set it up as a background service (see below).

## How it works

1. Detects your approximate location via IP geolocation (`ip-api.com`).
2. Fetches today's five prayer times for that location from the Aladhan API.
3. Waits until the next prayer time.
4. Mutes system volume, waits `--mute-minutes`, then restores your previous volume.
5. Repeats daily.

## Running in the background

**macOS/Linux** — run under `nohup`, or set up a `launchd`/`systemd` user service.

**Windows** — schedule it via Task Scheduler at login, or leave the terminal open.

## Development

```bash
git clone https://github.com/wailbentafat/adhan-mute
cd adhan-mute
uv sync
uv run main.py
```

CI runs on `ubuntu-latest`, `macos-latest`, and `windows-latest` on every push. Tagging a release (`git tag vX.Y.Z && git push origin vX.Y.Z`) builds and publishes a standalone binary for each OS via [PyInstaller](https://pyinstaller.org/).

## License

[MIT](LICENSE)
