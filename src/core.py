import os
import json
import difflib
import sys
import time
import locale
from datetime import datetime
import requests
from colorama import *

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_tokens, get_headers
from src.auth import get_token, authenticate
from src.exceptions import auto_upgrade_passive_earn, claim_daily, execute_tasks, full_boost_tap
from src.exceptions import sync_clicker, tap_until_exhausted, execute_combo, claim_daily_cipher
from src.exceptions import format_number, countdown_timer, print_with_timestamp, print_line
from src.exceptions import mrh,pth,hju,bru,kng,reset,htm

def print_banner():
    banner = r"""
    ██╗████████╗███████╗     ██╗ █████╗ ██╗    ██╗
    ██║╚══██╔══╝██╔════╝     ██║██╔══██╗██║    ██║
    ██║   ██║   ███████╗     ██║███████║██║ █╗ ██║
    ██║   ██║   ╚════██║██   ██║██╔══██║██║███╗██║
    ██║   ██║   ███████║╚█████╔╝██║  ██║╚███╔███╔╝
    ╚═╝   ╚═╝   ╚══════╝ ╚════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  """ 
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(hju + "    Hamster Kombat Auto Bot")
    print(mrh + f"    NOT FOR SALE = Free to use")
    print(mrh + f"    before start please '{hju}git pull{mrh}' to update bot")

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
    print(kng + f"\n  Configurations :")
    print(f"  1. Auto Buy Upgrade           : {get_status_text(auto_buy_upgrade)}")
    print(f"  2. Auto Complete Combo        : {get_status_text(combo_upgrade)}")
    print(f"  3. Auto Complete Daily Cipher : {get_status_text(daily_cipher_on)}")
    print(f"  4. Auto Complete Tasks        : {get_status_text(tasks_on)}")
    print(f"  5. {hju}Start Bot {kng}(default){Style.RESET_ALL}")
    print(f"  6. {mrh}Exit")
    print(f"\n  Note : {pth}without config will execute {hju}taps & boost {pth}only\n")
    choice = input("  —— Enter your choice (1/2/3/4/5/6): ")
    return choice

def show_upgrade_menu():
    clear_screen()
    print_banner()
    print(f"\n{hju}   Active Menu {kng}'Auto Buy Upgrade'")
    print(htm + "   " + "~" * 50)
    print(f"{kng}\n   Upgrade metode:")
    print(f"   1. Upgrade items with the {hju}highest profit")
    print(f"   2. Upgrade items at the {hju}lowest price")
    print(f"   3. Upgrade items with a {hju}price less than balance")
    print(f"   4. Back to {hju}main menu\n")
    choice = input("   —— Enter your choice (1/2/3/4):")
    return choice

def get_current_daily_cipher():
    try:
        with open('data/cipher.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "No ciphers are set."

def set_daily_cipher():
    clear_screen()
    print_banner()
    
    current_cipher = get_current_daily_cipher()
    print(f"\n{hju}   Active Menu {kng}'Auto Complete Daily Cipher' ")
    print(htm + "   " + "~" * 50)
    print(f"{kng}\n   Current cipher:")
    print(pth + f"   —— {current_cipher} | {hju}ON")
    print(kng + f"\n   1. Set a new daily cipher?")
    print(kng + f"   2. Back to {hju}main menu")
    
    choice = input(f"\n   —— Enter your choice (1/2): ").strip()
    
    if choice == '1':
        new_cipher = input("   ——  Enter the new daily cipher (CAPITAL LETTER): ").strip()
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
    print(f"\n{hju}   Active Menu {kng}'Active Auto Complete Combo'")
    print(htm + "   " + "~" * 50)
    print(kng + f"\n   Current Combo:")
    if current_combo:
        combo_items = current_combo.split("\n")
        for item in combo_items:
            print(pth + f"   —— {item}")
    else:
        print(mrh + "   No combo set.")

    print(kng + f"\n   1. Set new combo")
    print(kng + f"   2. Back to {hju}main menu")
    
    choice = input("\n   —— Enter your choice (1/2): ").strip()
    
    if choice == '1':
        print(kng + f"\n   —— Enter the new combo items {Fore.WHITE}(3 items):")
        combo_items = []
        
        init_data_list = load_tokens('tokens.txt')
        token = get_token(init_data_list[0])
        upgrades = get_available_upgrades(token)
        valid_items = [upgrade['id'] for upgrade in upgrades]
        
        for i in range(3):
            item = input(f"   —— Enter item {i+1}: ").strip().replace(" ", "_").lower()
            closest_match = get_closest_match(item, valid_items)
            combo_items.append(closest_match)
        with open('data/combo.txt', 'w') as file:
            file.write(f"\n".join(combo_items))
        
                # Delete all combo_log files in the logs folder
        logs_folder = 'logs'
        for filename in os.listdir(logs_folder):
            if filename.startswith('combo_log') and filename.endswith('.txt'):
                file_path = os.path.join(logs_folder, filename)
                os.remove(file_path)

        print(Fore.GREEN + Style.BRIGHT + f"\n   —— Combo updated successfully! ——\n")
    elif choice == '2':
        return
    else:
        print(Fore.RED + Style.BRIGHT + "   —— Invalid choice. Please try again.")
        time.sleep(1)
        set_combo()

def main():
    auto_buy_upgrade = False
    combo_upgrade = False
    daily_cipher_on = False
    tasks_on = False

    cek_task_dict = {}

    while True:
        choice = show_menu(auto_buy_upgrade, combo_upgrade, daily_cipher_on, tasks_on)
        if choice == '1':
            auto_buy_upgrade = not auto_buy_upgrade
            if auto_buy_upgrade:
                upgrade_method = show_upgrade_menu()
                if upgrade_method not in ['1', '2', '3']:
                    auto_buy_upgrade = False
                    print(mrh + "   —— No auto upgrade set. Auto buy upgrade is still OFF")
        elif choice == '2':
            combo_upgrade = not combo_upgrade
            print(f"  —— Combo Upgrade turned {get_status_text(combo_upgrade)}")
            if combo_upgrade:
                set_combo()
                if not get_current_combo():
                    combo_upgrade = False
                    print(mrh + "   —— No combo set. Combo Upgrade is still OFF")
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
                    if token:
                        response = authenticate(token)
                        if response.status_code == 200:
                            user_data = response.json()
                            username = user_data.get('telegramUser', {}).get('username', 'Please set username first')
                            print_with_timestamp(Fore.YELLOW + Style.BRIGHT + f"Login as {Fore.WHITE}{username}")    
                    
                            clicker_data = sync_clicker(token)
                            if 'clickerUser' in clicker_data:
                                user_info = clicker_data['clickerUser']
                                balance_coins = user_info['balanceCoins']
                                earn_passive_per_hour = user_info['earnPassivePerHour']
                                exchange_name = user_info['exchangeId']
                                
                                print_with_timestamp(
                                    f"{hju}Balance: {pth}{format_number(balance_coins)}" +
                                    f"{hju} | Income: {pth}{format_number(earn_passive_per_hour)}/h")
                                print_with_timestamp(f"{hju}You choose {pth}{exchange_name} exchange"
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
                                execute_combo(token, username)
                            if auto_buy_upgrade:
                                auto_upgrade_passive_earn(token, upgrade_method)
                            print_line()
                            countdown_timer(3)
                        else:
                            print_with_timestamp(Fore.RED + Style.BRIGHT + f"\r: Failed to login token {token[:4]}*********\n", flush=True)
                countdown_timer(3600)
        elif choice == '6':
            print(mrh + f"\nHas successfully logged out of the bot...")
            break
        else:
            print_with_timestamp(mrh + "Invalid choice. Please try again.")
        time.sleep(1)

if __name__ == '__main__':
    main()
