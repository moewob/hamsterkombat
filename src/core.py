import os
import time
import locale
from colorama import *
import shutil
from src.utils import load_tokens
from src.auth import get_token, authenticate
from src.exceptions import upgrade_passive, claim_daily, execute, boost, clicker_config
from src.exceptions import _sync, exhausted, execute_combo, claim_cipher
from src.exceptions import _number, countdown_timer, log, log_line
from src.__init__ import mrh, pth, hju, kng, htm, reset, read_config

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
init(autoreset=True)
def _banner():
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

def get_status(status):
    if status:
        return Fore.GREEN + "ON" + Style.RESET_ALL
    else:
        return Fore.RED + "OFF" + Style.RESET_ALL

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(auto_upgrade, combo_upgrade, daily_cipher_on, tasks_on):
    _clear()
    _banner()
    print(kng + f"\n  Configurations :{reset}")
    print(f"  1. Auto Buy Upgrade           : {get_status(auto_upgrade)}")
    print(f"  2. Auto Complete Combo        : {get_status(combo_upgrade)}")
    print(f"  3. Auto Complete Daily Cipher : {get_status(daily_cipher_on)}")
    print(f"  4. Auto Complete Tasks        : {get_status(tasks_on)}")
    print(f"  5. {hju}Start Bot {kng}(default){reset}")
    print(f"  6. {mrh}Exit")
    print(f"\n  {kng}[INFO] {pth}By default will do {hju}taps, boost & streak\n")
    choice = input("  —— Enter your choice (1/2/3/4/5/6): ")
    log_line()
    return choice

def show_upgrade_menu():
    _clear()
    _banner()
    config = read_config()
    max_price = config.get('max_price', 10000000)
    print(f"\n{hju}   Active Menu {kng}'Auto Buy Upgrade'")
    print(htm + "   " + "~" * 50)
    print(f"{kng}\n   Upgrade metode:{reset}")
    print(f"   1. Upgrade items with the {hju}highest profit")
    print(f"   2. Upgrade items at the {hju}lowest price")
    print(f"   3. Upgrade items with a {hju}price less than balance")
    print(f"   4. Back to {hju}main menu\n")
    print(f"\n   {kng}[INFO]{hju} Current Max Price : {pth}{_number(max_price)}\n")
    choice = input("   —— Enter your choice (1/2/3/4):")
    return choice

def clear_logs_folder():
    log_folder_path = os.path.join(os.path.dirname(__file__), '../logs')
    if os.path.exists(log_folder_path):
        shutil.rmtree(log_folder_path)
        os.makedirs(log_folder_path)

def main():
    auto_upgrade = False
    combo_upgrade = False
    daily_cipher_on = False
    tasks_on = False

    cek_task_dict = {}
    config = read_config()
    countPerAccount = config.get('DelayPerAccount', 3)
    loop = config.get('loop', 3600)
    while True:
        choice = show_menu(auto_upgrade, combo_upgrade, daily_cipher_on, tasks_on)
        if choice == '1':
            auto_upgrade = not auto_upgrade
            if auto_upgrade:
                _method = show_upgrade_menu()
                if _method not in ['1', '2', '3']:
                    auto_upgrade = False
                    print(f"   —— No auto upgrade set. Auto buy upgrade is {mrh}still OFF")
        elif choice == '2':
            clear_logs_folder()
            combo_upgrade = not combo_upgrade
            print(f"  —— Combo Upgrade turned {get_status(combo_upgrade)}")
        elif choice == '3':
            daily_cipher_on = not daily_cipher_on
            print(f"  —— Daily Cipher turned {get_status(daily_cipher_on)}")
        elif choice == '4':
            tasks_on = not tasks_on
            print(f"  —— Tasks turned {get_status(tasks_on)}")
        elif choice == '5':
            while True:
                init_data_list = load_tokens('tokens.txt')
                
                for init_data in init_data_list:
                    token = get_token(init_data)
                    if token:
                        res = authenticate(token)
                        if res.status_code == 200:
                            user_data = res.json()
                            username = user_data.get('telegramUser', {}).get('username', 'Please set username first')
                            log(kng + f"Login as {pth}{username}")    
                            clicker_config(token)
                            clicker_data = _sync(token)
                            if 'clickerUser' in clicker_data:
                                user_info = clicker_data['clickerUser']
                                balance_coins = user_info['balanceCoins']
                                earn_passive_per_hour = user_info['earnPassivePerHour']
                                exchange_name = user_info['exchangeId']
                                
                                log(
                                    f"{hju}Balance: {pth}{_number(balance_coins)}" +
                                    f"{hju} | Income: {pth}{_number(earn_passive_per_hour)}/h")
                                log(f"{hju}CEO of {pth}{exchange_name} exchange"
                                )
                            claim_daily(token)
                            while True:
                                exhausted(token)
                                if not boost(token):
                                    break
                            if tasks_on:
                                execute(token, cek_task_dict)
                            if daily_cipher_on:
                                claim_cipher(token)
                            if combo_upgrade:
                                execute_combo(token, username)
                            if auto_upgrade:
                                upgrade_passive(token, _method)  
                        log_line()
                        countdown_timer(countPerAccount)
                    else:
                        log(mrh + f"\r: Failed to login token {token[:4]}*********\n", flush=True)
                countdown_timer(loop)
        elif choice == '6':
            log(mrh + f"Successfully logged out of the bot\n")
            break
        else:
            log(mrh + "Invalid choice. Please try again.")
        time.sleep(1)

if __name__ == '__main__':
    main()
