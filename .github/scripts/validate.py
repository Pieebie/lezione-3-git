#!/usr/bin/env python3
"""
validate.py — Controlla che index.html sia corretto.

Verifiche eseguite:
  1. Il file index.html esiste ed è leggibile.
  2. L'HTML è ben formato (nessun errore di parsing).
  3. Esiste almeno un blocco <li class="student-card">.
  4. Ogni card ha un <div class="student-avatar"> e un <span class="student-name">.
  5. Nessun nome è duplicato.
  6. Nessun nome è rimasto con il valore di esempio ("Mario Professore", "Giulia Esempio").

Usato dalla GitHub Action .github/workflows/validate.yml
"""

import sys
from html.parser import HTMLParser
from pathlib import Path

# ─── Configurazione ────────────────────────────────────────────────────────────
HTML_FILE    = Path("index.html")
EXAMPLE_NAMES = {"Mario Professore", "Giulia Esempio"}   # nomi demo da non copiare

# ─── Parser ────────────────────────────────────────────────────────────────────
class ClassPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards: list[dict] = []

        # stato interno
        self._in_card       = False
        self._in_avatar     = False
        self._in_name       = False
        self._depth         = 0          # annidamento dentro <li class="student-card">
        self._current_card  = {}

    # ── tag aperto ──────────────────────────────────────
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        classes = attr.get("class", "").split()

        if tag == "li" and "student-card" in classes:
            self._in_card      = True
            self._depth        = 1
            self._current_card = {"avatar": "", "name": ""}
            return

        if self._in_card:
            self._depth += 1
            if tag == "div" and "student-avatar" in classes:
                self._in_avatar = True
            if tag == "span" and "student-name" in classes:
                self._in_name = True

    # ── tag chiuso ──────────────────────────────────────
    def handle_endtag(self, tag):
        if not self._in_card:
            return

        self._depth -= 1
        self._in_avatar = False
        self._in_name   = False

        if self._depth == 0:
            self.cards.append(self._current_card.copy())
            self._in_card = False

    # ── testo ───────────────────────────────────────────
    def handle_data(self, data):
        if not self._in_card:
            return
        text = data.strip()
        if not text:
            return
        if self._in_avatar:
            self._current_card["avatar"] = text
        if self._in_name:
            self._current_card["name"] = text


# ─── Validazione ───────────────────────────────────────────────────────────────
def validate() -> list[str]:
    errors: list[str] = []

    # 1 — Esistenza file
    if not HTML_FILE.exists():
        errors.append(f"❌  File non trovato: {HTML_FILE}")
        return errors

    source = HTML_FILE.read_text(encoding="utf-8")

    # 2 — Parsing (intercetta eccezioni di html.parser)
    parser = ClassPageParser()
    try:
        parser.feed(source)
    except Exception as exc:
        errors.append(f"❌  Errore di parsing HTML: {exc}")
        return errors

    cards = parser.cards

    # 3 — Almeno una card
    if not cards:
        errors.append(
            "❌  Nessun blocco <li class=\"student-card\"> trovato in index.html.\n"
            "    Hai aggiunto il tuo nome seguendo le istruzioni del README?"
        )
        return errors

    # 4 — Ogni card ha avatar e nome
    for i, card in enumerate(cards, start=1):
        if not card.get("avatar"):
            errors.append(f"❌  Card #{i}: manca <div class=\"student-avatar\"> o è vuoto.")
        if not card.get("name"):
            errors.append(f"❌  Card #{i}: manca <span class=\"student-name\"> o è vuoto.")

    # 5 — Nomi duplicati
    names = [c["name"] for c in cards if c.get("name")]
    seen: set[str] = set()
    for name in names:
        if name in seen:
            errors.append(f"❌  Nome duplicato trovato: \"{name}\".")
        seen.add(name)

    # 6 — Nomi di esempio rimasti invariati
    for card in cards:
        if card.get("name") in EXAMPLE_NAMES:
            errors.append(
                f"❌  Il nome \"{card['name']}\" è un nome di esempio e non deve essere presente.\n"
                "    Sostituiscilo con il tuo nome reale."
            )

    return errors


# ─── Punto di ingresso ─────────────────────────────────────────────────────────
def main():
    print(f"🔍  Validazione di {HTML_FILE} …\n")

    errors = validate()

    if errors:
        print("Trovati i seguenti problemi:\n")
        for err in errors:
            print(f"  {err}")
        print(f"\n❌  Validazione FALLITA ({len(errors)} {'errore' if len(errors) == 1 else 'errori'}).")
        print("   Correggi i problemi indicati, poi fai un nuovo commit.")
        sys.exit(1)
    else:
        # Ri-parsare per contare le card non-example
        source = HTML_FILE.read_text(encoding="utf-8")
        parser = ClassPageParser()
        parser.feed(source)
        real_cards = [c for c in parser.cards if c.get("name") not in EXAMPLE_NAMES]

        print(f"✅  HTML valido — {len(real_cards)} studente/i registrato/i:")
        for card in real_cards:
            print(f"   • {card['name']}")
        print("\n✅  Tutti i controlli superati. La PR è pronta per la review!")


if __name__ == "__main__":
    main()
