# Panini Treasure Box Verfügbarkeits-Bot

Überwacht die Panini-CH-Seite alle 10 Minuten und schickt einen Push aufs Handy, sobald die Box wieder verfügbar ist. Läuft komplett kostenlos auf GitHub Actions.

## Setup (ca. 5 Minuten)

### 1. GitHub Repo anlegen

- Auf [github.com](https://github.com) einloggen (oder Account erstellen)
- Oben rechts **"+" → "New repository"**
- Name z.B. `panini-monitor`
- **Private** wählen
- "Create repository"

### 2. Dateien hochladen

Im neuen Repo:

- **"Add file" → "Upload files"**
- `monitor.py` reinziehen → "Commit changes"
- Dann **"Add file" → "Create new file"** klicken
- Als Dateinamen **`.github/workflows/monitor.yml`** eingeben (die Slashes erzeugen die Ordner automatisch)
- Inhalt von `monitor.yml` reinkopieren → "Commit changes"

### 3. ntfy.sh einrichten

- App **"ntfy"** auf dem Handy installieren:
  - iOS: App Store → "ntfy"
  - Android: Play Store → "ntfy"
- App öffnen → **"+"** → einen **geheimen Topic-Namen** wählen
  - z.B. `panini-david-x9k2m7q4n8` (irgendwas Zufälliges)
  - **Wichtig:** Topic muss schwer zu erraten sein, sonst kann jeder dir Pushes schicken
- "Subscribe"

### 4. Topic als GitHub Secret speichern

- Im Repo: **Settings → Secrets and variables → Actions**
- **"New repository secret"**
- Name: `NTFY_TOPIC`
- Secret: dein Topic-Name (z.B. `panini-david-x9k2m7q4n8`)
- "Add secret"

### 5. Schreibrechte für den Workflow

- Im Repo: **Settings → Actions → General**
- Runterscrollen zu **"Workflow permissions"**
- **"Read and write permissions"** auswählen
- "Save"

### 6. Testen

- Im Repo: **Actions Tab**
- Wenn ein Warnhinweis erscheint ("Workflows aren't being run on this forked repository"), auf "I understand my workflows" klicken
- Links: **"Panini Treasure Box Monitor"** anklicken
- Rechts: **"Run workflow" → "Run workflow"**
- Nach ~30 Sekunden grünes Häkchen → läuft

Ab jetzt läuft der Check alle 10 Minuten automatisch.

## Funktionsweise

- Holt alle 10 Min die Produktseite und prüft, ob "Nicht lieferbar" noch dasteht
- Speichert den letzten Status in `last_status.txt` im Repo
- Push wird **nur einmal** geschickt, wenn der Status von ausverkauft → verfügbar wechselt
- Push hat höchste Priorität und einen Click-Through-Link direkt zur Produktseite

## Hinweise

- GitHub Actions cron kann **5–15 Min Verzögerung** haben (besonders zu Stosszeiten) – ist normal
- Free tier reicht easy: ~144 Run-Minuten/Monat von 2000 verfügbaren
- Wenn die Box auftaucht: **schnell sein** – limitierte Auflage von 5000 Stück, andere Bots gibt's sicher auch
- Topic-Namen niemandem verraten

## Wenn was nicht klappt

- Actions Tab → den fehlgeschlagenen Run anklicken → Logs lesen
- Häufigste Probleme: Secret falsch geschrieben (`NTFY_TOPIC`), oder Workflow-Permissions nicht auf "Read and write"
