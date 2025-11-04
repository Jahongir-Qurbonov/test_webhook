from pathlib import Path

import aiohttp

from .config import settings

COOKIE_JAR_PATH = Path(settings.COOKIE_FILE)


def load_cookies_from_file():
    loaded_jar = aiohttp.CookieJar()

    if not COOKIE_JAR_PATH.exists():
        COOKIE_JAR_PATH.parent.mkdir(parents=True, exist_ok=True)
        COOKIE_JAR_PATH.touch()
        print(f"Cookie jar file created at {COOKIE_JAR_PATH}")

        loaded_jar.save(COOKIE_JAR_PATH)
        return loaded_jar

    loaded_jar.load(COOKIE_JAR_PATH)
    print(f"Cookie jar loaded from {COOKIE_JAR_PATH}")
    return loaded_jar


def save_cookies_to_file(cookie_jar: aiohttp.CookieJar):
    cookie_jar.save(COOKIE_JAR_PATH)
    print(f"Cookie jar saved to {COOKIE_JAR_PATH}")
