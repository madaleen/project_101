# ⚙️ Backend Masterclass: Arhitectură și Implementare Detaliată

Acest document este conceput ca un manual de inginerie aprofundat. Nu este doar o referință, ci o explorație a modului în care funcționează fiecare piesă din sistemul nostru, cu blocuri de cod complete și explicații teoretice.

---

## 🏛️ Filozofia Datelor: "The Chain of Truth"

În Proiectul 101, datele nu sunt simple rânduri într-un tabel. Ele sunt obiecte inteligente care trec printr-un proces riguros de transformare. Iată de ce structurăm fișierele astfel:

1.  **Modelele SQLAlchemy (`models/`)**: Reprezintă structura fizică a bazei de date. Folosim `Mapped` pentru a avea suport complet de la IDE (Autocomplete) și `Geography` pentru a permite calcule matematice pe suprafața pământului (curbura terestră).
2.  **Schemele Pydantic (`schemas/`)**: Reprezintă "contractul" nostru cu lumea exterioară. Ele decid ce date poate vedea utilizatorul și ce date avem voie să primim. Acesta este stratul de protecție împotriva atacurilor de tip *Mass Assignment*.

---

## 🛠️ Tutorial Aprofundat: Adăugarea unui Câmp Nou (Ex: Telefon)

Vom urmări drumul complet al unei noi informații, de la baza de date până la API.

### Pasul 1: Modificarea Modelului Fizic
Deschidem `backend/app/models/user.py`. Adăugăm coloana `phone`.
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    # Noul câmp adăugat:
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
```
**Explicație**: `Mapped[str | None]` îi spune lui Python că acest câmp poate fi un string sau gol. `String(20)` limitează lungimea în baza de date pentru a economisi spațiu.

### Pasul 2: Modificarea Schemei de Validare
Deschidem `backend/app/schemas/user.py`. Trebuie să actualizăm cum primim și trimitem datele.
```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    phone: str | None = None # Adăugăm aici pentru a fi disponibil în restul claselor

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True # Permite transformarea automată din model SQLAlchemy
```
**Explicație**: Pydantic folosește aceste clase pentru a genera automat documentația Swagger și pentru a valida dacă datele primite sub formă de JSON sunt corecte.

---

## 🔐 Securitate și RBAC: Cum protejăm rutele?

Sistemul nostru folosește **Dependency Injection**. Aceasta înseamnă că protecția nu este scrisă "în interiorul" rutei, ci este o cerință care trebuie îndeplinită *înainte* ca ruta să fie apelată.

### Exemplu: Protejarea unei rute de Store
```python
from fastapi import APIRouter, Depends
from app.core.deps import get_current_user, require_role

router = APIRouter()

@router.post("/create-offer")
async def post_food(
    obj_in: DonationCreate,
    current_user: User = Depends(require_role(["Store"]))
):
    # Această secțiune de cod se va executa DOAR dacă:
    # 1. Utilizatorul are un Token JWT valid.
    # 2. Utilizatorul are rolul de "Store" în baza de date.
    new_donation = await create_in_db(obj_in, owner_id=current_user.id)
    return new_donation
```
**Logica Internă**: 
1. `get_current_user` extrage ID-ul din JWT.
2. `require_role` caută user-ul în DB și verifică dacă `user.role` se află în lista `["Store"]`.
3. Dacă oricare pas eșuează, FastAPI trimite automat `401 Unauthorized` sau `403 Forbidden`.

---

## 🚜 Migrări (Alembic): De ce sunt critice?

Alembic este "Time Machine" pentru baza ta de date. Orice schimbare în `models/` trebuie înregistrată:
1.  **Generare**: `alembic revision --autogenerate -m "descriere"` (Citește modelele tale și compară-le cu DB-ul).
2.  **Aplicare**: `alembic upgrade head` (Execută codul SQL generat).
**Important**: Nu șterge niciodată manual coloane din DB în timpul dezvoltării; lasă Alembic să gestioneze istoricul pentru a evita erori de sincronizare între membrii echipei.
