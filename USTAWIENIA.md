# 🛠️ Zarządzanie Twoją Pocztą — własne reguły

Poniższe ustawienia dotyczą skryptu Outlook/Hotmail przez Microsoft Graph. Gmail i inne skrzynki wymagają osobnej integracji.

W pliku [config.example.json](config.example.json) każdy może samodzielnie ustawić reguły bez zmieniania programu.

| Nazwa | Co robi |
|---|---|
| `protected_senders` | Adresy nadawców, których wiadomości zawsze zostają |
| `protected_domains` | Domeny chronione (także ich poddomeny) |
| `protected_keywords` | Słowa w temacie lub podglądzie chroniące wiadomość |
| `blocked_senders` | Konkretni nadawcy kwalifikowani do Kosza |
| `blocked_domains` | Domeny kwalifikowane do Kosza |
| `blocked_keywords` | Własne słowa wskazujące zbędne wiadomości |
| `min_age_days` | Minimalny wiek wiadomości, np. 7 dni |
| `max_moves` | Maksymalna liczba kandydatów na uruchomienie |
| `use_default_marketing_rules` | Włączanie rozpoznawania typowych promocji |

**Najważniejsze:** reguły ochronne i wbudowane zabezpieczenia mają pierwszeństwo. Zablokowanie nadawcy nie oznacza bezwarunkowego usunięcia wszystkich jego wiadomości. Program analizuje tylko temat i krótki podgląd treści, dlatego nie gwarantuje pełnej trafności.

## Pierwsze uruchomienie

1. Zainstaluj Python 3.10+.
2. W katalogu projektu uruchom `pip install -r requirements.txt`.
3. Sprawdź demonstrację bez logowania: `python outlook_cleaner.py --demo`.
4. Zmień ustawienia w `config.example.json` albo skopiuj je do własnego pliku i użyj `--config moja-konfiguracja.json`.
5. Zarejestruj aplikację Microsoft Entra z obsługą osobistych kont Microsoft, logowaniem device-code i delegowanym `Mail.ReadWrite`.
6. W PowerShell ustaw `$env:OUTLOOK_CLIENT_ID="TWOJ_CLIENT_ID"`.
7. Uruchom `python outlook_cleaner.py` — to **podgląd, bez przenoszenia**.
8. Po dokładnej kontroli: `python outlook_cleaner.py --apply --yes`.

## Testy

```bash
python -m unittest discover -s tests -v
```

## Bezpieczeństwo

Nie wpisuj haseł, tokenów ani prawdziwych adresów prywatnych do publicznego repozytorium. Program nie opróżnia Kosza, nie usuwa trwale i nie ma wbudowanego harmonogramu. Dla użytkowników ChatGPT dostępna jest osobna [instrukcja](INSTRUKCJA_CHATGPT.md).
