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
mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX

def print_with_timestamp(message, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    print(f"{htm}[{current_time}] {message}", flush=flush, end=end)

def print_line():
    print(pth + "~" * 60)

def countdown_timer(seconds):
    while seconds:
        menit, detik = divmod(seconds, 60)
        jam, menit = divmod(menit, 60)
        jam = str(jam).zfill(2)
        menit = str(menit).zfill(2)
        detik = str(detik).zfill(2)
        print(f"{pth}please wait until {jam}:{menit}:{detik} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print("                          ", flush=True, end="\r")

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def format_number(number):
    return locale.format_string("%d", number, grouping=True)

def sync_clicker(token):
    url = 'https://api.hamsterkombat.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def list_tasks(token):
    url = 'https://api.hamsterkombat.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def check_task(token, task_id):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    return response

def tap(token, tap_count, available_taps):
    url = 'https://api.hamsterkombat.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": tap_count, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def tap_until_exhausted(token):
    while True:
        clicker_data = sync_clicker(token)

        if 'clickerUser' in clicker_data:
            user_info = clicker_data['clickerUser']
            available_taps = user_info['availableTaps']
            max_taps = user_info['maxTaps']
            
            while available_taps > 100:
                taps_to_perform = max_taps
                response = tap(token, taps_to_perform, max_taps)
                print_with_timestamp(
                        f"{hju}Available energy to tap {pth}{format_number(available_taps)}\r"
                    )
                
                if response.status_code == 200:
                    clicker_data = sync_clicker(token)
                    available_taps = clicker_data['clickerUser']['availableTaps']

                    print_with_timestamp(
                        f"{hju}Success tapping, {pth}{format_number(available_taps)}{kng} remaining\r"
                    )
                else:
                    print_with_timestamp(f"{mrh}Taptap {kng}failed to make a tap\r")
                    break
            break
        else:
            print_with_timestamp(f"{mrh}Error {kng}Unable to retrieve clicker data\r" + Style.RESET_ALL)
            break

def claim_daily(token):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    data = response.json()
    if response.status_code == 200:
        if data['task']['completedAt']:
            print_with_timestamp(f"{hju}Daily streaks {pth}already claimed\r" + Style.RESET_ALL)
        else:
            print_with_timestamp(f"{hju}Daily streaks {pth}claimed successfully\r" + Style.RESET_ALL)
    else:
        print_with_timestamp(f"{mrh}Daily streaks", data.get('error', 'Unknown error') + Style.RESET_ALL)
    return response

def execute_tasks(token, cek_task_dict):
    if token not in cek_task_dict:
        cek_task_dict[token] = False
    if not cek_task_dict[token]:
        response = list_tasks(token)
        cek_task_dict[token] = True
        if response.status_code == 200:
            tasks = response.json()['tasks']
            all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
            if all_completed:
                print_with_timestamp(f"{hju}Tasks {kng}all task claimed successfully\r", flush=True)
            else:
                for task in tasks:
                    if not task['isCompleted']:
                        response = check_task(token, task['id'])
                        if response.status_code == 200 and response.json()['task']['isCompleted']:
                            print_with_timestamp(f"{hju}Tasks {pth}{task['id']}\r", flush=True)
                            print_with_timestamp(f"{hju}Claim success & get {pth}+{task['rewardCoins']} coin\r", flush=True)
                        else:
                            print_with_timestamp(f"{hju}Tasks {mrh}failed {pth}{task['id']}\r", flush=True)
        else:
            print_with_timestamp(f"{hju}Tasks {mrh}failed to get list {pth}{response.status_code}\r", flush=True)

def upgrade(token, boost_type):
    url = 'https://api.hamsterkombat.io/clicker/boosts-for-buy'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": boost_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def full_boost_tap(token):
    boost_type = "BoostFullAvailableTaps"
    response = upgrade(token, boost_type)
    if response.status_code == 200:
        response_data = response.json()
        if 'cooldownSeconds' in response_data:
            cooldown = response_data['cooldownSeconds']
            print_with_timestamp(f"{mrh}Failed ! boost cooldown: {kng}{cooldown} seconds remaining.")
            return False
        else:
            print_with_timestamp(f"{hju}Boost {kng}successfully applied!")
            return True
    else:
        print_with_timestamp(f"{mrh}Failed {kng}boost on cooldown or unavailable")
        return False

def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombat.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def get_available_upgrades(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['upgradesForBuy']
    else:
        print_with_timestamp(mrh + f"Failed to get upgrade list: {response.json()}\r", flush=True)
        return []

def auto_upgrade_passive_earn(token, upgrade_method):
    clicker_data = sync_clicker(token)

    if 'clickerUser' in clicker_data:
        user_info = clicker_data['clickerUser']
        balance_coins = user_info['balanceCoins']
    else:
        print(mrh + f"Failed to get user data\r", flush=True)
        return

    upgrades = get_available_upgrades(token)
    if not upgrades:
        print(mrh + f"\rFailed to get data or no upgrades available\r", flush=True)
        return

    max_price = 5000000
    if upgrade_method == '1':
        upgrades_sorted = sorted(upgrades, key=lambda x: (-x['profitPerHour'], x['price']))
    elif upgrade_method == '2':
        upgrades_sorted = sorted(upgrades, key=lambda x: x['price'])
    elif upgrade_method == '3':
        upgrades_sorted = [u for u in upgrades if u['price'] <= balance_coins and u['price'] <= max_price]
        if not upgrades_sorted:
            print(mrh + f"No upgrade available less than balance\r", flush=True)
            return
    else:
        print(mrh + "Invalid option please try again", flush=True)
        return

    for upgrade in upgrades_sorted:
        if upgrade['isAvailable'] and not upgrade['isExpired']:
            print_with_timestamp(f"{pth}{upgrade['name']} {hju}| cost : {kng}{upgrade['price']}")
            print_with_timestamp(f"{hju}Trying to upgrade {pth}{upgrade['name']}", flush=True, end='\r')
            status = buy_upgrade(token, upgrade['id'], upgrade['name'], upgrade['level'], upgrade['profitPerHour'])
            
            if status == 'insufficient_funds':
                print_with_timestamp(f"{mrh}Not enough coin to upgrade                      \r", flush=True)
                break
            elif status == 'success':
                continue  # Skip to the next iteration if the upgrade is successful
            else:
                print_with_timestamp(f"{hju}Upgrade {mrh}failed {hju}to {pth}level {upgrade['level']}                  \r", flush=True)
   
def buy_upgrade(token: str, upgrade_id: str, upgrade_name: str, level: int, profitPerHour: float) -> str:
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print_with_timestamp(f"{hju}Success | Level {pth}+{level} | +{kng}{profitPerHour}{pth}/h         \r", flush=True)
        return 'success'
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
            print_with_timestamp(kng + f"Insufficient funds: {pth}{upgrade_name} ", flush=True)
            return 'insufficient_funds'
        elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
            cooldown_time = error_response.get('cooldownSeconds')
            print_with_timestamp(hju + f"Item {kng}cooldown for {pth}{cooldown_time} {kng}seconds.", flush=True)
            return 'cooldown'
        elif error_response.get('error_code') == 'UPGRADE_MAX_LEVEL':
            error_messages = error_response.get('error_message')
            print_with_timestamp(hju + f"{error_messages}", flush=True)
            return 'max_level'
        elif error_response.get('error_code') == 'UPGRADE_NOT_AVAILABLE':
            error_messages = error_response.get('error_message')
            print_with_timestamp(kng + f"{error_messages}.", flush=True)
            return 'not_available'
        elif error_response.get('error_code') == 'UPGRADE_HAS_EXPIRED':
            error_messages = error_response.get('error_message')
            print_with_timestamp(kng + f"Item {pth}{upgrade_name} {kng}has expired", flush=True)
            return 'expired'
        else:
            print_with_timestamp(hju + f"{response.json()}", flush=True)
            return 'error'

def claim_daily_combo(token: str) -> bool:
    url = 'https://api.hamsterkombat.io/clicker/claim-daily-combo'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        bonus_coins = data.get('dailyCombo', {}).get('bonusCoins', 0)
        print_with_timestamp(f"{hju}Success claim combo {kng}+{bonus_coins} coins.\r")
        return True
    elif response.status_code == 400:
        error_response = response.json()
        if error_response.get('error_code') == 'DAILY_COMBO_NOT_READY':
            error_message = error_response.get('error_message')
            print_with_timestamp(f"{kng}{error_message}\r")
        else:
            print_with_timestamp(f"{mrh}Failed to claim daily combo {response.json()}\r")
        return False
    else:
        print_with_timestamp(f"{mrh}Failed to claim daily combo {response.json()}\r")
        return False

def execute_combo(token: str, username: str):
    combo = read_combo_file()
    combo_log = read_combo_log(username)
    combo_purchased = True

    if 'DAILY_COMBO_DOUBLE_CLAIMED' in combo_log:
        print_with_timestamp(kng + "Combo has already claimed before", flush=True)
        return
    
    for combo_item in combo:
        if combo_item in combo_log:
            print_with_timestamp(pth + f"{combo_item} {kng}have purchased before", flush=True)
            continue
        
        # Retrieve upgrade details for the combo item
        upgrades = get_available_upgrades(token)
        upgrade_details = next((u for u in upgrades if u['id'] == combo_item), None)
        if upgrade_details is None:
            print_with_timestamp(mrh + f"Failed to find details for {pth}{combo_item}", flush=True)
            continue
        
        status = buy_upgrade(token, combo_item, combo_item, upgrade_details['level'], upgrade_details['profitPerHour'])
        if status == 'success':
            print_with_timestamp(hju + f"Executed combo {pth}{combo_item} ", flush=True)
            combo_log.add(combo_item)
        elif status == 'insufficient_funds':
            combo_purchased = False
            print_with_timestamp(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
            break
        elif status == 'cooldown':
            print_with_timestamp(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        elif status == 'max_level':
            print_with_timestamp(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        elif status == 'not_available':
            print_with_timestamp(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        elif status == 'expired':
            print_with_timestamp(mrh + f"Failed to buy {pth}{combo_item}", flush=True)
        else:
            print_with_timestamp(mrh + f"Failed to buy {pth}{combo_item}. Error: {status}.", flush=True)
            break
    
    if combo_purchased:
        if claim_daily_combo(token):
            print_with_timestamp(kng + "Successfully claimed daily combo.", flush=True)
            combo_log.add('DAILY_COMBO_DOUBLE_CLAIMED')
        else:
            print_with_timestamp(mrh + "Failed to claim daily combo.", flush=True)
    else:
        print_with_timestamp(kng + "Incomplete combo purchase, switching.", flush=True)
    
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
   
def claim_daily_cipher(token):
    url_claim = 'https://api.hamsterkombat.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    
    with open('data/cipher.txt', 'r') as file:
        cipher_word = file.read().strip()
    
    data = {"cipher": cipher_word}
    print_with_timestamp(f"{hju}today morse is {pth}'{cipher_word}'\r", flush=True)
    response_claim = requests.post(url_claim, headers=headers, json=data)
    
    if response_claim.status_code == 200:
        data = response_claim.json()
        if data.get('dailyCipher', {}).get('isClaimed', True):
            print_with_timestamp(
                f"{hju}Successfully claim morse.", flush=True
                )
        else:
            print_with_timestamp(
                f"{mrh}Failed to claim morse.", flush=True
                )
            return False
    else:
        print_with_timestamp(
            f"{kng}Already claim this morse before.", flush=True
            )
        return False
