import json
from colorama import Fore, Style, init
import requests
from fake_useragent import UserAgent
from src.utils import get_headers
import time
from src.__init__ import read_config
from requests.exceptions import ConnectionError, Timeout

init(autoreset=True)
ua = UserAgent()
config = read_config()
timeouts = config.get('loop',3800)

def get_token(init_data_raw, retries=5, backoff_factor=0.5, timeout=timeouts):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})

    for attempt in range(retries):
        try:
            res = requests.post(url, headers=headers, data=data, timeout=timeout)
            res.raise_for_status()
            return res.json()['authToken']
        except (ConnectionError, Timeout) as e:
            print(Fore.RED + Style.BRIGHT + f"Connection error on attempt {attempt + 1}: {e}", flush=True)
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Failed Get Token. Error: {e}", flush=True)
            try:
                error_data = res.json()
                if "invalid" in error_data.get("error_code", "").lower():
                    print(Fore.RED + Style.BRIGHT + "Failed Get Token. Invalid init data", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"Failed Get Token. {error_data}", flush=True)
            except Exception as json_error:
                print(Fore.RED + Style.BRIGHT + f"Failed Get Token and unable to parse error response: {json_error}", flush=True)
            return None
        time.sleep(backoff_factor * (2 ** attempt))
    print(Fore.RED + Style.BRIGHT + "Failed to get token after multiple attempts.", flush=True)
    return None

def authenticate(token):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers = get_headers(token)
    
    try:
        res = requests.post(url, headers=headers)
        res.raise_for_status()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Token Failed : {token[:4]}********* | Status : {res.status_code} | Error: {e}", flush=True)
        return None

    return res

