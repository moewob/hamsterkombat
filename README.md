# Hamster Kombat Auto Farming Bot 
This is a bot that can help you to run hamsterkombat telegram bot which has quite complete features with auto upgrade (3 methods), auto complete combo, auto complete daily cipher, auto complete Mini Game & auto complete tasks.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [TWITTER](https://x.com/itsjaw_real)

### Buy me Coffee ☕ 
```
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

# Latest update // 6-08-2024
in this update we got a lot of feedback from you guys and some of them have been applied in this update. which there may be many updates to come.

1. User agent is not random but static on each account
2. Split tap tap is no longer default when starting the bot 3.
3. addition of redeem promotion codes for bicycle games. 

add your promo code on `promo.txt` example :
  ```bash
BIKE-0H4-1BP0-0BH7-52H
BIKE-2GR-36HC-0DJF-67F
BIKE-1HG-3QQ0-0NGZ-BVV
  ```

`LOOKING FOR FREE 10 PROMO CODE?` just DM [t.me/itsjaw_real](https://t.me/itsjaw_real)

Add configuration setting on `config.json` 

**bool** | TAP_DELAY : `true` or `false` 

**bool** | CLAIM_KEY_DELAY : `true` or `false` 

**bool** | DELAY_UPGRADE : `true` or `false` 
  ```bash
{
    "MINIMUM_TAP": 438,
    "MAXIMUM_TAP": 1200,

    "TAP_DELAY": true,
    "MIN_TAP_DELAY": 5,
    "MAX_TAP_DELAY": 7,

    "CLAIM_KEY_DELAY": true,
    "MIN_CLAIM_KEY_DELAY": 7,
    "MAX_CLAIM_KEY_DELAY": 11,

    "DELAY_UPGRADE": true,
    "MIN_DELAY_UPGRADE": 3,
    "MAX_DELAY_UPGRADE": 5,

    "DELAY_EACH_ACCOUNT": 5,
    "MAXIMUM_PRICE": 5000000,
    "LOOP_COUNTDOWN": 3800
}
  ```
## Features
- Auto Buy Upgrade (with 3 method options) - `ON/OFF`
- Auto Taps Taps - `ON/OFF`
- Auto Complete Daily Combo - `ON/OFF`
- Auto Complete Daily Morse - `ON/OFF`
- Auto Complete Tasks - `ON/OFF`
- Auto Complete Mini Game - `ON/OFF` `NEW`
- Auto Redeem Promo codes - `ON/OFF` `NEW`
- Auto Energy Boost (6x / day) - `Auto ON`
- Static UserAgent - `Auto ON` `NEW`
- By default without config will execute `Boost & Daily Streak`

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


