import http.client

api_key_predictleads = "vseywxkoyz-2jw62hx9z"
api_token_predictleads = "Fn5NqhUyKWkxmyXc9ztQ"

conn = http.client.HTTPSConnection("predictleads.com")

headers = {"X-Api-Key": api_key_predictleads, "X-Api-Token": api_token_predictleads}

domain = "motionsociety.com"  # Replace with the target domain
endpoint = f"/api/v3/companies/{domain}"

# Send the request
conn.request("GET", endpoint, headers=headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Print the response
print(data.decode("utf-8"))
