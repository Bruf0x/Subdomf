# Subdomf
Subdomain finder using crt and certspotter APIs.

This script is based on crtndstry by [NahamSec](https://www.youtube.com/@NahamSec).

```bash
           _         _                  __ 
          | |       | |                / _|
 ___ _   _| |__   __| | ___  _ __ ___ | |_ 
/ __| | | | '_ \ / _` |/ _ \| '_ ` _ \|  _|
\__ \ |_| | |_) | (_| | (_) | | | | | | |  
|___/\__,_|_.__/ \__,_|\___/|_| |_| |_|_| by. Bruf0x
```

This script uses:

- crt.sh
- certspotter
- others in the furure...
  
With these APIs, it finds subdomains by passively searching Certificate Transparency logs.

```bash
# Default patterns
patterns=("api" "corp" "dev" "uat" "test" "stag" "sandbox" "prod" "hom")
```

You can add more patterns with the -p option:
```bash
└─# ./subdomf.sh -p secret,cam,project nasa.gov
```

The output shows a list of subdomains and creates a file `domain.txt`:
```bash
ted.mecum@mail.nasa.gov
tpetkovs@mail.nasa.gov
uat.nasa.gov
userdocuments.test.nasa.gov
userdocuments.uat.nasa.gov
vpn.test.nasa.gov
vpn.uat.nasa.gov
wapr.uat.nasa.gov
water.uat.nasa.gov
wbm.uat.nasa.gov
[+] Number of subdomains found: 197
```
# Disclaimer
`This script is for educational purposes only. I am not responsible for any misuse of this script.`
