import requests
import os

password = os.environ["PASSWORD"]

domain_list = requests.get("http://localhost:8000/uptime/domains/").json()
for domain in domain_list:
    domain = requests.get(domain["url"]).json()
    domain["domain"] = domain["domain"].replace(".be", ".fr")
    print(requests.put(domain["url"], auth=("mdk", password), json=domain))
