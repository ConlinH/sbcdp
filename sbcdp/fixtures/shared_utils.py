"""Shared utility methods"""
import os
import pathlib
import platform
import sys
import time
from contextlib import suppress

import colorama

from . import constants


def pip_install(package, version=None):
    import fasteners
    import subprocess

    pip_install_lock = fasteners.InterProcessLock(
        constants.PipInstall.LOCKFILE
    )
    with pip_install_lock:
        if not version:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package]
            )
        else:
            package_and_version = package + "==" + str(version)
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_and_version]
            )


def is_arm_mac():
    """(M1 / M2 Macs use the ARM processor)"""
    return (
        "darwin" in sys.platform
        and (
            "arm" in platform.processor().lower()
            or "arm64" in platform.version().lower()
        )
    )


def is_mac():
    return "darwin" in sys.platform


def is_linux():
    return "linux" in sys.platform


def is_windows():
    return "win32" in sys.platform


def is_safari(driver):
    return driver.capabilities["browserName"].lower() == "safari"


def get_terminal_width():
    width = 80  # default
    try:
        width = os.get_terminal_size().columns
    except Exception:
        try:
            import shutil

            width = shutil.get_terminal_size((80, 20)).columns
        except Exception:
            pass
    return width


def fix_colorama_if_windows():
    if is_windows():
        colorama.just_fix_windows_console()


def fix_url_as_needed(url):
    if not url:
        url = "data:,"
    elif url.startswith("//"):
        url = "https:" + url
    elif ":" not in url:
        url = "https://" + url
    return url


def reconnect_if_disconnected(driver):
    if (
        hasattr(driver, "_is_using_uc")
        and driver._is_using_uc
        and hasattr(driver, "is_connected")
        and not driver.is_connected()
    ):
        with suppress(Exception):
            driver.connect()


def is_cdp_swap_needed(driver):
    """
    When someone is using CDP Mode with a disconnected webdriver,
    but they forget to reconnect before calling a webdriver method,
    this method is used to substitute the webdriver method for a
    CDP Mode method instead, which keeps CDP Stealth Mode enabled.
    For other webdriver methods, SeleniumBase will reconnect first.
    """
    return (
        hasattr(driver, "is_cdp_mode_active")
        and driver.is_cdp_mode_active()
        and hasattr(driver, "is_connected")
        and not driver.is_connected()
    )


def is_chrome_130_or_newer(self, binary_location=None):
    from ..core import detect_b_ver

    """Due to changes in Chrome-130, UC Mode freezes at start-up
    unless the user-data-dir already exists and is populated."""
    with suppress(Exception):
        if not binary_location:
            ver = detect_b_ver.get_browser_version_from_os("google-chrome")
        else:
            ver = detect_b_ver.get_browser_version_from_binary(
                binary_location
            )
        if ver and len(ver) > 3 and int(ver.split(".")[0]) >= 130:
            return True
    return False


def make_dir_files_writable(dir_path):
    # Make all files in the given directory writable.
    for file_path in pathlib.Path(dir_path).glob("*"):
        if file_path.is_file():
            mode = os.stat(file_path).st_mode
            mode |= (mode & 0o444) >> 1  # copy R bits to W
            with suppress(Exception):
                os.chmod(file_path, mode)


def make_writable(file_path):
    # Set permissions to: "If you can read it, you can write it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 1  # copy R bits to W
    os.chmod(file_path, mode)


def make_executable(file_path):
    # Set permissions to: "If you can read it, you can execute it."
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(file_path, mode)


def format_exc(exception, message):
    """Formats an exception message to make the output cleaner."""

    if exception is Exception:
        exc = Exception
        return exc, message
    elif isinstance(exception, str):
        exc = Exception
        message = "%s: %s" % (exception, message)
        return exc, message
    else:
        exc = Exception
        return exc, message
    # message = _format_message(message)
    # try:
    #     exc.message = message
    # except Exception:
    #     pass
    # return exc, message


def _format_message(message):
    message = "\n " + message
    return message

