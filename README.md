# check_innovaphone.py
*Icinga and Nagios check plugin for innovaphone PBX devices*

#### Available checks:
- Temprature of the PBX (°C)
- Sync state of the PBX (ISDN Interaface)
- If reset required? (true / false)
- Remaining time for software rental licenses in days, hours, minutes, seconds

usage for help: `./check_innovaphone.py`

usage: `./check_innovaphone.py -H <ip or hostname> -l <username> -p <password> --command <check> -w <warning threshold> -c <critical threshold>`

*available options for --command: "temp", "sync", "reset-required", "srlicense"*