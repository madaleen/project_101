# 🎨 Frontend Masterclass: Arhitectură și Implementare Detaliată

Acest document este conceput ca un manual de inginerie aprofundat pentru interfața Proiectului 101. Vom explora de la structura fișierelor la modul în care datele circulă prin componente folosind React și Vite.

---

## 🏛️ Filozofia Interfaței: "The Atomic Brain"

În acest proiect, nu scriem doar cod vizual; construim un sistem de date reactiv. Iată de ce structurăm fișierele astfel:

1.  **Componentele (`src/components/`)**: Sunt piese detașabile și reutilizabile (Butoane, Carduri, Bare de filtrare). Ele nu au "memorie" proprie; primesc date de la părinte via `props`. Acest lucru le face ușor de testat și de stilizat independent.
2.  **Serviciile API (`src/services/`)**: Acesta este singurul loc unde React "vorbește" cu serverul. Abstracționăm toate apelurile de `fetch` aici pentru a păstra componentele curate.

---

## 🛠️ Tutorial Aprofundat: Modificarea UI-ului și Integrarea API

Vom urmări drumul complet al unei noi cerințe: Adăugarea unui buton de "Contact" care trimite un mesaj la server.

### Pasul 1: Crearea Serviciului de Comunicare
Deschidem `frontend/src/services/api.js`. Adăugăm funcția de trimitere a mesajului.
```javascript
const API_URL = "http://localhost:8000";

export async function postContactMessage(messageData) {
  // Preluăm token-ul pentru a fi siguri că userul e logat
  const token = localStorage.getItem("token");
  
  const response = await fetch(`${API_URL}/contact`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}` # Injectarea automată a securității
    },
    body: JSON.stringify(messageData)
  });
  
  // Dacă serverul dă eroare, o tratăm aici înainte să ajungă în UI
  if (!response.ok) throw new Error("A apărut o problemă la trimiterea mesajului.");
  return response.json();
}
```
**Explicație**: Păstrăm logica de `fetch` centralizată. Dacă adresa serverului se schimbă, o modificăm într-un singur loc (`API_URL`), nu în 50 de componente!

### Pasul 2: Implementarea în Pagina Principală
Deschidem `frontend/src/App.jsx`. Adăugăm butonul și logica de trimitere.
```jsx
function App() {
  // Starea pentru mesajul utilizatorului (Logic)
  const [message, setMessage] = useState("");

  // Funcția de handler care "leagă" UI-ul de Service (Action)
  const handleSubmit = async () => {
    try {
      await postContactMessage({ text: message });
      alert("Mesaj trimis cu succes!");
    } catch (err) {
      console.error(err.message);
    }
  };

  return (
    <div className="p-8">
      {/* Secțiunea Vizuală: Hero Section */}
      <div className="glass-effect p-12 rounded-3xl">
        <h1>Stop Food Waste!</h1>
        <textarea 
          value={message} 
          onChange={(e) => setMessage(e.target.value)} 
          className="w-full p-4 border rounded-xl my-4" 
        />
        <button 
          onClick={handleSubmit}
          className="px-8 py-4 bg-emerald-500 text-white rounded-2xl hover:scale-105 transition-all"
        >
          Trimite Mesaj
        </button>
      </div>
    </div>
  );
}
```
**Explicație**: `useState` reține ceea ce tastează utilizatorul. `onClick` declanșează funcția `handleSubmit`, care la rândul ei apelează serviciul nostru din Pasul 1. Acesta este fluxul standard: **Trigger (UI) -> Action (Service) -> Response (State/Alert)**.

---

## 🎨 Design System: Variabile CSS vs CSS Utility

Folosim o metodă hibridă pentru a avea viteză maximă:
- **Variabile CSS**: Păstrăm culorile de brand (ex: Verdele Emerald) într-un singur loc în `index.css`.
- **Utility Classes**: Folosim clase precum `p-8` (padding) sau `rounded-3xl` (colțuri rotunjite) direct în codul JSX.

### Exemplu de Stilare Avansată în `index.css`:
```css
:root {
  --primary-color: #10b981;
  --secondary-color: #334155;
  --glass-bg: rgba(255, 255, 255, 0.7);
}

.glass-effect {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
}
```
**Dacă vrei să schimbi aspectul "Glassmorphism"**, modifici doar fișierul `.css`. Componentele tale nu trebuie modificate, ele vor adopta automat noile stiluri.
