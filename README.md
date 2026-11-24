# Astro Tarot

A tarot and astrology learning site built with Django. Browse all 78 cards, explore the zodiac, and try one-, three-, or five-card reflective readings. The separate Yes / No reading draws one upright card.

## Run locally

```powershell
git clone https://github.com/sivagrr/astro-tarot.git
cd astro-tarot
uv venv
uv pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py runserver
```

Open http://127.0.0.1:8000/. Python 3.11+ is recommended. No account, API key, or external service is needed.

This repository is a local portfolio demo. Its default Django secret key and debug setting are for local development only. Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=0` before adapting it for deployment, and review Django's deployment checklist.

## Checks

```powershell
.venv\Scripts\python manage.py check
.venv\Scripts\python manage.py test
```

## How it works

- `tarot/data.py` defines the card library, spread positions, and zodiac guide.
- `tarot/card_meanings.json` holds the 78-card interpretation text used by the reading tool.
- `tarot/static/tarot/reading.js` draws distinct cards, tracks upright or reversed orientation, and builds the combined reflection in the browser. No question or reading is sent to a server or saved.

Readings are educational prompts, not predictions or professional advice. Card images are proportion-preserving WebP copies of the deck artwork supplied for this project.

The purple palette is shared across every page. Card faces use the supplied deck images in readings, the Card Library, and card details. The home hero uses original inline vector art with gentle orb and ring motion that stops when reduced motion is requested. No original card-back file was found with the supplied deck, so card backs use a matching CSS design.
