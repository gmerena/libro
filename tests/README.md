# Libro API Tesztek

Ez a mappa tartalmazza a Libro könyvtár API automatizált tesztjeit.

## Tesztek futtatása

### Telepítés

Először telepítsd a dev függőségeket:

```bash
uv sync --dev
```

### Tesztek futtatása

Összes teszt futtatása:
```bash
uv run pytest
```

Specifikus teszt fájl futtatása:
```bash
uv run pytest tests/test_api.py
```

Részletes kimenet:
```bash
uv run pytest -v
```

Coverage jelentés:
```bash
uv run pytest --cov=app --cov-report=html
```

## Teszt struktúra

- `conftest.py` - Pytest fixtures és konfiguráció
- `test_api.py` - API alapvető tesztek (root endpoint)
- `test_members.py` - Tagok végpont tesztek
- `test_books.py` - Könyvek végpont tesztek
- `test_loans.py` - Kölcsönzések végpont tesztek

## Teszt kategóriák

### API Tesztek (`test_api.py`)
- Root endpoint elérhetőség
- Verzió információ
- Elérhető végpontok listája

### Members Tesztek (`test_members.py`)
- Tagok listázása (üres adatbázis)
- Lapozás működése
- Nem létező tag lekérése
- Érvénytelen email validáció

### Books Tesztek (`test_books.py`)
- Könyvek listázása
- Lapozás működése
- Elérhető könyvek szűrése
- Keresés cím szerint
- Keresés szerző szerint
- Nem létező könyv lekérése
- Érvénytelen ISBN validáció

### Loans Tesztek (`test_loans.py`)
- Kölcsönzések listázása
- Aktív kölcsönzések szűrése
- Tagok kölcsönzési előzményei
- Könyvek kölcsönzési előzményei
- Lejárt kölcsönzések
- Nem létező kölcsönzés lekérése
- Érvénytelen kölcsönzés létrehozása

## Megjegyzések

- A tesztek async módon futnak (`pytest-asyncio`)
- HTTPX `AsyncClient` használata a végpontok teszteléséhez
- A tesztek nem módosítanak valós adatbázist (mock/test DB szükséges produkciós használathoz)
- Minden teszt függetlenül futtatható