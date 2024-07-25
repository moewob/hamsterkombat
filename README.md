# Hamster Kombat Auto Farming Bot 
This is a bot that can help you to run hamsterkombat telegram bot which has quite complete features with auto upgrade (3 methods), auto complete combo, auto complete daily cipher, auto complete Mini Game & auto complete tasks.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [TWITTER](https://x.com/itsjaw_real)

### Buy me Coffee ☕ 
```
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

# Latest update // 25-07-2024
These changes enhance the script by adding a `Maximum Price Filter Include on Upgrade & Combo` for upgrades `FULL Auto Complete Daily Combo`, `FULL Auto Complete Daily Morse`, `FULL Auto Complete Minigame`, `Fake userAgent` , refining the upgrade process to avoid unnecessary error messages, and improving error handling in the buy_upgrade function. These updates ensure a smoother and more efficient upgrading experience in the Hamster Kombat Clicker game.

Add configuration setting on `config.json` 

**bool** | tapDelay : `true` or `false` 

**bool** | ClaimKeysDelay : `true` or `false` 

**bool** | delayUpgrade : `true` or `false` 
  ```bash
{
    "min_tap": 1038,
    "max_tap": 1800,
    "DelayPerAccount": 5,
    "tapDelay": true,
    "ClaimKeysDelay": true,
    "delayUpgrade": false,
    "max_price": 5000000,
    "loop": 3800
}
  ```
## Features
- Auto Buy Upgrade (with 3 method options) - `ON/OFF` enhanced on `25-07-2024`
- Auto Complete Daily Combo - `ON/OFF` enhanced on `25-07-2024`
- Auto Complete Daily Morse - `ON/OFF` enhanced on `16-07-2024`
- Auto Complete Mini Game - `ON/OFF` `NEW`
- Auto Complete Tasks - `ON/OFF`
- Auto Energy Boost (6x / day) - `Auto ON`
- Random UserAgent - `Auto ON`
- By default without config will execute `Taps, Boost & Daily Streak`

##  Auto Upgrade metode
  1. Upgrade items with the **highest profit**
  2. Upgrade items at the **lowest price**
  3. Upgrade items with a **price less than balance**

## Prerequisites
Before installing and running this project, make sure you have the following prerequisites:
- Python 3 version 1.0.1+ = Python 3.10+
- Other required dependencies

## Installation
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/jawikas/hamsterkombat.git
    ```
2. Go to the project directory:
    ```bash
    cd hamsterkombat
    ```
3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
before starting the bot you must have your own initdata / queryid telegram! why query id? with query_id it is definitely more profitable because you don't have to bother changing your init data every time.

1. Use PC/Laptop or Use USB Debugging Phone
2. open the `hamster kombat bot`
3. Inspect Element `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`Hamster Kombat`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A1323733375%2C%22first_name%22%3A%22xxxx%22%2C%22last_name%22%3A%22%E7%9A%BF%20xxxxxx%22%2C%22username%22%3A%22xxxxx%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=xxxxx&hash=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
9. add it to `tokens.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A1323733375%2C%22first_name%22%3A%22xxxx%22%2C%22last_name%22%3A%22%E7%9A%BF%20xxxxxx%22%2C%22username%22%3A%22xxxxx%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=xxxxx&hash=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A1323733375%2C%22first_name%22%3A%22xxxx%22%2C%22last_name%22%3A%22%E7%9A%BF%20xxxxxx%22%2C%22username%22%3A%22xxxxx%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=xxxxx&hash=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
## RUN THE BOT
after that run the kombat hamster bot by writing the command

```bash
python main.py
```

## Screenshoot
![image](https://github.com/jawikas/hamsterkombat/assets/63976518/de33ad9f-f5ea-451e-a9ac-bce8d525e28f)

## License
This project is licensed under the `NONE` License.

## Contact
If you have any questions or suggestions, please feel free to contact us at [ https://t.me/itsjaw_real ].

## Thanks to

Template based by - https://github.com/akasakaid

Full Source code by YOU 💘 (users of this scripts)


