# Astro Tarot

A calm tarot and astrology learning site built with Django. Explore all 78 cards, study three spreads, and try an interactive sample reading. The reading uses the supplied 78-card meanings export and deck images.

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

The content is educational and reflective. Readings are randomly drawn, stay in your browser, and are not professional advice. The Tarot Techs reference project was not changed. The card images in this project are resized WebP copies of the user-provided deck files; original proportions are preserved.

The purple palette is shared across every page. Card faces use the supplied deck images in readings, the Card Library, and card details. The home hero uses original inline vector art with gentle orb and ring motion that stops when reduced motion is requested. No original card-back file was found with the supplied deck, so card backs use a matching CSS design.
