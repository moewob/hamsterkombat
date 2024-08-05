import sys
import time
import locale
import requests
from colorama import *
from src.utils import load_tokens
from src.auth import get_token, authenticate
from src.exceptions import upgrade_passive, claim_daily, execute, boost, clicker_config
from src.exceptions import _sync, exhausted, execute_combo, claim_cipher, claim_key
from src.promo import redeem_promo

from src.__init__ import (
    mrh, pth, hju, kng, htm, bru,  reset, 
    read_config, _number, countdown_timer, log, 
    log_line, _banner, _clear
    )

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
init(autoreset=True)
config = read_config()

def get_status(status):
    return Fore.GREEN + "ON" + Style.RESET_ALL if status else Fore.RED + "OFF" + Style.RESET_ALL

def show_menu(auto_upgrade, taps_on, combo_upgrade, daily_cipher_on, claim_key_on, tasks_on, promo_on):
    _clear()
    _banner()
    menu = f"""
{kng} Configurations :{reset}
{kng}  1.{reset} Auto Buy Upgrade           : {get_status(auto_upgrade)}
{kng}  2.{reset} Auto Taps Taps             : {get_status(taps_on)}
{kng}  3.{reset} Auto Complete Combo        : {get_status(combo_upgrade)}
{kng}  4.{reset} Auto Complete Cipher       : {get_status(daily_cipher_on)}
{kng}  5.{reset} Auto Complete Mini Game    : {get_status(claim_key_on)}
{kng}  6.{reset} Auto Complete Tasks        : {get_status(tasks_on)}
{kng}  7.{reset} Auto Redeem Promo          : {get_status(promo_on)}
{mrh}\n  [INFO]{reset} {kng}add configuration {bru}and {hju}start the bot\n{reset}
{kng}  0.{reset} {hju}Start Bot {kng}(default){reset}
{kng}  99.{reset} {mrh}Reset{reset}

    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4/5/6): ")
    log_line()
    return choice

def show_upgrade_menu():
    _clear()
    _banner()
    config = read_config()
    MAXIMUM_PRICE = config.get('MAXIMUM_PRICE', 1000000)
    menu = f"""
{hju} Active Menu {kng}'Auto Buy Upgrade'{reset}
{htm} {'~' * 50}{reset}
{kng} Upgrade Method:{reset}
{kng} 1. {pth}highest profit {hju}[ enchanced ]{reset}
{kng} 2. {pth}lowest price{reset}
{kng} 3. {pth}price less than balance{reset}
{kng} 4. {pth}upgrade by payback{reset}
{kng} 5. {pth}back to {bru}main menu{reset}

{kng} [INFO]{reset} you set Max Price to : {pth}{_number(MAXIMUM_PRICE)}{reset}
    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4): ")
    return choice

def load_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    auto_upgrade = False
    taps_on = False
    combo_upgrade = False
    daily_cipher_on = False
    claim_key_on = False
    tasks_on = False
    promo_on = False

    cek_task_dict = {}
    DELAY_EACH_ACCOUNT = config.get('DELAY_EACH_ACCOUNT', 0)
    LOOP_COUNTDOWN = config.get('LOOP_COUNTDOWN', 0)

    while True:
        try:
            choice = show_menu(auto_upgrade, taps_on, combo_upgrade, daily_cipher_on, claim_key_on, tasks_on, promo_on)
            if choice == '1':
                auto_upgrade = not auto_upgrade
                if auto_upgrade:
                    _method = show_upgrade_menu()
                    if _method not in ['1', '2', '3', '4']:
                        auto_upgrade = False
            elif choice == '2':
                taps_on = not taps_on
            elif choice == '3':
                combo_upgrade = not combo_upgrade
            elif choice == '4':
                daily_cipher_on = not daily_cipher_on
            elif choice == '5':
                claim_key_on = not claim_key_on
            elif choice == '6':
                tasks_on = not tasks_on
            elif choice == '7':
                promo_on = not promo_on
            elif choice == '0':
                while True:
                    init_data_list = load_tokens('tokens.txt')
                    
                    for idx, init_data in enumerate(init_data_list):
                        account = f"account_{idx + 1}"
                        token = get_token(init_data, account)
                        if token:
                            try:
                                res = authenticate(token, account)
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
                                        
                                        log(hju + f"Balance: {pth}{_number(balance_coins)}")
                                        log(hju + f"Income: {pth}{_number(earn_passive_per_hour)}/h")
                                        log(hju + f"CEO of {pth}{exchange_name} {hju}exchange")
                                    claim_daily(token)
                                    if taps_on:
                                        while True:
                                            exhausted(token)
                                            if not boost(token):
                                                break
                                    if promo_on:
                                        redeem_promo(token)
                                    if tasks_on:
                                        execute(token, cek_task_dict)
                                    if daily_cipher_on:
                                        claim_cipher(token)
                                    if claim_key_on:    
                                        claim_key(token)
                                    if combo_upgrade:
                                        execute_combo(token)
                                    if auto_upgrade:
                                        upgrade_passive(token, _method)  
                                log_line()
                                countdown_timer(DELAY_EACH_ACCOUNT)
                            except requests.RequestException as e:
                                log(mrh + f"Request exception for token {pth}{token[:4]}****: {str(e)}")
                        else:
                            log(mrh + f"Failed to login token {pth}{token[:4]}*********\n", flush=True)
                    countdown_timer(LOOP_COUNTDOWN)
            elif choice == '99':
                break
            else:
                log("Invalid choice. Please try again.")
            time.sleep(1)
        except Exception as e:
            log(mrh + f"An error occurred in the main loop: {kng}{str(e)}")
            countdown_timer(10)

if __name__ == '__main__':
    main()