# 📬 Zarządzanie Twoją Pocztą

> Własne reguły i porządkowanie skrytek w aplikacji Outlook. Hotmail, Gmail, itd.

**Zarzadzanie-Outlook** to projekt pomagający utrzymać porządek w poczcie, z ochroną ważnych wiadomości i podglądem przed zmianami.

## ✨ Możliwości

- Własne listy nadawców, domen i słów kluczowych.
- Reguły wieku wiadomości i limitu przenoszenia.
- Rozpoznawanie reklam oraz newsletterów.
- Ochrona faktur, kodów weryfikacyjnych i ważnej korespondencji.
- Przenoszenie do Kosza po sprawdzeniu podglądu, bez trwałego usuwania.

## 📮 Obsługa skrzynek

Dołączony [skrypt Python](outlook_cleaner.py) obsługuje Outlook i Hotmail przez Microsoft Graph. Gmail oraz inne skrzynki wymagają osobnej integracji — nie są obecnie obsługiwane przez ten skrypt.

W ChatGPT można pracować z wybraną skrzynką, jeżeli odpowiednie połączenie i wymagane działania są dostępne na koncie. Zobacz [instrukcję](INSTRUKCJA_CHATGPT.md).

## 🔒 Ochrona wiadomości

W razie wątpliwości wiadomość pozostaje w skrzynce. Reguły ochronne mają pierwszeństwo. Program nie opróżnia Kosza. Szczegóły opisano w [zasadach bezpieczeństwa](BEZPIECZENSTWO.md).

## 🧩 Sposoby pracy

**Python:** uruchamiasz skrypt z własnymi ustawieniami. Domyślnie wyświetla podgląd; nie ma wbudowanego harmonogramu.

**ChatGPT:** korzystasz z dostępnej integracji pocztowej i [gotowego polecenia](PROMPT_CHATGPT.md). Cykliczne zadania wymagają osobnej konfiguracji i dostępu do poczty w środowisku wykonawczym. Samo pobranie repozytorium nie uruchamia automatyzacji.

**Cel:** mniej zbędnych wiadomości, własne zasady i wygodniejsze zarządzanie Twoją pocztą.
