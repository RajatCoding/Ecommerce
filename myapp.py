import requests
import json
dataa = {
      "id":50,
      "first_name" : "Rajat",
      "last_name" : "Dave",
      "password":"payal1997",
      "password2":"payal1997",
      "email" : "rajat128@gmail.com",
      "mobile_no" : 8000000061,
      "address" : "Nanda nagar",
      "city" : "Indore",
      "state" : "Madhya Pradesh",
      "zipcode" : 452011
}
json_data = json.dumps(dataa)
url = "http://127.0.0.1:8000/api/register/"
headers = {
      "content-Type" : "application/json"
}
res = requests.post(url = url, data=json_data, headers=headers )
# print(res)
py_data = res.json()
print(py_data)