# Coin bot - Automatically buying coin using Upbit

## Tested environment
- ubuntu 20.04 x86_64 instance in AWS EC2 
- python 3.8.10

## Requirements
- pyupbit

## Preparation
- Clone this repository in your workspace
``` bash
git clone git@github.com:SunandBean/coin_buying_bot.git
```
- Change directory to the cloned repository and install python packages in `requirements.txt` by following command
``` bash
cd coin_buying_bot && pip install -r requirements.txt
```

## How to use
### Set configuration
- Fill out the configuration file based on your information
``` json
{
    "access_key":"your_access_key_from_upbit_openapi",
    "secret_key":"your_secret_key_from_upbit_openapi",
    "send_mail_address":"your_google_mail",
    "send_mail_password":"your_app_password_of_google_mail",
    "receiver":"mail_address_where_you_want_to_send"
}
```

### Run script only once
- Run `upbit_buying_bot.py` by following command in the cloned repository
    ``` bash
    python3 upbit_buying_bot.py
    ```
- Or run `run_bot.sh` by following command in the cloned repository
    ``` bash
    ./run_bot.sh
    ```
    - if it's not working, then please run the following command and try one more time to run the script
        ``` bash
        chmod +x run_bot.sh
        ```

### Run script periodically
- Enter edit mode of crontab by following command 
    ``` bash
    crontab -e
    ```
- Set your periodical information in crontab
    ``` bash
    # m h  dom mon dow   command
    0 9 * * * /home/ubuntu/upbit_buying_bot/run_bot.sh
    ```