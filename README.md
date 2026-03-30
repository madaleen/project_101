# 🥗 Food Saving & Donation Platform — project_101

> O platformă care reduce risipa alimentară prin conectarea Restaurantelor și Comercianților cu ONG-uri și Voluntari individuali.

---

## 🏗️ Masterclass Full-Stack (Overview)

Acesta este ghidul central pentru dezvoltarea și extinderea platformei Project 101. Nu doar că pui cap-la-cap bucăți de cod, ci înțelegi modul în care Datele și Securitatea creează o experiență de utilizator premium.

### Istoria unei Cereri: De la Click la Baza de Date (Full-Stack Story)

Pentru a înțelege puterea acestei arhitecturi, urmăm drumul unei cereri de tip **"Revendică o Masă" (Claim a Meal)**. Aceasta este "odiseea" asincronă a unei singure acțiuni:

1. **Scânteia (Frontend UI)**: Utilizatorul vede un card de donație și apasă pe butonul "Claim Meal". În acel moment, React capturează ID-ul donației (`App.jsx`).
2. **Diplomația (Frontend Service)**: Serviciul preia ID-ul, injectează automat Token-ul JWT de autentificare și trimite cererea HTTP (`services/api.js`).
3. **Poliția (Backend Auth)**: Cererea ajunge la server. FastAPI validează Token-ul prin `get_current_user` (`core/deps.py`).
4. **Execuția (Backend Logic)**: Router-ul primește ID-ul și deschide o tranzacție cu baza de date. Verifică disponibilitatea și creează revendicarea (`routers/claims.py`).
5. **Finalul (Database & Response)**: Baza de date confirmă scrierea. Serverul trimite succes, iar UI-ul se actualizează instantaneu (Optimistic UI).

---

## 📋 Cuprins

1. [Contextul proiectului](#-contextul-proiectului)
2. [Arhitectura generală](#-arhitectura-generală)
3. [Roluri în aplicație](#-roluri-în-aplicație)
4. [Setup inițial (prima rulare)](#-setup-inițial-prima-rulare)
5. [Deep-Dive: Manuale Tehnice](#-deep-dive-manuale-tehnice-complete)
6. [Workflow Git pentru echipă](#-workflow-git-pentru-echipă)
7. [Variabile de mediu](#-variabile-de-mediu)
8. [Troubleshooting](#-troubleshooting)

---

## 🌍 Contextul proiectului

Sunt em 3 persoane care lucrăm împreună la o platformă de salvare și donație alimente. Scopul este să conectăm:

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
├── backend/           # API-ul FastAPI
├── database/          # Schema SQL inițială și migrații
├── README.md          # Acest fișier
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

- **Node.js** ≥ 18, **Python** 3.12, **PostgreSQL** ≥ 14 cu **PostGIS**, **Git**

### 1. Clonează repo-ul

```bash
git clone https://github.com/madaleen/project_101.git
cd project_101
```

### 2. Pornește baza de date

```bash
psql -U postgres -c "CREATE DATABASE foodsave;"
psql -U postgres -d foodsave -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql -U postgres -d foodsave -f database/schema.sql
```

### 3. Pornește Backend-ul

```bash
cd backend
python -m venv venv
# venv\Scripts\activate (Windows) sau source venv/bin/activate (Mac)
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### 4. Pornește Frontend-ul

```bash
cd frontend
npm install
npm run dev
```

---

## 🛠️ Deep-Dive: Manualele Tehnice Complete

Dacă vrei să intri în fiecare fișier în parte, am pregătit ghiduri pline de cod și explicații:

- ⚙️ **[Backend Masterclass](file:///c:/Users/madaleen/proiects/project_101/backend/README.md)**: Adăugarea de câmpuri, logica PostGIS, Securitate JWT și Migrări.
- 🎨 **[Frontend Masterclass](file:///c:/Users/madaleen/proiects/project_101/frontend/README.md)**: React State, Service Layer Abstraction, Hooks și Design System.
- 🛠️ **[Flow-ul de Dezvoltare Git](file:///c:/Users/madaleen/proiects/project_101/README_GIT.md)** (Tutorial Branching, Commit, Push).

---

## 🌿 Workflow Git pentru echipă

| Branch | Scop |
|--------|------|
| `main` | Cod gata de producție — **nu comite direct aici** |
| `develop` | Branch de integrare — merge-uiți feature-urile aici |
| `feature/nume-feature` | Lucrul tău curent |

---

## 🛠 Troubleshooting

1. **CORS Errors**: Verifică `allow_origins` în `backend/app/main.py`. Trebuie să accepte `http://localhost:5173`.
2. **PostGIS missing**: Rulează `CREATE EXTENSION IF NOT EXISTS postgis;` în psql pentru baza `foodsave`.
3. **Frontend connection**: Verifică URL-ul API din `frontend/src/services/api.js`.

---

## 🌍 Viziune de Inginerie
Project 101 nu este doar o aplicație; este o soluție pentru o problemă socială majoră. Arhitectura noastră este gândită să susțină mii de utilizatori concurenți și tone de date geospațiale. 
**Spor la implementat!**
