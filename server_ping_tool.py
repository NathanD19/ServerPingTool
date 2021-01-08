import platform
import subprocess
import boto3
import time
import datetime
import sys

import servers
import secrets

# Last SMS Sent DATETIME (set 2 hours back from start time) - Avoid Spam
sms_sent_time = datetime.datetime.now() - datetime.timedelta(hours=2)

def ping(server):

    global sms_sent_time

    # Create and Send the ping
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    # Build the command
    command = ['ping', param, '1', server['ip']]
    res = subprocess.call(command) == 0

    if not res and (datetime.datetime.now() - sms_sent_time).total_seconds() > secrets.SMS_COOLDOWN:
        # Create AWS Client
        client = boto3.client(
            "sns",
            aws_access_key_id=secrets.AWS_KEY_ID,
            aws_secret_access_key=secrets.AWS_SECRET_KEY,
            region_name=secrets.AWS_REGION
        )

        # Retrieve phone numbers, split by ","
        ph_numbers = secrets.PHONE_NUMBERS.split(",")
        for number in ph_numbers:
            client.publish(
                PhoneNumber=number,
                Message=server['name'] + " DOWN - CHECK SERVER IMMEDIATELY!"
            )

        sms_sent_time = datetime.datetime.now()



# Server List
server_list = servers.list

while True:
    sys.stdout.write('Checking status...')
    sys.stdout.flush()
    sys.stdout.write('\r')
    for server in server_list:
        ping(server)
    for i in range(0, secrets.PING_INTERVAL):
        sys.stdout.write('Next Ping - ' + (str(secrets.PING_INTERVAL - i)).zfill(2))
        sys.stdout.flush()
        sys.stdout.write('\r')
        time.sleep(1)

