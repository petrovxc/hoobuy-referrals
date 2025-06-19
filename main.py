import requests, uuid, hashlib, time, os, pystyle, json, re

# setup section

ammount    = 150  # ammount of total registrations
send_delay = 300  # delay between each send (in seconds)
refferal   = ""   # refferal code tokens should use
proxy      = ""   # rotating proxy

# ---

class Register:
    
    def __init__(self):
        self.session = requests.Session()
        self.proxies = {"http" : f"http://{proxy}/", "https" : f"http://{proxy}/"}
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", "X-Version" : "hoobuy-production-web-1.0"}
        request      = requests.get("https://www.minuteinbox.com/", proxies=self.proxies)
        self.php     = request.cookies.get_dict()['PHPSESSID']
        self.crsf    = re.search(r'const CSRF="([^"]+)"', request.text).group(1)
        
        self.create_email()
        self.setup_acc()
        
    def create_email(self):
        url = f"https://www.minuteinbox.com/index/index?csrf_token={self.crsf}"
        
        headers = {"Cookie" : f"PHPSESSID={self.php}", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", "X-Requested-With" : "XMLHttpRequest"}
        
        response = requests.get(url, headers=headers, proxies=self.proxies).text
    
        self.email = response.split('{"email":"')[1].split('"}')[0]
        
        print(f" [+] Progress | acquired email: {self.email}")
    
    def check_code(self):
        url = f"https://www.minuteinbox.com/index/refresh"
        
        headers = {"Cookie" : f"PHPSESSID={self.php}; MI={self.email.split('@')[0]}%40{self.email.split('@')[1]}", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", "X-Requested-With" : "XMLHttpRequest"}
        
        time.sleep(5)
    
        for i in range(10):
            response = requests.get(url, headers=headers, proxies=self.proxies).text

            try:
                predmet = json.loads(response.split(f'[')[1].split(',"od"')[0] + '}')
                code = predmet['predmet'][:6]
                return code
            except:
                time.sleep(1)
                continue
        
        return "000000"
        
    def setup_acc(self):
        url = "https://api.hoobuy.com/hoobuy_account/pub/register-email-check"
        
        body = {"email" : self.email, "password" : self.email}
        
        x_nonce     = str(uuid.uuid4())
        x_signature = hashlib.md5(f"{x_nonce}980683EF-46C6-47D5-80C1-7B2CB6B2D0BF".encode()).hexdigest()
        
        self.headers.update({"X-Nonce" : x_nonce, "X-Signature" : x_signature})

        response = self.session.post(url, headers=self.headers, json=body, proxies=self.proxies)

        if "OK" in response.text:
            print(f" [+] Progress | account prepared for verification")
        else:
            print(f" [-] Progress | error with account preparation")
            return False
        
        self.send_code()
    
    def send_code(self):
        url = "https://api.hoobuy.com/hoobuy_account/pub/email/verifycode"
        
        body = {"email" : self.email, "type"  : 1}
        
        x_nonce     = str(uuid.uuid4())
        x_signature = hashlib.md5(f"{x_nonce}980683EF-46C6-47D5-80C1-7B2CB6B2D0BF".encode()).hexdigest()
        
        self.headers.update({"X-Nonce" : x_nonce, "X-Signature" : x_signature})

        response = self.session.post(url, headers=self.headers, json=body, proxies=self.proxies)

        if "OK" in response.text:
            print(f" [+] Progress | hoobuy email sent")
        else:
            print(f" [-] Progress | error sending email")
            return False

        self.register_acc()
    
    def register_acc(self):
        url = "https://api.hoobuy.com/hoobuy_account/pub/register"
        
        body = {"email" : self.email, "password" : self.email, "verifyCode" : self.check_code(), "referralCode" : refferal, "utm_source" : "", "utm_medium" : "", "utm_campaign" : ""}
        
        x_nonce     = str(uuid.uuid4())
        x_signature = hashlib.md5(f"{x_nonce}980683EF-46C6-47D5-80C1-7B2CB6B2D0BF".encode()).hexdigest()
        
        self.headers.update({"X-Nonce" : x_nonce, "X-Signature" : x_signature})

        response = self.session.post(url, headers=self.headers, json=body, proxies=self.proxies)

        if "OK" in response.text:
            print(f" [+] Progress | created token: {response.json()['data']['token']}")
            open("accounts.txt", "a").write(f"{response.json()['data']['email']}|{response.json()['data']['userId']}|{response.json()['data']['token']}\n")
            return True
        else:
            print(f" [-] Progress | error creating token")
            return False

def main():
    for i in range(ammount):
        os.system("cls" if os.name == "nt" else "clear")
        print(pystyle.Center.XCenter(f"\n/petrovxc | refferal: {refferal} | ammount: {ammount} | delay: {send_delay}s | finished: {i}\n\n"))
        
        if Register():
            time.sleep(send_delay)

main()
