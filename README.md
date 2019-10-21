# check_innovaphone.py
*Icinga and Nagios check plugin for innovaphone PBX devices*

#### Available checks:
- Temprature of the PBX with Perfdata (°C)

    `OK - Temprature is 41.2°C | Temprature=41.2;45;50`
- Sync state of the PBX (ISDN Interaface)

    `OK - Sync Interface = PRI1-L1`
- If reset required? (true / false)

    `OK - No Reset Required`
- Remaining time for software rental licenses in days, hours, minutes, seconds

    `OK - Remaining Time: 95 days, 4 hours, 51 minutes, 51 seconds`


![Icinga2 check output:][pic-output]

![pic-perfdata]


usage for help:

    ./check_innovaphone.py

usage: 

    ./check_innovaphone.py -H <ip or hostname> -l <username> -p <password> --command <check> -w <warning threshold> -c <critical threshold>

*available options for --command: "temp", "sync", "reset-required", "srlicense"*

[pic-output]: https://github.com/hashfunktion/check_innovaphone/output.png "Icinga2 check output"
[pic-perfdata]: https://github.com/hashfunktion/check_innovaphone/tempwithperfdata.png "Icinga2 check output with perfdata"