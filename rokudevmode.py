import requests
import time
tvip="10.0.0.21"
print("Entering key combo")
requests.post("http://" + tvip + ":8060/keypress/Home")
time.sleep(0.5)
requests.post("http://" + tvip + ":8060/keypress/Home")
time.sleep(0.5)
requests.post("http://" + tvip + ":8060/keypress/Home")
time.sleep(0.5)
requests.post("http://" + tvip + ":8060/keypress/Up")
time.sleep(0.5)
requests.post("http://" + tvip + ":8060/keypress/Up")
time.sleep(0.5)
for _ in range(2):
    requests.post("http://" + tvip + ":8060/keypress/Right")
    time.sleep(0.5)
    requests.post("http://" + tvip + ":8060/keypress/Left")
    time.sleep(0.5)
time.sleep(1)
requests.post("http://" + tvip + ":8060/keypress/Right")
print("You should see a popup on your roku device!")

