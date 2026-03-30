# 🥗 Food Saving & Donation Platform — project_101

> O platformă care reduce risipa alimentară prin conectarea Restaurantelor și Comercianților cu ONG-uri și Voluntari individuali.

---

## 📋 Cuprins

1. [Contextul proiectului](#-contextul-proiectului)
2. [Arhitectura generală](#-arhitectura-generală)
3. [Roluri în aplicație](#-roluri-în-aplicație)
4. [Setup inițial (prima rulare)](#-setup-inițial-prima-rulare)
5. [Ghid Frontend](#-ghid-frontend)
6. [Ghid Backend](#-ghid-backend)
7. [Ghid Database](#-ghid-database)
8. [Workflow Git pentru echipă](#-workflow-git-pentru-echipă)
9. [Variabile de mediu](#-variabile-de-mediu)
10. [Troubleshooting](#-troubleshooting)

---

## 🌍 Contextul proiectului

Suntem 3 persoane care lucrăm împreună la o platformă de salvare și donație alimente. Scopul este să conectăm:

- **Comercianți** (restaurante, magazine) care au surplus de mâncare
- **ONG-uri / Centre de îngrijire** care colectează pentru cei în nevoie
- **Voluntari individuali** care ajută la distribuție

Platforma funcționează ca un marketplace în timp real: comercianții postează oferte, iar ONG-urile/voluntarii le revendică înainte de expirare.

### Tech stack

| Layer | Tehnologie | Port local |
|-------|-----------|------------|
| Frontend | React + Vite | `http://localhost:5173` |
| Backend | Python 3.12 + FastAPI | `http://localhost:8000` |
| Database | PostgreSQL + PostGIS | `localhost:5432` |

---

## 🏗 Arhitectura generală

```
project_101/
├── frontend/          # Aplicația React (Vite)
│   ├── src/
│   │   ├── components/    # Componente reutilizabile (butoane, carduri, etc.)
│   │   ├── pages/         # Paginile aplicației (Home, Login, Dashboard, etc.)
│   │   ├── assets/        # Imagini, fonturi, iconițe
│   │   └── App.jsx        # Entry point React, definire rute
│   ├── index.html
│   └── vite.config.js
│
├── backend/           # API-ul FastAPI
│   └── app/
│       ├── main.py        # Entry point FastAPI, înregistrare rute
│       ├── models/        # Modele SQLAlchemy (structura tabelelor din DB)
│       ├── schemas/       # Scheme Pydantic (validare request/response JSON)
│       ├── routers/       # Endpoint-urile API grupate pe funcționalitate
│       └── security/      # Autentificare JWT, hashing parole
│
├── database/          # Schema SQL inițială și migrații
│
├── .gitignore
├── pyrightconfig.json # Configurare type-checker Python
└── README.md
```

---

## 👥 Roluri în aplicație

| Rol | Ce poate face |
|-----|---------------|
| **Merchant** | Postează produse pentru donație sau la reducere, setează cantitate și dată expirare |
| **NGO / Care Center** | Revendică donații în bloc pentru beneficiarii lor |
| **Individual Volunteer** | Revendică donații individual și ajută la livrare |

---

## 🚀 Setup inițial (prima rulare)

### Cerințe prealabile

- **Node.js** ≥ 18 și **npm** ≥ 9
- **Python** 3.12
- **PostgreSQL** ≥ 14 cu extensia **PostGIS**
- **Git**

### 1. Clonează repo-ul

```bash
git clone https://github.com/madaleen/project_101.git
cd project_101
```

### 2. Pornește baza de date

```bash
# Dacă ai PostgreSQL instalat local:
psql -U postgres -c "CREATE DATABASE foodsave;"
psql -U postgres -d foodsave -c "CREATE EXTENSION postgis;"

# Aplică schema inițială:
psql -U postgres -d foodsave -f database/schema.sql
```

### 3. Pornește Backend-ul

```bash
cd backend

# Creează și activează virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# SAU
venv\Scripts\activate           # Windows

# Instalează dependențele
pip install -r requirements.txt

# Copiază și completează variabilele de mediu
cp .env.example .env
# Editează .env cu datele tale (vezi secțiunea Variabile de mediu)

# Pornește serverul
uvicorn app.main:app --reload
# API disponibil la: http://localhost:8000
# Documentație interactivă: http://localhost:8000/docs
```

### 4. Pornește Frontend-ul

```bash
cd frontend

# Instalează dependențele
npm install

# Pornește serverul de dezvoltare
npm run dev
# Aplicația disponibilă la: http://localhost:5173
```

---

## 🎨 Ghid Frontend

> **Când să folosești acest ghid:** Vrei să modifici aspectul aplicației, să adaugi o pagină nouă, să schimbi culori, layout, componente vizuale.

### Structura fișierelor relevante

```
frontend/src/
├── components/        ← Componente reutilizabile (NavBar, Card, Button, etc.)
├── pages/             ← O pagină = o rută în aplicație
├── assets/            ← Imagini, iconițe, fonturi
├── styles/ sau index.css ← Stiluri globale
└── App.jsx            ← Definirea rutelor (ce pagină se afișează la ce URL)
```

### Cum modific aspectul vizual?

#### Schimb culori / font / spațiere globală

Caută fișierul de stiluri global — de obicei `src/index.css` sau `src/App.css`:

```css
/* Exemplu: schimbă culoarea primară */
:root {
  --color-primary: #2e7d32;   /* verde închis */
  --color-accent: #ff7043;    /* portocaliu */
}
```

Dacă proiectul folosește **Tailwind CSS**, culorile se configurează în `tailwind.config.js`:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#2e7d32',
        accent: '#ff7043',
      }
    }
  }
}
```

#### Modific o componentă existentă (ex: cardul unui produs)

1. Găsește componenta în `src/components/` (ex: `ProductCard.jsx`)
2. Editează JSX-ul și clasele CSS direct
3. Salvează — Vite face **hot reload** automat, modificarea apare instant în browser

#### Adaug o pagină nouă

1. Creează fișierul în `src/pages/`:
   ```jsx
   // src/pages/AboutPage.jsx
   export default function AboutPage() {
     return <div>Despre noi</div>;
   }
   ```

2. Înregistrează ruta în `src/App.jsx`:
   ```jsx
   import AboutPage from './pages/AboutPage';

   // În lista de rute:
   <Route path="/about" element={<AboutPage />} />
   ```

3. Adaugă un link în NavBar sau oriunde e nevoie:
   ```jsx
   <Link to="/about">Despre noi</Link>
   ```

### Cum fac o cerere către API?

Cererile către backend se fac cu `fetch` sau `axios`. Exemplu:

```jsx
// Listează produsele disponibile
useEffect(() => {
  fetch('http://localhost:8000/api/v1/listings')
    .then(res => res.json())
    .then(data => setListings(data));
}, []);
```

> ⚠️ **Important:** Dacă primești erori CORS în browser, verifică că backend-ul are CORS configurat pentru `http://localhost:5173` (vezi secțiunea Backend).

### Build pentru producție

```bash
cd frontend
npm run build
# Fișierele generate sunt în frontend/dist/
```

---

## ⚙️ Ghid Backend

> **Când să folosești acest ghid:** Vrei să adaugi un endpoint nou, să modifici logica de business, să adaugi câmpuri noi în baza de date, să schimbi regulile de autentificare.

### Structura fișierelor relevante

```
backend/app/
├── main.py            ← Pornire FastAPI, înregistrare rute, CORS
├── models/            ← Structura tabelelor din baza de date
│   ├── user.py        ← Modelul User (merchant, ngo, volunteer)
│   ├── listing.py     ← Modelul Listing (un produs postat)
│   └── claim.py       ← Modelul Claim (o revendicare)
├── schemas/           ← Ce date acceptă / returnează API-ul
│   ├── user.py        ← Schema UserCreate, UserResponse, etc.
│   └── listing.py     ← Schema ListingCreate, ListingResponse, etc.
├── routers/           ← Grupuri de endpoint-uri
│   ├── auth.py        ← /auth/register, /auth/login, /auth/me
│   ├── listings.py    ← /listings/ (GET, POST, PUT, DELETE)
│   └── claims.py      ← /claims/ (POST, GET)
└── security/
    ├── auth.py        ← Generare și validare JWT tokens
    └── hashing.py     ← Hashing parole (bcrypt)
```

### Cum adaug un endpoint nou?

**Exemplu: adaug endpoint-ul `GET /listings/{id}/similar`**

**Pasul 1** — Deschide router-ul relevant (`routers/listings.py`) și adaugă:

```python
@router.get("/{listing_id}/similar", response_model=list[ListingResponse])
async def get_similar_listings(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # dacă necesită autentificare
):
    # logica ta aici
    similar = db.query(Listing).filter(
        Listing.category == listing_id,
        Listing.id != listing_id
    ).limit(5).all()
    return similar
```

**Pasul 2** — Dacă returnezi date noi, creează o schemă în `schemas/listing.py`:

```python
class ListingResponse(BaseModel):
    id: int
    title: str
    category: str
    expires_at: datetime

    class Config:
        from_attributes = True
```

**Pasul 3** — Verifică în browser la `http://localhost:8000/docs` că endpoint-ul apare și funcționează.

### Cum adaug un câmp nou în baza de date?

**Exemplu: adaug câmpul `image_url` la tabelul Listing**

**Pasul 1** — Modifică modelul în `models/listing.py`:

```python
class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=True)   # ← adăugat
    expires_at = Column(DateTime, nullable=False)
```

**Pasul 2** — Actualizează și schema Pydantic în `schemas/listing.py`:

```python
class ListingCreate(BaseModel):
    title: str
    image_url: str | None = None   # ← adăugat, opțional

class ListingResponse(BaseModel):
    id: int
    title: str
    image_url: str | None        # ← adăugat
```

**Pasul 3** — Aplică modificarea în baza de date:

```bash
# Dacă folosești Alembic (migrații):
alembic revision --autogenerate -m "add image_url to listing"
alembic upgrade head

# Dacă nu folosești Alembic (manual):
psql -U postgres -d foodsave -c "ALTER TABLE listings ADD COLUMN image_url VARCHAR;"
```

### Cum funcționează autentificarea?

Proiectul folosește **JWT (JSON Web Tokens)**:

1. Utilizatorul face `POST /auth/login` cu email + parolă
2. Serverul returnează un `access_token` (JWT)
3. Pentru endpoint-urile protejate, clientul trimite headerul:
   ```
   Authorization: Bearer <access_token>
   ```
4. FastAPI validează token-ul automat prin `Depends(get_current_user)`

### Cum configurez CORS (să accepte cereri din frontend)?

În `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adresa frontend-ului local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Documentația API

FastAPI generează automat documentație interactivă:
- **Swagger UI:** `http://localhost:8000/docs` ← poți testa endpoint-urile direct din browser
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🗄 Ghid Database

> **Când să folosești acest ghid:** Vrei să înțelegi structura bazei de date, să rulezi query-uri, să modifici schema.

### Conectare la baza de date

```bash
psql -U postgres -d foodsave

# Comenzi utile în psql:
\dt               # listează toate tabelele
\d listings       # descrie structura tabelului listings
\q                # ieși
```

### Structura tabelelor principale

```sql
-- Utilizatori (merchants, NGO-uri, voluntari)
users (id, email, password_hash, role, name, phone, created_at)

-- Listinguri (produse postate de merchant)
listings (id, merchant_id, title, description, quantity, unit,
          expires_at, location GEOMETRY(Point,4326), status, created_at)

-- Revendicări (când un NGO/voluntar ia un listing)
claims (id, listing_id, claimer_id, quantity_claimed, status, claimed_at)
```

### Căutare geospațială (PostGIS)

PostGIS permite căutare "în raza de X km":

```sql
-- Găsește listinguri în raza de 5 km față de un punct dat
SELECT * FROM listings
WHERE ST_DWithin(
    location::geography,
    ST_MakePoint(26.1025, 44.4268)::geography,  -- lng, lat (București)
    5000  -- metri
)
AND status = 'available';
```

---

## 🌿 Workflow Git pentru echipă

### Reguli de bază

| Branch | Scop |
|--------|------|
| `main` | Cod gata de producție — **nu comite direct aici** |
| `develop` | Branch de integrare — merge-uiți feature-urile aici |
| `feature/nume-feature` | Lucrul tău curent |

### Fluxul de lucru zilnic

```bash
# 1. Mereu actualizează develop înainte de a începe
git checkout develop
git pull origin develop

# 2. Creează un branch nou pentru ce lucrezi
git checkout -b feature/adaug-pagina-profil

# 3. Lucrează, comite des cu mesaje clare
git add .
git commit -m "feat: adaug pagina de profil pentru merchant"

# 4. Când termini, pune pe develop
git push origin feature/adaug-pagina-profil

# 5. Deschide Pull Request pe GitHub: feature → develop
# Roagă un coechipier să facă review
```

### Convenții pentru mesaje de commit

```
feat: adaug funcționalitate nouă
fix: repar un bug
style: modificări vizuale / CSS
refactor: restructurare cod fără funcționalitate nouă
docs: actualizare documentație
chore: actualizare dependențe, configurări
```

### Rezolvarea conflictelor

```bash
# Dacă ai conflicte la merge:
git fetch origin
git merge origin/develop

# Rezolvă conflictele în fișiere (caută <<<<<<< în cod)
# Apoi:
git add .
git commit -m "fix: rezolv conflicte cu develop"
```

---

## 🔐 Variabile de mediu

Creează fișierul `backend/.env` (nu îl comite niciodată în Git!):

```env
# Baza de date
DATABASE_URL=postgresql://postgres:parola_ta@localhost:5432/foodsave

# JWT
SECRET_KEY=un_string_lung_si_random_de_minim_32_caractere
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Mediu
ENVIRONMENT=development
```

> ⚠️ Fișierul `.env` este deja în `.gitignore`. **Nu îl comite niciodată.**

---

## 🛠 Troubleshooting

### Backend nu pornește

```bash
# Verifică că ești în virtual environment
which python  # trebuie să arate calea spre venv/

# Verifică că PostgreSQL rulează
pg_isready

# Verifică că baza de date există
psql -U postgres -l | grep foodsave
```

### Frontend nu se conectează la backend

1. Verifică că backend-ul rulează la `http://localhost:8000`
2. Verifică CORS în `backend/app/main.py` — `http://localhost:5173` trebuie să fie în `allow_origins`
3. Verifică că URL-ul din fetch/axios din frontend bate pe portul corect

### Erori de tip checker (Pyright)

Configurarea este în `pyrightconfig.json` la rădăcina proiectului. Dacă VS Code subliniază cod valid, verifică că interpretorul Python selectat în editor este cel din `venv/`.

### PostGIS nu e instalat

```bash
# Ubuntu/Debian:
sudo apt install postgresql-14-postgis-3

# Mac (cu Homebrew):
brew install postgis

# Activează extensia în baza de date:
psql -U postgres -d foodsave -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

---

## 📞 Contact echipă

| Rol | Responsabilitate principală |
|-----|-----------------------------|
| Dev 1 | Backend (FastAPI, modele, autentificare) |
| Dev 2 | Frontend (React, componente, UI) |
| Dev 3 | Database, DevOps, integrare |

---

*Ultima actualizare: Martie 2026*
