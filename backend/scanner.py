import subprocess
import requests
import time

while True:
    l = str(subprocess.check_output(['nmap', '-sn', '192.168.1.0/24']))
        
    print(l)

    res = requests.post(
        'https://gongy-93-fastapi.modal.run/localpost',
        json={'nmapResult': l}
    )

    print(res.reason)
    print(res.status_code)

    time.sleep(3 * 60)