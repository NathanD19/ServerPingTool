ServerPingTool

Ping tool that pings server(s) on an internal network, notifying by text message if the server is offline/not responding.
The tool pings a sever every minute, if the server does not reply, an sms message will be sent. A cool down is included to avoid spam.

This tool was created because I dont want to pay for any server monitoring tools or want bloated software running on my machine 

Requirements:

Linux Machine (windows does not work with subprocess.call() - always returns that the server is online (True), sorry)

AWS Account with SNS User