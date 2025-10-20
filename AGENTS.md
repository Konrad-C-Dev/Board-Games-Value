
# AGENTS.md — Projekt Scraper gier planszowych (aleplanszowki.pl)

## 🎯 Cel projektu
Celem projektu jest stworzenie aplikacji umożliwiającej legalne, etyczne i wydajne pobieranie danych o grach planszowych z serwisu **aleplanszowki.pl**. Dane będą wykorzystywane wyłącznie w celach edukacyjnych i analitycznych, z poszanowaniem zasad robots.txt oraz dobrych praktyk scrapingowych.

---

## 🧩 Architektura systemu
Aplikacja składa się z modułów backendowych (scraper, baza danych, API) i frontendowych (dashboard do wizualizacji).

### Backend:
- **`scraper/`**
  - `base_scraper.py` – zarządza logiką pobierania, parsowania i zapisu danych.
  - `aleplanszowki_scraper.py` – specyficzna implementacja dla strony aleplanszowki.pl.
  - `selectors.py` – selektory CSS / XPath dla kluczowych elementów strony (nazwa, cena, link, zdjęcie, kategoria).
- **`db/`**
  - `models.py` – modele SQLAlchemy (tabele: gry, kategorie, historia_cen).
  - `database.py` – konfiguracja bazy SQLite i sesji ORM.
- **`api/`**
  - `main.py` – FastAPI endpointy (pobieranie, filtrowanie, aktualizacja danych).
- **`utils/`**
  - `robot_check.py` – sprawdzanie robots.txt (urllib.robotparser).
  - `logging_config.py` – konfiguracja loggera.
  - `scheduler.py` – harmonogram aktualizacji (schedule lub APScheduler).

### Frontend:
- **React / Next.js / Streamlit** – do wizualizacji danych.
  - Widoki: lista gier, szczegóły gry, porównanie cen, trendy.
  - Integracja z REST API z backendu.

---

## ⚙️ Narzędzia i biblioteki

### Core (MVP):
```
requests
beautifulsoup4
lxml
python-dotenv
requests-cache
tenacity
SQLAlchemy
schedule
pandas
pytest
```

### Opcjonalne (rozszerzenia):
```
playwright  # dynamiczne strony JS
httpx       # async requests
selectolax  # szybki parser HTML
fake-useragent
black, isort, pre-commit  # formatowanie kodu
```

---

## 🧠 Zasady działania scrapera
1. **Zgodność z robots.txt**  
   - Przed wykonaniem requesta, scraper używa `urllib.robotparser` do weryfikacji, czy dany URL może być crawlowany.
2. **User-Agent**  
   - Wysyłany w nagłówkach jako np. `"DataScienceScraperBot/1.0 (+kontakt@example.com)"`.
3. **Rate limiting i opóźnienia**  
   - Każde zapytanie odczekuje losowo 1–3 s (`time.sleep(random.uniform(1,3))`).
   - Retry/backoff na błędach HTTP 429 i 5xx (`tenacity`).
4. **Cache HTTP**  
   - `requests-cache` przechowuje odpowiedzi lokalnie podczas developmentu.
5. **Logowanie**  
   - Wykorzystanie modułu `logging`, poziomy INFO/ERROR.
6. **Struktura danych**  
   - Każda gra zawiera: `id`, `tytuł`, `link`, `cena`, `dostępność`, `obrazek`, `kategoria`, `timestamp`.

---

## 🧱 Struktura projektu
```
project_root/
│
├── scraper/
│   ├── base_scraper.py
│   ├── aleplanszowki_scraper.py
│   └── selectors.py
│
├── db/
│   ├── models.py
│   └── database.py
│
├── api/
│   └── main.py
│
├── utils/
│   ├── robot_check.py
│   ├── logging_config.py
│   └── scheduler.py
│
├── tests/
│   └── test_scraper.py
│
├── .env
├── requirements.txt
├── README.md
└── AGENTS.md
```

---

## 🧰 Zadania dla agenta AI (Backend)

### `base_scraper.py`
- Utwórz klasę `BaseScraper` z metodami:
  - `fetch_html(url: str) -> str`
  - `parse_page(html: str) -> dict`
  - `save_to_db(data: dict)`
- Użyj `requests`, `BeautifulSoup` i `SQLAlchemy`.
- Uwzględnij logowanie, opóźnienia, retry.

### `aleplanszowki_scraper.py`
- Dziedziczy po `BaseScraper`.
- W `parse_page()` znajdź selektory:
  - nazwa gry (`.product-title` lub `h1[itemprop='name']`),
  - cena (`.price` lub `meta[itemprop='price']`),
  - dostępność (`.product-availability`),
  - obraz (`img[itemprop='image']`),
  - link (`meta[property='og:url']`).
- Zapisz dane w formacie JSON i/lub do SQLite.

### `database.py`
- Inicjalizuj bazę SQLite (`games.db`).
- Funkcja `get_session()`.

### `models.py`
- Klasy: `Game`, `Category`, `PriceHistory`.
- Pola: `id`, `name`, `url`, `price`, `availability`, `image_url`, `category_id`, `created_at`.

### `robot_check.py`
- Funkcja `is_allowed(url: str) -> bool` korzystająca z `urllib.robotparser`.

### `scheduler.py`
- Automatyczne uruchamianie scrapera np. co 12 godzin.

---

## 💻 Zadania dla agenta AI (Frontend)
- Stworzyć dashboard (React / Streamlit / Next.js) umożliwiający:
  - Przegląd gier (nazwa, cena, dostępność, miniaturka).
  - Filtrowanie po kategorii i przedziale cenowym.
  - Wykres historii cen (`recharts` / `plotly`).
  - Endpoint `/api/games` z backendu jako źródło danych.

---

## ✅ Dobre praktyki
1. Nie rób zbyt wielu requestów naraz.
2. Używaj cache podczas testów.
3. Stosuj `.env` do danych konfiguracyjnych.
4. Utrzymuj strukturę projektu czytelną (modularność).
5. Testuj mockami (`pytest + responses/vcrpy`).
6. Każdy moduł powinien mieć docstring i logging.
7. Wersjonuj kod w Git (branch `dev`, PR do `main`).

---

## 📅 Etapy realizacji
1. Przygotowanie środowiska (Python, venv, instalacja pakietów).
2. Implementacja `BaseScraper` i `robot_check`.
3. Testy jednostkowe na pojedynczym URL.
4. Dodanie ORM i zapis danych.
5. Dodanie REST API (FastAPI).
6. Stworzenie prostego dashboardu (Streamlit lub React).
7. Dokumentacja i deployment (Docker, GitHub Actions).

---

## 📜 Licencja i etyka
Projekt ma charakter **edukacyjny**. Dane nie będą wykorzystywane komercyjnie.  
Należy przestrzegać zasad **robots.txt**, nie przeciążać serwera oraz oznaczać scraper odpowiednim User-Agentem.
