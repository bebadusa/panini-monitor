#!/usr/bin/env python3
"""
Panini Treasure Box Verfügbarkeits-Bot
Prüft die Panini-CH-Produktseite und schickt einen Push via ntfy.sh,
sobald sich der Status von "Nicht lieferbar" auf verfügbar ändert.
"""

import os
import sys
from pathlib import Path

import requests

PRODUCT_URL = (
    "https://www.panini.ch/shp_che_de/"
    "official-fifa-world-cup-26-united-edition-sticker-collection-"
    "treasure-box-united-edition-005460cofchc-ch02.html"
)
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")
STATE_FILE = Path("last_status.txt")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "de-CH,de;q=0.9,en;q=0.8",
}


def check_availability():
    """Returns True if available, False if sold out, None if undetermined."""
    response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    html = response.text

    # Sanity-Check: Produktseite überhaupt geladen?
    if "Treasure Box" not in html:
        print("WARN: 'Treasure Box' nicht im HTML – Seite evtl. nicht geladen.")
        return None

    # "Nicht lieferbar" = ausverkauft
    if "Nicht lieferbar" in html:
        return False

    return True


def send_notification(topic, title, message):
    """Push via ntfy.sh."""
    requests.post(
        f"https://ntfy.sh/{topic}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": "urgent",
            "Tags": "moneybag,bell,soccer",
            "Click": PRODUCT_URL,
        },
        timeout=10,
    )


def main():
    if not NTFY_TOPIC:
        print("ERROR: NTFY_TOPIC env var nicht gesetzt")
        sys.exit(1)

    try:
        available = check_availability()
    except Exception as e:
        # Transient-Fehler nicht als Failure werten
        print(f"ERROR beim Fetch: {e}")
        sys.exit(0)

    if available is None:
        print("Status nicht ermittelbar – überspringe.")
        return

    last_status = (
        STATE_FILE.read_text().strip() if STATE_FILE.exists() else "unknown"
    )
    current_status = "available" if available else "unavailable"

    print(f"Last: {last_status} | Current: {current_status}")
    STATE_FILE.write_text(current_status)

    # Nur pushen, wenn Status von nicht-verfügbar → verfügbar wechselt
    if available and last_status != "available":
        print("VERFÜGBAR! Sende Push...")
        send_notification(
            NTFY_TOPIC,
            "Panini Treasure Box verfügbar!",
            "Die FIFA World Cup 26 United Edition Treasure Box ist "
            "jetzt im Panini-Shop verfügbar. Schnell zugreifen!",
        )
    elif available:
        print("Verfügbar, aber schon gemeldet – kein Push.")
    else:
        print("Nicht verfügbar.")


if __name__ == "__main__":
    main()
