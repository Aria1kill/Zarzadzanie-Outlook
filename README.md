<div align="center">

# 📬 Kontrola Outlook

### Bezpieczny porządek w poczcie Outlook i Hotmail

**Własne reguły • Ochrona ważnych wiadomości • Podgląd przed zmianami**

Prosty projekt open source do rozpoznawania zbędnych wiadomości i porządkowania skrzynki przy użyciu Microsoft Graph.

[🚀 Szybki start](#-szybki-start) · [⚙️ Własne reguły](USTAWIENIA.md) · [🤖 ChatGPT](INSTRUKCJA_CHATGPT.md) · [🔒 Bezpieczeństwo](BEZPIECZENSTWO.md)

</div>

---

## ✨ Co potrafi program?

| Funkcja | Opis |
|---|---|
| 🎯 Wybrani nadawcy | Wskaż konkretne adresy i domeny, których wiadomości chcesz porządkować. |
| 🛡️ Lista chronionych | Zachowaj wiadomości od ważnych osób i firm. |
| 🔎 Własne słowa | Dodaj frazy charakterystyczne dla reklam i newsletterów. |
| 🕒 Wiek wiadomości | Ustal, po ilu dniach wiadomość może zostać zakwalifikowana. |
| 👀 Bezpieczny podgląd | Domyślnie program niczego nie przenosi. |
| 🗑️ Odwracalne zmiany | Po potwierdzeniu przenosi do Elementów usuniętych; nie usuwa trwale. |

## 🚀 Szybki start

**Wymagania:** Python 3.10+, konto Outlook/Hotmail, aplikacja Microsoft Entra do autoryzacji Microsoft Graph (dla pracy z prawdziwą skrzynką).

1. Pobierz pliki repozytorium i zainstaluj zależności: `pip install -r requirements.txt`.
2. Wypróbuj bez logowania: `python outlook_cleaner.py --demo`.
3. Zmień reguły w [config.example.json](config.example.json) — szczegóły w [instrukcji ustawień](USTAWIENIA.md).
4. Skonfiguruj `OUTLOOK_CLIENT_ID` zgodnie z [instrukcją](USTAWIENIA.md).
5. Uruchom `python outlook_cleaner.py`, aby zobaczyć **podgląd bez zmian**.
6. Dopiero po sprawdzeniu wyników użyj `python outlook_cleaner.py --apply --yes`.

## 🤖 Chcesz używać ChatGPT?

Zobacz [instrukcję dla ChatGPT](INSTRUKCJA_CHATGPT.md) i [gotowe polecenie](PROMPT_CHATGPT.md). To **oddzielny sposób pracy** od programu Python; dostępność integracji i harmonogramów zależy od Twojego konta i uprawnień.

## 🧪 Testowanie

```bash
python -m unittest discover -s tests -v
python outlook_cleaner.py --demo
```

[Testy GitHub Actions](../../actions) uruchamiają się przy zmianach w repozytorium. Testy symulacyjne nie łączą się z prawdziwą pocztą. Pomyślny wynik nie gwarantuje poprawnego działania na każdym koncie Microsoft.

## 📚 Dokumentacja

- [⚙️ Ustawienia i własne reguły](USTAWIENIA.md)
- [🤖 Instrukcja ChatGPT](INSTRUKCJA_CHATGPT.md)
- [📋 Gotowy prompt ChatGPT](PROMPT_CHATGPT.md)
- [🔐 Zasady bezpieczeństwa](BEZPIECZENSTWO.md)
- [📁 Struktura projektu](STRUKTURA_PROJEKTU.md)
- [📖 Opis projektu](kontrola-outlook.md)

---

> **Uwaga:** Reguły bazują na temacie i krótkim podglądzie wiadomości. Mogą popełniać błędy. Przed włączeniem przenoszenia sprawdź wyniki. Nie publikuj haseł, tokenów ani prywatnych wiadomości w repozytorium.

<sub>Projekt społecznościowy i demonstracyjny. Nie jest oficjalnym produktem Microsoft ani OpenAI.</sub>
