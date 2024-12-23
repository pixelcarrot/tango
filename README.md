# Tango

## Installation

```sh
curl -o tango.py https://raw.githubusercontent.com/pixelcarrot/tango/refs/heads/main/tango.py | curl -O https://raw.githubusercontent.com/pixelcarrot/tango/refs/heads/main/requirements.txt | pip install -r requirements.txt
```

`nano tango.py`

```
BOT_TOKEN = "" # Using BotFather to create one

ALLOWED_USER_IDS = [] # Using @userinfobot to get Id

# transmission-remote -n 'yourusername:yourpassword' -l
TRANSMISSION_USER = ""
TRANSMISSION_PASS = ""
```

## Create Bot Service

Create a service file:

```sh
sudo nano /etc/systemd/system/tango_bot.service
```

Add the following content:

```sh
[Unit]
Description=Tango
After=network.target

[Service]
ExecStart=/usr/bin/python /home/justin/script/tango.py
Restart=always
User=justin
WorkingDirectory=/home/justin/script

[Install]
WantedBy=multi-user.target
```

Tip: To find ExecStart `type -a python`

Start and enable the service:

```sh
sudo systemctl start telegram_bot.service
sudo systemctl enable telegram_bot.service
```
