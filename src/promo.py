import requests
from src.utils import get_headers
from src.__init__ import countdown_timer, log, hju, kng, mrh,pth

def load_promo(filename='promo.txt'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def save_promo(codes, filename='promo.txt'):
    with open(filename, 'w') as file:
        file.writelines(f"{code}\n" for code in codes)

def redeem_promo(token):
    promo_codes = load_promo()
    
    if not promo_codes:
        log(mrh + f"No codes available in {pth}promo.txt.")
        return

    max_attempts = 4
    attempts = 0

    while attempts < max_attempts:
        promo_code = promo_codes[0]
        url = 'https://api.hamsterkombatgame.io/clicker/apply-promo'
        headers = get_headers(token)
        payload = {"promoCode": promo_code}
        
        try:
            res = requests.post(url, headers=headers, json=payload)
            res.raise_for_status()

            if res.status_code == 200:
                log(hju + f"Applied Promo {pth}{promo_code}.")
                promo_codes.pop(0)
                save_promo(promo_codes)
                countdown_timer(5)
                attempts = 0
            else:
                log(kng + f"Error while applying promo code")
                break
                
        except requests.exceptions.HTTPError as e:
            log(kng + f"4/4 Promo has been applied")
        except Exception as err:
            log(f"Error: {err}. Promo code: {promo_code}")

        attempts += 1

    if attempts >= max_attempts:
        log(mrh + "Max code attempts reached.")
