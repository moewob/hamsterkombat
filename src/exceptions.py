import os
import sys
import json
import time
import locale
from datetime import datetime
import random
import requests
from colorama import *
from src.utils import get_headers
from src.__init__ import mrh, pth, hju, kng, bru, reset, htm

def log(message, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    print(f"{htm}[{current_time}] {message}", flush=flush, end=end)

def log_line():
    print(pth + "~" * 60)

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print("                          ", flush=True, end="\r")

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def _number(number):
    return locale.format_string("%d", number, grouping=True)

def clicker_config(token):
    url = 'https://api.hamsterkombatgame.io/clicker/config'
    headers = get_headers(token)
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return {}
    
def _sync(token):
    url = 'https://api.hamsterkombatgame.io/clicker/sync'
    headers = get_headers(token)
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return {}

def _list(token):
    url = 'https://api.hamsterkombatgame.io/clicker/list-tasks'
    headers = get_headers(token)
    res = requests.post(url, headers=headers)
    return res

def _check(token, task_id):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    res = requests.post(url, headers=headers, data=data)
    return res

def tap(token, tap_count, available_taps):
    url = 'https://api.hamsterkombatgame.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": tap_count, "availableTaps": available_taps, "timestamp": int(time.time())})
    res = requests.post(url, headers=headers, data=data)
    return res

def exhausted(token):
    while True:
        clicker_data = _sync(token)

        if 'clickerUser' in clicker_data:
            user_info = clicker_data['clickerUser']
            available_taps = user_info['availableTaps']
            max_taps = user_info['maxTaps']
            
            while available_taps > 100:
                _perform = max_taps
                res = tap(token, _perform, max_taps)
                log(
                        f"{hju}Available energy to tap {pth}{_number(available_taps)}\r"
                    )
                
                if res.status_code == 200:
                    clicker_data = _sync(token)
                    available_taps = clicker_data['clickerUser']['availableTaps']

                    log(
                        f"{hju}Success tapping, {pth}{_number(available_taps)}{kng} remaining\r"
                    )
                else:
                    log(f"{mrh}Failed to make a tap\r")
                    break
            break
        else:
            log(f"{mrh}Error {kng}Unable to retrieve clicker data\r" + Style.RESET_ALL)
            break

def claim_daily(token):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    res = requests.post(url, headers=headers, data=data)
    data = res.json()
    if res.status_code == 200:
        if data['task']['completedAt']:
            log(f"{hju}Daily streaks {pth}already claimed\r" + Style.RESET_ALL)
        else:
            log(f"{hju}Daily streaks {pth}claimed successfully\r" + Style.RESET_ALL)
    else:
        log(f"{mrh}Daily streaks", data.get('error', 'Unknown error') + Style.RESET_ALL)
    return res

def execute(token, cek_task_dict):
    if token not in cek_task_dict:
        cek_task_dict[token] = False
    if not cek_task_dict[token]:
        res = _list(token)
        cek_task_dict[token] = True
        if res.status_code == 200:
            tasks = res.json()['tasks']
            all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
            if all_completed:
                log(f"{hju}Tasks {kng}all task claimed successfully\r", flush=True)
            else:
                for task in tasks:
                    if not task['isCompleted']:
                        res = _check(token, task['id'])
                        if res.status_code == 200 and res.json()['task']['isCompleted']:
                            log(f"{hju}Tasks {pth}{task['id']}\r", flush=True)
                            log(f"{hju}Claim success & get {pth}+{task['rewardCoins']} coin\r", flush=True)
                        else:
                            log(f"{hju}Tasks {mrh}failed {pth}{task['id']}\r", flush=True)
        else:
            log(f"{hju}Tasks {mrh}failed to get list {pth}{res.status_code}\r", flush=True)

def upgrade(token, boost_type):
    url = 'https://api.hamsterkombatgame.io/clicker/boosts-for-buy'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": boost_type, "timestamp": int(time.time())})
    res = requests.post(url, headers=headers, data=data)
    return res

def boost(token):
    boost_type = "BoostFullAvailableTaps"
    res = upgrade(token, boost_type)
    if res.status_code == 200:
        res_data = res.json()
        if 'cooldownSeconds' in res_data:
            cooldown = res_data['cooldownSeconds']
            log(f"{kng}Boost cooldown: {kng}{cooldown} seconds remaining.")
            return False
        else:
            log(f"{hju}Boost {kng}successfully applied!")
            return True
    else:
        log(f"{kng}boost on cooldown or unavailable")
        return False

def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    res = requests.post(url, headers=headers, data=data)
    return res

def available_upgrades(token):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        return res.json()['upgradesForBuy']
    else:
        log(mrh + f"Failed to get upgrade list: {res.json()}\r", flush=True)
        return []

def upgrade_passive(token, _method):
    clicker_data = _sync(token)

    if 'clickerUser' in clicker_data:
        user_info = clicker_data['clickerUser']
        balance_coins = user_info['balanceCoins']
    else:
        log(mrh + f"Failed to get user data\r", flush=True)
        return

    upgrades = available_upgrades(token)
    if not upgrades:
        log(mrh + f"\rFailed to get data or no upgrades available\r", flush=True)
        return

    max_price = 5000000
    if _method == '1':
        upg_sort = sorted(upgrades, key=lambda x: (-x['profitPerHour'], x['price']))
    elif _method == '2':
        upg_sort = sorted(upgrades, key=lambda x: x['price'])
    elif _method == '3':
        upg_sort = [u for u in upgrades if u['price'] <= balance_coins and u['price'] <= max_price]
        if not upg_sort:
            log(mrh + f"No upgrade available less than balance\r", flush=True)
            return
    else:
        log(mrh + "Invalid option please try again", flush=True)
        return

    for upgrade in upg_sort:
        if upgrade['isAvailable'] and not upgrade['isExpired']:
            log(f"{pth}{upgrade['name']} {hju}| cost : {kng}{upgrade['price']}")
            log(f"{hju}Trying to upgrade {pth}{upgrade['name']}", flush=True, end='\r')
            status = buy_upgrade(token, upgrade['id'], upgrade['name'], upgrade['level'], upgrade['profitPerHour'])
            
            if status == 'insufficient_funds':
                log(f"{mrh}Not enough coin to upgrade                      \r", flush=True)
                break
            elif status == 'success':
                continue  # Skip to the next iteration if the upgrade is successful
            else:
                log(f"{hju}Upgrade {mrh}failed {hju}to {pth}level {upgrade['level']}                  \r", flush=True)
   
def buy_upgrade(token: str, upgrade_id: str, upgrade_name: str, level: int, profitPerHour: float) -> str:
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        log(f"{hju}Success | Level {pth}+{level} | +{kng}{profitPerHour}{pth}/h         \r", flush=True)
        return 'success'
    else:
        error_res = res.json()
        if error_res.get('error_code') == 'INSUFFICIENT_FUNDS':
            log(kng + f"Insufficient funds: {pth}{upgrade_name} ", flush=True)
            return 'insufficient_funds'
        elif error_res.get('error_code') == 'UPGRADE_COOLDOWN':
            cooldown_time = error_res.get('cooldownSeconds')
            log(hju + f"Item {kng}cooldown for {pth}{cooldown_time} {kng}seconds.", flush=True)
            return 'cooldown'
        elif error_res.get('error_code') == 'UPGRADE_MAX_LEVEL':
            error_messages = error_res.get('error_message')
            log(hju + f"{error_messages}", flush=True)
            return 'max_level'
        elif error_res.get('error_code') == 'UPGRADE_NOT_AVAILABLE':
            error_messages = error_res.get('error_message')
            log(kng + f"{error_messages}.", flush=True)
            return 'not_available'
        elif error_res.get('error_code') == 'UPGRADE_HAS_EXPIRED':
            error_messages = error_res.get('error_message')
            log(kng + f"Item {pth}{upgrade_name} {kng}has expired", flush=True)
            return 'expired'
        else:
            log(hju + f"{res.json()}", flush=True)
            return 'error'

def claim_daily_combo(token: str) -> bool:
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-combo'
    headers = get_headers(token)
    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        bonus_coins = data.get('dailyCombo', {}).get('bonusCoins', 0)
        log(f"{hju}Success claim combo {kng}+{bonus_coins} coins.\r")
        return True
    elif res.status_code == 400:
        error_res = res.json()
        if error_res.get('error_code') == 'DAILY_COMBO_NOT_READY':
            error_message = error_res.get('error_message')
            log(f"{kng}{error_message}\r")
        else:
            log(f"{mrh}Failed to claim daily combo {res.json()}\r")
        return False
    else:
        log(f"{mrh}Failed to claim daily combo {res.json()}\r")
        return False

def execute_combo(token: str, username: str):
    combo = read_combo_file()
    combo_log = read_combo_log(username)
    combo_purchased = True

    if 'DAILY_COMBO_DOUBLE_CLAIMED' in combo_log:
        log(kng + "Combo has already claimed before", flush=True)
        return
    
    for combo_item in combo:
        if combo_item in combo_log:
            log(pth + f"{combo_item} {kng}have purchased before", flush=True)
            continue
        
        # Retrieve upgrade details for the combo item
        upgrades = available_upgrades(token)
        upgrade_details = next((u for u in upgrades if u['id'] == combo_item), None)
        if upgrade_details is None:
            log(mrh + f"Failed to find details for {pth}{combo_item}", flush=True)
            continue
        
        status = buy_upgrade(token, combo_item, combo_item, upgrade_details['level'], upgrade_details['profitPerHour'])
        if status == 'success':
            log(hju + f"Executed combo {pth}{combo_item} ", flush=True)
            combo_log.add(combo_item)
        elif status == 'insufficient_funds':
            combo_purchased = False
            log(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
            break
        elif status == 'cooldown':
            log(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        elif status == 'max_level':
            log(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        elif status == 'not_available':
            log(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        elif status == 'expired':
            log(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        else:
            log(mrh + f"Failed to buy {pth}{combo_item}. Error: {status}.", flush=True)
            break
    
    if combo_purchased:
        if claim_daily_combo(token):
            log(kng + "Successfully claimed daily combo.", flush=True)
            combo_log.add('DAILY_COMBO_DOUBLE_CLAIMED')
        else:
            log(mrh + "Failed to claim daily combo.", flush=True)
    else:
        log(kng + "Incomplete combo purchase, switching.", flush=True)
    
    write_combo_log(username, combo_log)

def read_combo_file() -> list:
    combo = []
    combo_file_path = os.path.join(os.path.dirname(__file__), '../data/combo.txt')
    with open(combo_file_path, 'r') as file:
        combo = file.read().splitlines()
    return combo

def read_combo_log(username: str) -> set:
    log_folder_path = os.path.join(os.path.dirname(__file__), '../logs')
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    log_file_path = os.path.join(log_folder_path, f'combo_log_{username}.txt')
    try:
        with open(log_file_path, 'r') as file:
            combo_log = set(file.read().splitlines())
    except FileNotFoundError:
        combo_log = set()
    return combo_log

def write_combo_log(username: str, combo_log: set):
    log_folder_path = os.path.join(os.path.dirname(__file__), '../logs')
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    log_file_path = os.path.join(log_folder_path, f'combo_log_{username}.txt')
    with open(log_file_path, 'w') as file:
        for item in combo_log:
            file.write(f"{item}\n")
   
def claim_cipher(token):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    
    with open('data/cipher.txt', 'r') as file:
        cipher_word = file.read().strip()
    
    data = {"cipher": cipher_word}
    log(f"{hju}today morse is {pth}'{cipher_word}'\r", flush=True)
    res_claim = requests.post(url, headers=headers, json=data)
    
    if res_claim.status_code == 200:
        data = res_claim.json()
        if data.get('dailyCipher', {}).get('isClaimed', True):
            log(
                f"{hju}Successfully claim morse.", flush=True
                )
        else:
            log(
                f"{mrh}Failed to claim morse.", flush=True
                )
            return False
    else:
        log(
            f"{kng}Already claim this morse before.", flush=True
            )
        return False
