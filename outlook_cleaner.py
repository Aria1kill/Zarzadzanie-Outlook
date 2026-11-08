#!/usr/bin/env python3
"""Zarządzanie Twoją Pocztą — skrypt Outlook/Hotmail. Domyślnie podgląd."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import time

GRAPH = "https://graph.microsoft.com/v1.0"
CONFIG = Path(__file__).with_name("config.example.json")
PROTECTED = ("faktur", "invoice", "rachun", "paragon", "płatno", "payment", "transakcj", "przelew", "windyk", "zadłuż", "zaległo", "wezwanie", "reklamacj", "zwrot", "refund", "spór", "weryfik", "verify", "security", "bezpieczeństw", "alert", "logowan", "hasł", "password", "blokad", "niepowodzen", "problem", "odrzucon", "nieudana", "nieopłacon", "preautoryzacj", "abonament", "subskrypcj", "zamówieni", "order", "umow", "contract", "dokument", "kod", "2fa", "otp")
MARKETING = ("newsletter", "wyprzedaż", "promocj", "rabat", "zniżk", "kupon", "sale", "discount", "special offer", "black friday")
LIST_KEYS = ("protected_senders", "protected_domains", "protected_keywords", "blocked_senders", "blocked_domains", "blocked_keywords")


def norm(value):
    return str(value or "").casefold().strip()


def matches(text, words):
    return any(norm(word) in text for word in words if norm(word))


def sender_matches(address, addresses, domains):
    address = norm(address)
    if address in addresses:
        return True
    if "@" not in address:
        return False
    domain = address.rsplit("@", 1)[1]
    return any(domain == d or domain.endswith("." + d) for d in domains)


def load_config(path):
    with open(path, encoding="utf-8") as stream:
        config = json.load(stream)
    if not isinstance(config, dict):
        raise ValueError("Ustawienia muszą być obiektem JSON")
    unknown = set(config) - set(LIST_KEYS) - {"min_age_days", "max_moves", "use_default_marketing_rules"}
    if unknown:
        raise ValueError("Nieznane ustawienia: " + ", ".join(sorted(unknown)))
    for key in LIST_KEYS:
        items = config.get(key, [])
        if not isinstance(items, list) or any(not isinstance(x, str) or not x.strip() for x in items):
            raise ValueError(key + ": wymagana lista niepustych napisów")
        config[key] = [norm(x) for x in items]
    for key, default, lower, upper in (("min_age_days", 7, 0, 3650), ("max_moves", 25, 1, 500)):
        value = config.get(key, default)
        if type(value) is not int or not lower <= value <= upper:
            raise ValueError(f"{key}: podaj liczbę całkowitą {lower}–{upper}")
        config[key] = value
    value = config.get("use_default_marketing_rules", True)
    if type(value) is not bool:
        raise ValueError("use_default_marketing_rules musi być true lub false")
    config["use_default_marketing_rules"] = value
    return config


def classify(message, config, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    subject = norm(message.get("subject"))
    preview = norm(message.get("bodyPreview"))
    text = subject + " " + preview
    address = norm(((message.get("from") or {}).get("emailAddress") or {}).get("address"))
    if sender_matches(address, config["protected_senders"], config["protected_domains"]):
        return None
    if matches(text, PROTECTED) or matches(text, config["protected_keywords"]):
        return None
    try:
        received = dt.datetime.fromisoformat(message["receivedDateTime"].replace("Z", "+00:00"))
        if received.tzinfo is None:
            return None
        age = (now - received).total_seconds() / 86400
    except (KeyError, AttributeError, TypeError, ValueError):
        return None
    if age < config["min_age_days"]:
        return None
    if sender_matches(address, config["blocked_senders"], config["blocked_domains"]):
        return "wybrany nadawca"
    if matches(text, config["blocked_keywords"]):
        return "własne słowo kluczowe"
    if config["use_default_marketing_rules"] and matches(subject, MARKETING):
        return "reklama lub newsletter"
    return None


def graph_request(method, url, token, **kwargs):
    import requests
    for attempt in range(5):
        response = requests.request(method, url, headers={"Authorization": "Bearer " + token, "Accept": "application/json"}, timeout=35, **kwargs)
        if response.status_code in (429, 500, 502, 503, 504):
            try:
                delay = min(max(int(response.headers.get("Retry-After", "2")), 0), 30)
            except ValueError:
                delay = 2
            time.sleep(delay + attempt)
            continue
        response.raise_for_status()
        return response.json() if response.content else {}
    raise RuntimeError("Microsoft Graph chwilowo niedostępny")


def authenticate(client_id):
    import msal
    app = msal.PublicClientApplication(client_id, authority="https://login.microsoftonline.com/consumers")
    flow = app.initiate_device_flow(scopes=["Mail.ReadWrite"])
    if "user_code" not in flow:
        raise RuntimeError("Nie można rozpocząć logowania Microsoft")
    print(flow["message"], flush=True)
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Błąd logowania"))
    return result["access_token"]


def run(args):
    config = load_config(args.config)
    limit = args.max_moves if args.max_moves is not None else config["max_moves"]
    if not 1 <= limit <= 500:
        raise ValueError("Limit musi wynosić od 1 do 500")
    if args.apply and not args.yes:
        raise ValueError("Użyj --apply --yes po sprawdzeniu podglądu")
    if args.demo:
        now = dt.datetime.now(dt.timezone.utc)
        for subject in ("Newsletter: promocja weekendowa", "Faktura za zamówienie"):
            sample = {"subject": subject, "bodyPreview": "", "receivedDateTime": (now - dt.timedelta(days=15)).isoformat(), "from": {"emailAddress": {"address": "news@sklep.pl"}}}
            print(subject, "→", classify(sample, config, now) or "ZACHOWAJ")
        return
    client_id = os.environ.get("OUTLOOK_CLIENT_ID")
    if not client_id:
        raise ValueError("Ustaw OUTLOOK_CLIENT_ID — zobacz README.md")
    token = authenticate(client_id)
    url = GRAPH + "/me/mailFolders/inbox/messages?$top=100&$select=id,subject,receivedDateTime,from,bodyPreview&$orderby=receivedDateTime%20desc"
    checked = selected = moved = errors = 0
    while url and selected < limit:
        page = graph_request("GET", url, token)
        for msg in page.get("value", []):
            checked += 1
            reason = classify(msg, config)
            if not reason:
                continue
            selected += 1
            print(f"{'[PRZENOSZĘ]' if args.apply else '[PODGLĄD]'} {msg.get('subject','')[:100]} — {reason}")
            if args.apply:
                try:
                    graph_request("POST", GRAPH + "/me/messages/" + msg["id"] + "/move", token, json={"destinationId": "deleteditems"})
                    moved += 1
                except Exception as exc:
                    errors += 1
                    print("Błąd przenoszenia:", exc, file=sys.stderr)
            if selected >= limit:
                break
        url = page.get("@odata.nextLink")
        if url and not url.startswith(GRAPH + "/"):
            raise RuntimeError("Nieoczekiwany adres kolejnej strony")
    print(f"Sprawdzono: {checked} | wybrano: {selected} | przeniesiono: {moved} | błędy: {errors}")
    print("Cała skrzynka sprawdzona:", "TAK" if not url else "NIE — osiągnięto limit")
    if errors:
        raise RuntimeError("Niektóre wiadomości nie zostały przeniesione")


def main():
    parser = argparse.ArgumentParser(description="Zarządzanie Twoją Pocztą — Outlook/Hotmail, własne reguły i podgląd")
    parser.add_argument("--config", default=str(CONFIG), help="Ścieżka do ustawień JSON")
    parser.add_argument("--demo", action="store_true", help="Przykład bez logowania")
    parser.add_argument("--apply", action="store_true", help="Przenoś do Kosza")
    parser.add_argument("--yes", action="store_true", help="Potwierdzenie przenoszenia")
    parser.add_argument("--max-moves", type=int, help="Limit kandydatów")
    args = parser.parse_args()
    try:
        run(args)
    except (ValueError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Błąd: {exc}\n")


if __name__ == "__main__":
    main()
