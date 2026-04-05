
import requests

print("hello")
for i in range(999999):
    response = requests.get(f"http://localhost:8000/getPincode?pincode={i}")
    print(response)
