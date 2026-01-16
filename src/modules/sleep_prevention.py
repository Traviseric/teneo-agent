"""
Sleep prevention for Teneo Agent.

Keeps the computer awake during overnight runs.
"""

import sys
from typing import Optional

from .logging_utils import log


class SleepPrevention:
    """
    Context manager for preventing system sleep.

    Usage:
        with SleepPrevention():
            # Computer won't sleep during this block
            do_work()
    """

    def __init__(self):
        self._previous_state = None

    def __enter__(self):
        prevent_sleep()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        allow_sleep()
        return False


def prevent_sleep() -> bool:
    """
    Prevent system from sleeping.

    Windows: Uses SetThreadExecutionState
    macOS: Uses caffeinate (spawns background process)
    Linux: Uses systemd-inhibit or xdg-screensaver

    Returns True if successful.
    """
    if sys.platform == "win32":
        return _prevent_sleep_windows()
    elif sys.platform == "darwin":
        return _prevent_sleep_macos()
    else:
        return _prevent_sleep_linux()


def allow_sleep() -> bool:
    """
    Allow system to sleep again.

    Returns True if successful.
    """
    if sys.platform == "win32":
        return _allow_sleep_windows()
    elif sys.platform == "darwin":
        return _allow_sleep_macos()
    else:
        return _allow_sleep_linux()


# ============================================================================
# Windows Implementation
# ============================================================================

_ES_CONTINUOUS = 0x80000000
_ES_SYSTEM_REQUIRED = 0x00000001
_ES_DISPLAY_REQUIRED = 0x00000002


def _prevent_sleep_windows() -> bool:
    """Prevent sleep on Windows using SetThreadExecutionState."""
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(
            _ES_CONTINUOUS | _ES_SYSTEM_REQUIRED | _ES_DISPLAY_REQUIRED
        )
        log("[SLEEP] Preventing system sleep (Windows)")
        return True
    except Exception as e:
        log(f"[WARN] Could not prevent sleep: {e}")
        return False


def _allow_sleep_windows() -> bool:
    """Allow sleep on Windows."""
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(_ES_CONTINUOUS)
        log("[SLEEP] Allowing system sleep (Windows)")
        return True
    except Exception:
        return False


# ============================================================================
# macOS Implementation
# ============================================================================

_caffeinate_process: Optional[object] = None


def _prevent_sleep_macos() -> bool:
    """Prevent sleep on macOS using caffeinate."""
    global _caffeinate_process
    try:
        import subprocess
        _caffeinate_process = subprocess.Popen(
            ["caffeinate", "-i", "-w", str(subprocess.os.getpid())],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log("[SLEEP] Preventing system sleep (macOS caffeinate)")
        return True
    except Exception as e:
        log(f"[WARN] Could not prevent sleep: {e}")
        return False


def _allow_sleep_macos() -> bool:
    """Allow sleep on macOS."""
    global _caffeinate_process
    if _caffeinate_process:
        try:
            _caffeinate_process.terminate()
            _caffeinate_process = None
            log("[SLEEP] Allowing system sleep (macOS)")
            return True
        except Exception:
            pass
    return False


# ============================================================================
# Linux Implementation
# ============================================================================

_inhibit_process: Optional[object] = None


def _prevent_sleep_linux() -> bool:
    """Prevent sleep on Linux using systemd-inhibit."""
    global _inhibit_process
    try:
        import subprocess
        import shutil

        # Try systemd-inhibit first
        if shutil.which("systemd-inhibit"):
            _inhibit_process = subprocess.Popen(
                [
                    "systemd-inhibit",
                    "--what=idle:sleep",
                    "--who=teneo-agent",
                    "--why=Overnight agent run",
                    "sleep", "infinity"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            log("[SLEEP] Preventing system sleep (systemd-inhibit)")
            return True

        # Fallback: try xdg-screensaver
        if shutil.which("xdg-screensaver"):
            subprocess.run(
                ["xdg-screensaver", "suspend", str(subprocess.os.getpid())],
                capture_output=True
            )
            log("[SLEEP] Preventing screensaver (xdg-screensaver)")
            return True

        log("[WARN] No sleep prevention method available on Linux")
        return False

    except Exception as e:
        log(f"[WARN] Could not prevent sleep: {e}")
        return False


def _allow_sleep_linux() -> bool:
    """Allow sleep on Linux."""
    global _inhibit_process
    if _inhibit_process:
        try:
            _inhibit_process.terminate()
            _inhibit_process = None
            log("[SLEEP] Allowing system sleep (Linux)")
            return True
        except Exception:
            pass
    return False
