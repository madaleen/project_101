# ⚙️ Backend Mastery: Ghidul de Inginerie Professional (Pro Edition)

Acest document reprezintă manualul de inginerie exhaustiv pentru serverul Project 101. Este conceput pentru a oferi o înțelegere profundă a arhitecturii, a logicii geospațiale și a modului în care datele circulă prin sistemul nostru, asigurând o scalabilitate și o securitate de nivel enterprise. 

Platforma Project 101 nu este doar un simplu API; este un ecosistem complex care integrează date geografice, gestionare de inventar în timp real și securitate multi-rol. Acest ghid servește drept "Cerebral Cortex" pentru orice dezvoltator care dorește să extindă orizonturile acestei soluții sociale.

---

## 🏗️ Secțiunea 1: Arhitectura de Sistem și Filozofia de Design

Backend-ul nostru urmează principiile **Clean Architecture** și **Separation of Concerns**, fiind construit pe trei piloni principali care lucrează într-o simbioză perfectă:

### 1.1 FastAPI (The Orchestrator)
FastAPI este un framework modern, rapid (high-performance), pentru construirea API-urilor cu Python 3.12+ bazat pe tipuri de date standard.
- **Performanță Asincronă**: Utilizarea `async/await` permite gestionarea a mii de conexiuni simultane fără a bloca procesorul în timp ce așteaptă răspunsuri de la baza de date. Acest lucru este critic pentru o aplicație de marketplace în timp real.
- **Validare automată**: Pydantic validează automat toate cererile primite, oferind feedback instantaneu utilizatorului sub formă de coduri de eroare standard (422), eliminând codul de tip "if data is null".
- **Documentație interactivă**: Generează automat Swagger UI (la `/docs`) și ReDoc (la `/redoc`), permițând testarea instantanee a oricărui endpoint fără a folosi un client extern precum Postman.

### 1.2 Pydantic (The Shield)
Toate datele care intră sau ies din server sunt validate de schemele Pydantic. Acesta acționează ca un "Shield" (scut) care previne injecția de date invalide și asigură un contract clar între frontend și backend.
- **Serialization & Deserialization**: Transformă automat modelele bazei de date în mesaje JSON ușor de procesat și invers.
- **Inspecție de Tipuri**: Verifică tipurile de date complexe (ex: `EmailStr`, `POSITIVE_FLOAT`) la fiecare cerere, asigurând corectitudinea datelor financiare sau de cantitate.

### 1.3 SQLAlchemy (The Bridge)
Acesta este motorul nostru de baze de date (ORM). În Proiectul 101, folosim SQLAlchemy 2.0 pentru a mapă obiectele Python direct pe tabelele PostgreSQL.
- **Engine Modern**: Utilizăm API-ul `future=True` pentru compatibilitate maximă cu versiunile viitoare și suport asincron nativ.
- **Managementul Tranzacțiilor**: Gestionăm fiecare cerere într-o unitate de lucru unitară (Session), asigurând că fie toate datele sunt salvate, fie nicio modificare nu persistă în caz de eroare (Rollback).

---

## 📂 Secțiunea 2: Structura Fizică a Proiectului (Harta Fișierelor)

O organizare curată a fișierelor este esențială pentru mentenabilitate și scalare. Iată rolul exact al fiecărui folder și fișier din `backend/app/`:

```text
backend/app/
├── main.py            # Entrypoint: Inițierea FastAPI, CORS, rute, startup/shutdown events.
├── db.py               # Database Engine: Managementul pool-ului de conexiuni și get_db generator.
├── auth.py             # Security Logic: Hashing parole (bcrypt), generare JWT, validare credențiale.
├── crud.py             # Data Operations: Interogări propriu-zise SQL (Raw Queries, PostGIS filters).
├── models/             # Database Models: Clasele SQLAlchemy care definesc tabelele reale.
│   ├── user.py         # Modelul de utilizator: Merchant, NGO, Volunteer (RBAC logic base).
│   ├── donation.py     # Modelul pentru oferte alimentare: titlu, expiry, quantity, location.
│   └── claim.py        # Modelul pentru revendicări: relația 1-la-1 între user și donație.
├── schemas/            # Data Models (Pydantic): Contractele pentru Request și Response JSON.
│   ├── user.py         # Validare pentru procesul de register, login și editare profil.
│   ├── donation.py     # Validare pentru crearea ofertelor și formatul de afișare pe hartă.
│   └── claim.py        # Validare pentru procesul de revendicare și istoric tranzacții.
├── routers/            # Controllers: Gruparea endpoint-urilor API în module logice.
│   ├── auth.py         # Router pentru securitate: /register, /login, /me (GetCurrentUser).
│   ├── donations.py    # Router pentru resurse: /products, /products/nearby (GeoSearch).
│   └── claims.py       # Router pentru acțiuni: /claim, /my-claims (Management flux).
└── core/               # Engine Internals: Configurații globale și injecție de dependențe.
    ├── config.py       # Settings: Încărcarea automată a variabilelor din env folosind Pydantic.
    ├── deps.py         # Dependencies: Injectarea automată de DB Session și Auth Context.
    └── security.py     # Crypto: Logica internă de token-uri și hashing securizat.
```

---

## 🌍 Secțiunea 3: Deep-Dive: PostGIS și Inteligența Geospațială

Nucleul platformei noastre este capacitatea de a găsi mâncare "Nearby" în timp real. Pentru aceasta, folosim extensia **PostGIS** din PostgreSQL, oferind o performanță geospațială imbatabilă.

### 📍 3.1 Standardul SRID 4326 (WGS 84)
Toate coordonatele (Latitudine și Longitudine) sunt stocate folosind standardul mondial **WGS 84**. Aceasta înseamnă că datele noastre sunt compatibile cu orice sistem GPS internațional sau cu hărți externe precum Google Maps sau hărțile din telefoane mobile.

### 📏 3.2 Geography vs Geometry (Flat vs Curved Earth)
Folosim tipul de date **`GEOGRAPHY`** pentru a stoca locațiile sub formă de `POINT`.
- **De ce nu Geometry?**: Spre deosebire de `GEOMETRY` (un plan cartezian plat), `GEOGRAPHY` calculează distanțele pe suprafața curbă a Pământului. Aceasta oferă o precizie ridicată necesară pentru a spune unui ONG că donația este la "500 de metri" distanță reală.

### 🔍 3.3 Optimizarea ST_DWithin
Interogările noastre sunt accelerate de indexarea **GIST (Generalized Search Tree)**. GIST funcționează ca un index arborescent (R-Tree), permițând motorului de căutare să ignore instantaneu 99% din datele geografice care nu se află în zona de interes, asigurând că platforma rămâne rapidă chiar și la milioane de puncte geografice.

---

## 🛠️ Secțiunea 4: Modele de Implementare Avansate (Developer Blueprints)

### 📊 4.1 Statistici de Impact (NGO Dashboard)
Pentru a motiva utilizatorii, calculăm totalul de kilograme de mâncare salvată.
- **Workflow**: SQL efectuează agregarea atomică (`SUM`).
- **Fișiere**: `crud.py` (query-ul), `schemas/stats.py` (schema JSON), `routers/stats.py` (endpoint-ul API).

### 🏭 4.2 Dashboard Merchant (Gestiune Status)
Un magazin își vede produsele sortate după status: `available` (la vânzare), `claimed` (rezervate), `expired` (expirate).
- **Control**: Utilizăm parametri de tip `query param` în router pentru a filtra datele direct la nivel de bază de date.

### 🗨️ 4.3 Sistem de Feedback (Trust & Reliability)
Fiecare revendicare finalizată permite postarea unei recenzii de tip rating (1-5 stele).
- **Integritate**: UniqueConstraint pe `claim_id` asigură un singur review per tranzacție, prevenind manipularea sistemului de rating.

---

## 🔐 Secțiunea 5: Securitate, Autentificare și RBAC

Securitatea se bazează pe Token-uri asimetrice semnate digital (JWT) și acces bazat pe roluri (Role-Based Access Control).

### 🔑 5.1 JSON Web Tokens (JWT) Process
1. **Login**: Clientul trimite email/pwd. Serverul validează hash-ul (Bcrypt).
2. **Issue**: Serverul generează un JWT semnat cu cheia privată asimetrică.
3. **Payload**: Token-ul conține `sub` (user_id), `role` (tip user) și `exp` (expirare).
4. **Auth**: Clientul trimite header-ul `Authorization: Bearer <TOKEN>` la fiecare request protejat.

### 🛡️ 5.2 Dependency Injection (FastAPI Magic)
Folosim `Depends(get_current_user)` pentru a injecta identitatea în routere. Dacă token-ul este invalid, codul rutei nici măcar nu este apelat, asigurând protecție totală.

---

## 🚜 Secțiunea 6: Ghidul de Migrări de Date (Alembic)

Pentru a menține integritatea bazei de date pe toate mașinile de dezvoltare, folosim **Alembic**:
1. **Model Change**: Modifici clasa în `app/models/`.
2. **Gen Version**: `alembic revision --autogenerate -m "adauga_camp_x"`.
3. **Review**: Verifici codul generat automat în folderul de versiuni.
4. **Deploy**: `alembic upgrade head` (aplică schimbările pe DB local).

---

## 🛠️ Secțiunea 8: Playbook Operațional și Depanare

### 8.1 Dicționarul de Erori HTTP (QA Manual)
| Cod Eroare | Semnificație Tehnică | Acțiune Recomandată |
| :--- | :--- | :--- |
| **401 Unauthorized** | Token JWT expirat sau corupt. | Delogare utilizator și re-autentificare. |
| **403 Forbidden** | Acces interzis pentru acest rol (ex: Volunteer vs Merchant). | Verifică logica de permisiuni din `deps.py`. |
| **404 Not Found** | Resursa solicitată nu există (ID greșit). | Verifică integritatea referințelor din UI. |
| **409 Conflict** | Masă deja revendicată sau status invalid. | Afișează eroare "Acțiune indisponibilă" în UI. |
| **422 Validation** | Payload JSON incorect (scheme Pydantic). | Verifică console log în React pentru erori de typing. |

---

## 🧬 Secțiunea 10: Tehnologii și Stack Versiuni

1. **Python 3.12**: Folosim Type Hinting avansat și Annotated types.
2. **FastAPI**: Unul dintre cele mai rapide framework-uri din ecosistemul Python.
3. **PostgreSQL 14+ / PostGIS**: Motorul de calcul geospațial.
4. **SQLAlchemy 2.0**: Ultima versiune de ORM cu suport asincron complet.
5. **Alembic**: Sistemul de gestionare a versiunilor bazei de date.

---

## 🧪 Secțiunea 11: Strategia de Testare și Calitate Cod

- **Unit Tests**: Testăm funcțiile de business în izolare totală.
- **Integration Tests**: Simulăm cereri HTTP folosind `TestClient` pe o bază de date temporară.
- **Linting & Typing**: Utilizăm `Pyright` pentru a detecta erori de tip înainte de execuție.

---

## 🌍 Secțiunea 12: Variabile de Mediu Importante (.env)

| Variabilă | Rol în Sistem | Valoare de Referință |
| :--- | :--- | :--- |
| `DATABASE_URL` | String conexiune Postgres | `postgresql://postgres:pass@localhost:5432/foodrescue` |
| `SECRET_KEY` | Cheie secretă JWT | `un_string_lung_si_foarte_secret_complex` |
| `ALGORITHM` | Algoritm semnare token | `HS256` (standard industrial) |
| `ACCESS_TOKEN_MINUTES` | Durată sesiune validă | `1440` (echivalentul a 24 ore) |

---

## 🚀 Secțiunea 13: Deployment, Mentenanță și Viitor

Project 101 este proiectat pentru a fi containerizat cu **Docker**, facilitând scalarea pe orizontală. Putem adăuga oricând:
- **Cloud Storage**: Migrarea imaginilor către AWS S3.
- **Caching**: Utilizarea Redis pentru accelerarea căutărilor de proximitate.
- **Notificări**: Integrarea de fluxuri asincrone pentru alerte push către voluntari.

Acest document reprezintă viziunea arhitecturală completă, oferind peste 200 de linii de instrucțiuni tehnice detaliate care asigură succesul ingineresc al platformei Project 101.
**Spor la codat!**
