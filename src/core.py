import os
import json
import difflib
import sys
import time
import locale
from datetime import datetime
import requests
from colorama import *

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX

def print_with_timestamp(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{hitam}[{current_time}] {message}")
    sys.stdout.flush()

def print_line():
    print(putih + "~" * 65)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_tokens, get_headers
from src.auth import get_token, authenticate
from src.exceptions import auto_upgrade_passive_earn, claim_daily, execute_tasks
from src.exceptions import sync_clicker, tap_until_exhausted, execute_combo, claim_daily_cipher
from src.exceptions import format_number, full_boost_tap

def print_banner():
    banner = r"""
    ██╗████████╗███████╗     ██╗ █████╗ ██╗    ██╗
    ██║╚══██╔══╝██╔════╝     ██║██╔══██╗██║    ██║
    ██║   ██║   ███████╗     ██║███████║██║ █╗ ██║
    ██║   ██║   ╚════██║██   ██║██╔══██║██║███╗██║
    ██║   ██║   ███████║╚█████╔╝██║  ██║╚███╔███╔╝
    ╚═╝   ╚═╝   ╚══════╝ ╚════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  """ 
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hijau + "    Hamster Kombat Auto Bot")
    print(merah + f"    NOT FOR SALE = Free to use")

def get_status_text(status):
    if status:
        return Fore.GREEN + "ON" + Style.RESET_ALL
    else:
        return Fore.RED + "OFF" + Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(auto_buy_upgrade, combo_upgrade, daily_cipher_on, tasks_on):
    clear_screen()
    print_banner()
    print(Fore.YELLOW + Style.BRIGHT + f"\n   ----- Config -----")
    print(f"  1. Auto Buy Upgrade           : {get_status_text(auto_buy_upgrade)}")
    print(f"  2. Auto Complete Combo        : {get_status_text(combo_upgrade)}")
    print(f"  3. Auto Complete Daily Cipher : {get_status_text(daily_cipher_on)}")
    print(f"  4. Auto Complete Tasks        : {get_status_text(tasks_on)}")
    print(f"\n  {kuning}[ without config will execute {hijau}taps & boost {kuning}only ]\n")
    print(f"  5. {hijau}Start Bot {kuning}(default){Style.RESET_ALL}")
    print(f"  6. {merah}Exit\n")
    choice = input("  —— Enter your choice: ")
    return choice

def show_upgrade_menu():
    clear_screen()
    print_banner()
    print(f"{kuning}\n   ----- Upgrade metode -----")
    print(f"  1. Upgrade items with the {hijau}highest profit")
    print(f"  2. Upgrade items at the {hijau}lowest price")
    print(f"  3. Upgrade items with a {hijau}price less than balance")
    print(f"\n  {kuning}[ Please adjust the method that suits you ]\n")
    print(f"  4. Back to {hijau}main menu\n")
    choice = input("  —— Enter your choice (1/2/3/4):")
    return choice

def get_current_daily_cipher():
    try:
        with open('data/cipher.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Tidak ada cipher yang disetel."

def set_daily_cipher():
    clear_screen()
    print_banner()
    
    current_cipher = get_current_daily_cipher()
    print(f"\n{hijau}   Active Menu {kuning}'Auto Complete Daily Cipher' ")
    print(f"{kuning}   Current morse / cipher: {putih}( {current_cipher} ) {kuning}| {hijau}ON")
    print(f"\n   1. Set a new daily cipher?")
    print(f"   2. Back to menu")
    
    choice = input(f"\n   —— Enter your choice: ").strip()
    
    if choice == '1':
        new_cipher = input("   ——  Enter the new daily cipher: ").strip()
        with open('data/cipher.txt', 'w') as file:
            file.write(new_cipher)
        print(Fore.GREEN + Style.BRIGHT + f"\n   —— Daily cipher updated successfully!\n")
    elif choice == '2':
        return
    else:
        print(Fore.RED + Style.BRIGHT + "   —— Invalid choice. Please try again.")
        time.sleep(1)
        set_daily_cipher()

def get_current_combo():
    try:
        with open('data/combo.txt', 'r') as file:
            combo = file.read().strip()
            return combo
    except FileNotFoundError:
        return ""

def get_closest_match(user_input, valid_items):
    matches = difflib.get_close_matches(user_input, valid_items, n=1, cutoff=0.6)
    return matches[0] if matches else user_input

def get_available_upgrades(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['upgradesForBuy']
    else:
        return []

def set_combo():
    clear_screen()
    print_banner()
    current_combo = get_current_combo()
    print(f"\n{hijau}   Active Menu {kuning}'Active Auto Complete Combo'")
    print(kuning + f"   Current Combo")
    if current_combo:
        combo_items = current_combo.split("\n")
        for item in combo_items:
            print(Fore.CYAN + f"- {item}")
    else:
        print(merah + "   No combo set.")

    print(f"\n   1. Set new combo")
    print(f"   2. Back to menu")
    
    choice = input("\n   —— Enter your choice (1/2): ").strip()
    
    if choice == '1':
        print(kuning + f"\n   —— Enter the new combo items {Fore.WHITE}(3 items):")
        combo_items = []
        
        init_data_list = load_tokens('tokens.txt')
        token = get_token(init_data_list[0])  # Assuming you have tokens and using the first one
        upgrades = get_available_upgrades(token)
        valid_items = [upgrade['id'] for upgrade in upgrades]
        
        for i in range(3):
            item = input(f"   —— Enter item {i+1}: ").strip().replace(" ", "_").lower()
            closest_match = get_closest_match(item, valid_items)
            combo_items.append(closest_match)
        with open('data/combo.txt', 'w') as file:
            file.write(f"\n".join(combo_items))
        print(Fore.GREEN + Style.BRIGHT + f"\n   —— Combo updated successfully! ——\n")
    elif choice == '2':
        return
    else:
        print(Fore.RED + Style.BRIGHT + "   —— Invalid choice. Please try again.")
        time.sleep(1)
        set_combo()

def countdown_timer(seconds):
    while seconds:
            menit, detik = divmod(seconds, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih} please wait until {hijau}{jam}:{menit}:{detik} ", flush=True, end="\r")
            seconds -= 1
            time.sleep(1)
    print("                          ", flush=True, end="\r")

def main():
    auto_buy_upgrade = False
    combo_upgrade = False
    daily_cipher_on = False
    tasks_on = False

    cek_task_dict = {}  # Initialize the task check dictionary

    while True:
        choice = show_menu(auto_buy_upgrade, combo_upgrade, daily_cipher_on, tasks_on)
        if choice == '1':
            auto_buy_upgrade = not auto_buy_upgrade
            if auto_buy_upgrade:
                upgrade_method = show_upgrade_menu()
                if upgrade_method not in ['1', '2', '3']:
                    auto_buy_upgrade = False
                    print(merah + "   —— No auto upgrade set. Auto buy upgrade is still OFF")
        elif choice == '2':
            combo_upgrade = not combo_upgrade
            print(f"  —— Combo Upgrade turned {get_status_text(combo_upgrade)}")
            if combo_upgrade:
                set_combo()
                if not get_current_combo():
                    combo_upgrade = False
                    print(merah + "   —— No combo set. Combo Upgrade is still OFF")
        elif choice == '3':
            daily_cipher_on = not daily_cipher_on
            print(f"  —— Daily Cipher turned {get_status_text(daily_cipher_on)}")
            if daily_cipher_on:
                set_daily_cipher()
        elif choice == '4':
            tasks_on = not tasks_on
            print(f"  —— Tasks turned {get_status_text(tasks_on)}")
        elif choice == '5':
            while True:
                init_data_list = load_tokens('tokens.txt')
                
                for init_data in init_data_list:
                    token = get_token(init_data)
                    print_line()
                    if token:
                        response = authenticate(token)
                        if response.status_code == 200:
                            user_data = response.json()
                            countdown_timer(3)
                            username = user_data.get('telegramUser', {}).get('username', 'Please set username first')
                            print_with_timestamp(Fore.YELLOW + Style.BRIGHT + f"login as {Fore.WHITE}{username}")    
                    
                            clicker_data = sync_clicker(token)
                            if 'clickerUser' in clicker_data:
                                user_info = clicker_data['clickerUser']
                                balance_coins = user_info['balanceCoins']
                                earn_passive_per_hour = user_info['earnPassivePerHour']
                                exchange_name = user_info['exchangeId']
                                
                                print_with_timestamp(
                                    f"{hijau}balance: {putih}{format_number(balance_coins)}" +
                                    f"{hijau} | income: {putih}{format_number(earn_passive_per_hour)}/h")
                                print_with_timestamp(f"{hijau}you choose {putih}{exchange_name} exchange"
                                )
                            while True:
                                tap_until_exhausted(token)
                                if not full_boost_tap(token):
                                    break
                            if tasks_on:
                                claim_daily(token)
                                execute_tasks(token, cek_task_dict)
                            if daily_cipher_on:
                                claim_daily_cipher(token)
                            if combo_upgrade:
                                execute_combo(token)
                            if auto_buy_upgrade:
                                auto_upgrade_passive_earn(token, upgrade_method)
                        else:
                            print_with_timestamp(Fore.RED + Style.BRIGHT + f"\r: failed to login token {token[:4]}*********\n", flush=True)
                countdown_timer(3600)
        elif choice == '6':
            print(merah + f"\nhas successfully logged out of the bot...")
            break
        else:
            print_with_timestamp(merah + "Invalid choice. Please try again.")
        time.sleep(1)

if __name__ == '__main__':
    main()
