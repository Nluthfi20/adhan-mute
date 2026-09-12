"""Cross-platform system volume mute/restore."""
import platform
import subprocess

SYSTEM = platform.system()  # "Darwin", "Windows", "Linux"


def mute():
    if SYSTEM == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output volume 0"], check=True)
    elif SYSTEM == "Windows":
        _windows_set_volume(0)
    elif SYSTEM == "Linux":
        subprocess.run(["amixer", "-q", "set", "Master", "mute"], check=False)
    else:
        raise RuntimeError(f"Unsupported OS: {SYSTEM}")


def unmute(restore_volume: int = 50):
    if SYSTEM == "Darwin":
        subprocess.run(
            ["osascript", "-e", f"set volume output volume {restore_volume}"], check=True
        )
    elif SYSTEM == "Windows":
        _windows_set_volume(restore_volume)
    elif SYSTEM == "Linux":
        subprocess.run(["amixer", "-q", "set", "Master", "unmute"], check=False)
    else:
        raise RuntimeError(f"Unsupported OS: {SYSTEM}")


def get_current_volume() -> int:
    """Best-effort read of current volume (0-100) so we can restore it later."""
    if SYSTEM == "Darwin":
        out = subprocess.run(
            ["osascript", "-e", "output volume of (get volume settings)"],
            check=True,
            capture_output=True,
            text=True,
        )
        return int(out.stdout.strip())
    elif SYSTEM == "Windows":
        return _windows_get_volume()
    elif SYSTEM == "Linux":
        return 50  # amixer mute/unmute preserves the underlying level; no read needed
    else:
        raise RuntimeError(f"Unsupported OS: {SYSTEM}")


def _windows_set_volume(level: int):
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    except ImportError as e:
        raise RuntimeError(
            "Windows volume control requires 'pycaw' and 'comtypes'. "
            "Install with: pip install pycaw comtypes"
        ) from e
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)


def _windows_get_volume() -> int:
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    except ImportError as e:
        raise RuntimeError(
            "Windows volume control requires 'pycaw' and 'comtypes'. "
            "Install with: pip install pycaw comtypes"
        ) from e
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return round(volume.GetMasterVolumeLevelScalar() * 100)
