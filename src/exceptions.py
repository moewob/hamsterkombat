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
merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX

def print_with_timestamp(message, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    print(f"{hitam}[{current_time}] {message}", flush=flush, end=end)
def print_line():
    print(putih + "~" * 60)

LOG_DIR = 'logs/combo_logs'

# Set the locale to use comma as thousand separator and dot as decimal separator
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def countdown_timer(seconds):
    while seconds:
        menit, detik = divmod(seconds, 60)
        jam, menit = divmod(menit, 60)
        jam = str(jam).zfill(2)
        menit = str(menit).zfill(2)
        detik = str(detik).zfill(2)
        print(f"{Fore.WHITE}please wait until {jam}:{menit}:{detik} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print("                          ", flush=True, end="\r")

def format_number(number):
    return locale.format_string("%d", number, grouping=True)

def read_combo_log(token):
    log_file = os.path.join(LOG_DIR, f'combo_log_{token[:9]}.txt')
    combo_log = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            combo_log = set(file.read().splitlines())
    return combo_log

def write_combo_log(token, combo_log):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file = os.path.join(LOG_DIR, f'combo_log_{token[:9]}.txt')
    with open(log_file, 'w') as file:
        file.write('\n'.join(combo_log))

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
                        f"{hijau}available to tap {putih}{format_number(available_taps)}\r"
                    )
                
                if response.status_code == 200:
                    clicker_data = sync_clicker(token)
                    available_taps = clicker_data['clickerUser']['availableTaps']

                    print_with_timestamp(
                        f"{hijau}success tapping, {putih}{format_number(available_taps)}{kuning} remaining\r"
                    )
                else:
                    print_with_timestamp(f"{merah}taptap {kuning}failed to make a tap\r")
                    break
            break
        else:
            print_with_timestamp(f"{merah}error {kuning}Unable to retrieve clicker data\r" + Style.RESET_ALL)
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
            print_with_timestamp(f"{hijau}daily streaks {putih}already claimed\r" + Style.RESET_ALL)
        else:
            print_with_timestamp(f"{hijau}daily streaks {putih}claimed successfully\r" + Style.RESET_ALL)
    else:
        print_with_timestamp(f"{merah}daily streaks", data.get('error', 'Unknown error') + Style.RESET_ALL)
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
                print_with_timestamp(f"{hijau}tasks: {kuning}all task claimed successfully\r", flush=True)
            else:
                for task in tasks:
                    if not task['isCompleted']:
                        response = check_task(token, task['id'])
                        if response.status_code == 200 and response.json()['task']['isCompleted']:
                            print_with_timestamp(f"{hijau}tasks: {putih}{task['id']}\r", flush=True)
                            print_with_timestamp(f"{hijau}claim success & get {putih}+{task['rewardCoins']} coin\r", flush=True)
                        else:
                            print_with_timestamp(f"{hijau}tasks: {merah}failed {putih}{task['id']}\r", flush=True)
        else:
            print_with_timestamp(f"{hijau}tasks: {merah}failed to get list {putih}{response.status_code}\r", flush=True)

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
            cooldown_seconds = response_data['cooldownSeconds']
            print_with_timestamp(f"{merah}Failed ! boost cooldown: {kuning}{cooldown_seconds} seconds remaining.")
            return False
        else:
            print_with_timestamp(f"{hijau}Boost {kuning}successfully applied!")
            return True
    else:
        print_with_timestamp(f"{merah}Failed {kuning}boost on cooldown.")
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
        print_with_timestamp(Fore.GREEN + Style.BRIGHT + f"succes to get upgrade list\r", flush=True)
        return response.json()['upgradesForBuy']
    else:
        print_with_timestamp(Fore.RED + Style.BRIGHT + f"failed to get upgrade list: {response.json()}\r", flush=True)
        return []

def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return 'success'
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
            return 'insufficient_funds'
        elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
            return f"cooldown: {error_response.get('error_message')}"
        else:
            return f"error: {response.json()}"

def auto_upgrade_passive_earn(token, upgrade_method):
    clicker_data = sync_clicker(token)

    if 'clickerUser' in clicker_data:
        user_info = clicker_data['clickerUser']
        balance_coins = user_info['balanceCoins']
    else:
        print(Fore.RED + Style.BRIGHT + f"failed to get user data\r", flush=True)
        return

    upgrades = get_available_upgrades(token)
    if not upgrades:
        print(Fore.RED + Style.BRIGHT + f"\rfailed to get data or no upgrades available\r", flush=True)
        return

    if upgrade_method == '1':
        # Sort upgrades by profit per hour descending
        upgrades_sorted = sorted(upgrades, key=lambda x: (-x['profitPerHour'], x['price']))
    elif upgrade_method == '2':
        # Sort upgrades by price ascending
        upgrades_sorted = sorted(upgrades, key=lambda x: x['price'])
    elif upgrade_method == '3':
        # Filter upgrades to keep only those with a price less than or equal to balance_coins
        upgrades_sorted = [u for u in upgrades if u['price'] <= balance_coins]
        if not upgrades_sorted:
            print(Fore.RED + Style.BRIGHT + f"no upgrade available less than balance\r", flush=True)
            return
    else:
        print(Fore.RED + Style.BRIGHT + "Pilihan tidak valid\r", flush=True)
        return

    for upgrade in upgrades_sorted:
        if upgrade['isAvailable'] and not upgrade['isExpired']:
            print_with_timestamp(f"{Fore.WHITE}{upgrade['name']} {Fore.GREEN}| cost : {Fore.YELLOW}{upgrade['price']}")
            print_with_timestamp(f"{Fore.GREEN}trying to upgrade {Fore.WHITE}{upgrade['name']}", flush=True, end='\r')
            status = buy_upgrade(token, upgrade['id'], upgrade['name'])
            time.sleep(random.uniform(0.2, 0.5))
            
            if status == 'success':
                print_with_timestamp(f"{Fore.GREEN}success | Level {Fore.WHITE}+{upgrade['level']} | +{Fore.YELLOW}{upgrade['profitPerHour']}{Fore.WHITE}/h         \r", flush=True)
            elif status == 'insufficient_funds':
                print_with_timestamp(f"{Fore.RED}not enough coin to upgrade                      \r", flush=True)
                break
            elif status.startswith('cooldown'):
                print_with_timestamp(f"{Fore.RED}{status.split(': ')[1]}\r", flush=True)
            else:
                print_with_timestamp(f"{Fore.RED}{status.split(': ')[1]}\r", flush=True)


def claim_daily_combo(token):
    url = 'https://api.hamsterkombat.io/clicker/claim-daily-combo'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        bonus_coins = data.get('dailyCombo', {}).get('bonusCoins', 0)
        print_with_timestamp(f"{hijau}Successfully claimed daily combo {kuning}+{format_number(bonus_coins)} coins.\r", flush=True)
        return True
    else:
        print_with_timestamp(f"{merah}Failed to claim daily combo {response.json()}\r", flush=True)
        return False

def execute_combo(token, username):
    combo = read_combo_file()
    combo_log = read_combo_log(username)
    all_items_bought = True

    if 'DAILY_COMBO_DOUBLE_CLAIMED' in combo_log:
        print_with_timestamp(f"{kuning}Combo already claimed before\r", flush=True)
        return
    
    for combo_item in combo:
        if combo_item not in combo_log: 
            print_with_timestamp(f"{hijau}Trying to buy: {putih}{combo_item}\r", flush=True)
            if not buy_upgrade(token, combo_item, combo_item):
                all_items_bought = False
                print_with_timestamp(f"{merah}Failed to buy: {kuning}{combo_item}\r", flush=True)
                break 
            else:
                print_with_timestamp(f"{hijau}Successfully bought: {putih}{combo_item}\r", flush=True)
                combo_log.add(combo_item)
        else:
            print_with_timestamp(f"{kuning}Item already bought: {putih}{combo_item}\r", flush=True)


    if all_items_bought and len(combo_log) == len(combo):
        if claim_daily_combo(token):
            combo_log.add('DAILY_COMBO_DOUBLE_CLAIMED')
        write_combo_log(username, combo_log)
    else:
        print_with_timestamp(f"{merah}Combo purchase is not complete\r", flush=True)
        write_combo_log(username, combo_log)

def read_combo_file():
    combo = []
    combo_file_path = os.path.join(os.path.dirname(__file__), '../data/combo.txt')
    with open(combo_file_path, 'r') as file:
        combo = file.read().splitlines()
    return combo

def read_combo_log(username):
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

def write_combo_log(username, combo_log):
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
    print_with_timestamp(f"{hijau}today morse is {putih}'{cipher_word}'\r", flush=True)
    response_claim = requests.post(url_claim, headers=headers, json=data)
    
    if response_claim.status_code == 200:
        data = response_claim.json()
        time.sleep(random.uniform(0.2, 1.1))
        if data.get('dailyCipher', {}).get('isClaimed', True):
            print_with_timestamp(
                f"{hijau}successfully claim morse.\r", flush=True
                )
        else:
            print_with_timestamp(
                f"{merah}failed to claim morse.\r", flush=True
                )
            return False
    else:
        print_with_timestamp(
            f"{kuning}already claim this morse before.\r", flush=True
            )
        return False
