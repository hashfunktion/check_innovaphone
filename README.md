# check_innovaphone.py
*Icinga and Nagios check plugin for innovaphone PBX devices*

This Icinga and Nagios check plugin is for innovaphone PBX devices to check some parameter like temprature and other helpfull thinks.

In the future i will ad some further parameters, if I think it's a good idea. Wishes are welcome.

*Tested and developed wit Icinga 2*

## Requirements

This check command depends on the following python modules:
- argparse
- urllib.request
- base64
- ssl
- math
- xml.etree.ElementTree

## Usage
*Befor using, change the "xmlpath" in the check plugin to a writable path for you..*

    usage: check_innovaphone.py [-h] [-H HOST] [-l USERNAME] [-p PASSWORD]
                                [--command COMMAND] [-w WARN] [-c CRIT]
    
    optional arguments:
      -h, --help
        how this help message and exit

      -H HOST, --hostname HOST
        enter IP-Adress or Hostname of the innovaphone PBX

      -l USERNAME, --loginname USERNAME
        define username from innovaphone PBX (default: admin)

      -p PASSWORD, --password PASSWORD
        define password from innovaphone PBX

      --command COMMAND
        define the check_command that should be use (available
        options: "temp", "sync", "reset-required", "srlicense"

      -w WARN, --warning WARN
        define the warning threshold for: temp=XX(°C),
        srlicense=XXXXXXX(seconds) only XX without unit

      -c CRIT, --critical CRIT
        define the critical threshold for: temp=XX(°C),
        srlicense=XXXXXXX(seconds) only XX without unit
    
    Sample:
    ./check_innovaphone.py -H <ip or hostname> -l <username> -p <password> --command <check> -w <warning threshold> -c <critical threshold>

    ./check_innovaphone.py -H "pbx.domain.net" -l "monitoring-user" -p "top-secret" --command "temp" -w "50" -c "55"


## Available checks:
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

[pic-output]: https://github.com/hashfunktion/check_innovaphone/blob/master/output.png?raw=true "Icinga2 check output"
[pic-perfdata]: https://github.com/hashfunktion/check_innovaphone/blob/master/tempwithperfdata.png?raw=true "Icinga2 check output with perfdata"