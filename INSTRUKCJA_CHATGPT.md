# 🤖 Jak uruchomić kontrolę Outlook w ChatGPT

Ten poradnik pozwala **spróbować skonfigurować podobny workflow** we własnym ChatGPT. Nie jest instalatorem ani oficjalną integracją.

## 1. Połącz pocztę
1. Otwórz ChatGPT → **Ustawienia → Plugins / Aplikacje** (nazwy mogą się różnić).
2. Znajdź integrację **Microsoft Outlook Email** i połącz własne konto.
3. Sprawdź, jakie uprawnienia ma połączenie. Do przenoszenia wiadomości konieczne są uprawnienia do ich modyfikacji. Sam odczyt nie wystarczy.

**Uwaga:** dostępność aplikacji, harmonogramów i uprawnień zależy od konta, planu i regionu. Samo dodanie repozytorium GitHub niczego nie uruchamia.

## 2. Skopiuj polecenie
W nowym czacie z podłączoną pocztą wklej treść z [PROMPT_CHATGPT.md](PROMPT_CHATGPT.md).

## 3. Najpierw test
Poproś: **„Przeanalizuj ostatnie 50 wiadomości i pokaż propozycje przeniesienia do Kosza, ale jeszcze nic nie przenoś.”**

Sprawdź wyniki. Jeśli wszystko wygląda poprawnie, możesz zezwolić na przenoszenie **jednoznacznych** reklam do folderu **Elementy usunięte**.

## 4. Kontrola cykliczna (opcjonalna)
Poproś ChatGPT: **„Jeżeli masz możliwość wykonywania zaplanowanych zadań z dostępem do Outlook, skonfiguruj kontrolę co 2 godziny. Jeżeli nie, powiedz mi wprost, że taka automatyzacja nie jest dostępna.”**

Zadania zaplanowane **nie zawsze** mają dostęp do tych samych połączeń i działań co zwykły czat. Sprawdź faktyczne wykonanie pierwszego uruchomienia i historię działań. Nie zakładaj, że działa, dopóki nie zobaczysz raportu.

## 5. Zasady
- Tylko własna skrzynka, na której masz uprawnienia.
- Nie udostępniaj haseł, tokenów, kodów 2FA ani treści prywatnych e-maili na GitHubie.
- **Nigdy nie opróżniaj automatycznie Kosza.**
- Wątpliwe wiadomości pozostaw w skrzynce.
- Zawsze wymagaj raportu: ile wiadomości przejrzano i ile faktycznie przeniesiono.

## Alternatywa bez ChatGPT
Samodzielny skrypt [outlook_cleaner.py](outlook_cleaner.py) korzysta z Microsoft Graph i ma domyślny tryb podglądu. Wymaga osobnej konfiguracji OAuth i uruchamiania przez użytkownika.
