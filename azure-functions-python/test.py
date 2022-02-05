import requests
import urllib.parse
import json

img = "https://longriverstorage.blob.core.windows.net/images/generic/2021/12/10D796C9.jpg?sv=2020-10-02&st=2022-02-05T04%3A57%3A08Z&se=2023-02-06T04%3A57%3A00Z&sr=b&sp=r&sig=YMwv%2B1hJs1VyulNn3onaDG%2B0RLkV6i8SjOUhsj9z0oM%3D"
code = "qAkViovem7ELUC6P2KwfVIOZSza0aBH/qNwdYlTuMqQrxmYDBvUqDQ=="
service = "https://alphataibai-func-python.azurewebsites.net/api/imgclf"
service = "http://localhost:7071/api/imgclf"
params = {'code':code, 'img': img, 'top':  20}
param_encode_str = urllib.parse.urlencode(params)
resp = requests.get(service + "?" + param_encode_str)
print(json.loads(resp.text))