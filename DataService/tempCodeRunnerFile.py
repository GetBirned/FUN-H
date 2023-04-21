x = requests.post(url, json=document)
print("response text", x.text)
print("response code", x.status_code)