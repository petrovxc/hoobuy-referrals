# PoC! Only ethical upload :)

Python script for farming referrals on [hoobuy.com](https://hoobuy.com/).

![alt text](https://raw.githubusercontent.com/petrovxc/hoobuy-referrals/refs/heads/main/screenshot.png)

Uploaded (19/06/25)

#### How I made this
Reversed the javascript file for encoding the header, and using a temp mail provider called [minuteinbox](https://www.minuteinbox.com/). Used to be all automatic, by registering to hoobuy and confirming the email address, by filtering the code from minuteinbox.
#

Doesn't work due to hoobuy's changes in source and them adding [recaptcha](https://developers.google.com/recaptcha?)

## Customize Section:

In lines 5-8 in main.py add your proxies and referral:

```py
ammount    = 150  # ammount of total registrations
send_delay = 300  # delay between each send (in seconds)
refferal   = ""   # refferal code tokens should use
proxy      = ""   # rotating proxy
```

If you want to use minuteinbox for verifying other codes, change the url after intercepting the new one. (this one is outdated and they change it every now and then)
```py
    def create_email(self):
        url = f"https://www.minuteinbox.com/index/index?csrf_token={self.crsf}" # this
        
        headers = {"Cookie" : f"PHPSESSID={self.php}", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", "X-Requested-With" : "XMLHttpRequest"}
        
        response = requests.get(url, headers=headers, proxies=self.proxies).text
```

#### Set Up

This is only poc (proof of concept), therefore no instructions on usage will be given

If you have further questions open an issue and I'll gladly help :)
#
