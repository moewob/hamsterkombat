import requests
import json
from src.utils import get_headers
from colorama import Fore, Style

def get_token(init_data_raw):
    url = 'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['authToken']
    else:
        error_data = response.json()
        if "invalid" in error_data.get("error_code", "").lower():
            print(Fore.RED + Style.BRIGHT + "\rFailed Get Token. Invalid init data", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\rFailed Get Token. {error_data}", flush=True)
        return None

def authenticate(token):
    url = 'https://api.hamsterkombat.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    
    if response.status_code != 200:
        print(Fore.RED + Style.BRIGHT + f"Gagal login token : {token[:4]}********* | Status Code: {response.status_code} | Response: {response.text}")
    return response
