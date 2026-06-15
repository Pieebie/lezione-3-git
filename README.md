# 👋 Classe Git 2026 — ITS Turismo e Nuove Tecnologie Marche

Questo repository è l’esercitazione pratica del corso **Git & GitHub**.  
L’obiettivo è semplice: **aggiungere il proprio nome** alla pagina della classe aprendo una Pull Request.

-----

## 🎯 Cosa imparerai

Completando questo esercizio metterai in pratica:

- Creare un **branch** con un nome descrittivo
- Fare un **commit** con un messaggio chiaro
- Aprire una **Pull Request** e richiedere una review
- Vedere la **GitHub Action** eseguire i controlli automatici

-----

## ✏️ Come aggiungere il tuo nome

### 1 — Clona il repository

```bash
git clone git@github.com:TUO-UTENTE/lezione-3-git.git
cd lezione-3-git
```

### 2 — Crea un branch

```bash
git switch -c feat/aggiungi-nome-tuonome
# Esempio: feat/aggiungi-mario-rossi
```

### 3 — Modifica `index.html`

Apri il file e cerca questo commento:

```html
<!-- ✏️ AGGIUNGI QUI IL TUO NOME -->
```

Copia uno dei blocchi `<li>` esistenti, incollalo **sopra** il commento e modifica i dati:

```html
<li class="student-card" data-initials="MR">
  <div class="student-avatar">MR</div>
  <div class="student-info">
    <span class="student-name">Mario Rossi</span>
    <span class="student-course">Corso Git 2026</span>
  </div>
</li>
```

### 4 — Fai il commit

```bash
git add index.html
git commit -m "feat: aggiungi Mario Rossi"
git push -u origin feat/aggiungi-mario-rossi
```

### 5 — Apri la Pull Request

Vai su GitHub, clicca **“Compare & pull request”** e:

- Scrivi un titolo chiaro (es. `Aggiungi Mario Rossi`)
- Aggiungi una breve descrizione
- Richiedi la review al docente

### 6 — Aspetta i controlli automatici ✅

La **GitHub Action** verificherà automaticamente che il file HTML sia valido.  
Se vedi una ✅ verde, sei a posto. Se vedi una ❌ rossa, leggi i log per capire cosa correggere.

-----

## 📐 Regole per la PR

|✅ Obbligatorio                                 |❌ Da evitare                                  |
|-----------------------------------------------|----------------------------------------------|
|Un solo nome per PR                            |Modificare i blocchi degli altri              |
|Messaggio commit: `feat: aggiungi Nome Cognome`|Messaggi generici come `fix` o `aggiornamento`|
|Branch con nome descrittivo                    |Lavorare direttamente su `main`               |
|Dati reali (nome e cognome)                    |Nomi inventati o nickname                     |

-----

## 🔍 Come funziona la GitHub Action

Ad ogni `push` e ad ogni PR, viene eseguito automaticamente `.github/workflows/validate.yml`.  
Lo script Python controlla che:

1. Il file `index.html` contenga almeno un blocco `student-card`
1. Ogni blocco abbia `student-name` e `student-avatar`
1. Non ci siano nomi duplicati

-----

## 🗂️ Struttura del repository

```
lezione-3-git/
├── index.html                  # La pagina della classe
├── README.md                   # Questo file
└── .github/
    └── workflows/
        └── validate.yml        # GitHub Action di validazione
```

-----

*ITS Turismo e Nuove Tecnologie Marche — Corso Git & GitHub 2024*
