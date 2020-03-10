import sys
import smtplib
import netifaces
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_text(ip_string):
	# the following line needs your Twilio Account SID and Auth Token
	client = Client("ACxxx", "xxx")
	# change the "from_" number to your Twilio number and the "to" number
	# to the phone number you signed up for Twilio with, or upgrade your
	# account to send SMS to any phone number
	client.messages.create(to="xxx(Sombody you love)", 
	                       from_="xxx(Twilio Number)", 
	                       body="Raspberry Pi IP: " + ip_string)

def send_email(ip_string):
	gmail_user = 'xxx(email)'
	gmail_password = 'xxx(super secret password)'

	sent_from = gmail_user
	to = 'xxx, xxx, xxx(People you want to get the email)'

	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Subject HERE'
	msg['From'] = sent_from
	msg['To'] = to

	ip_table = ""
	for ip in ip_string:
		ip_table += "<tr><td><span style='color: #ffffff;''>"+ip+"</span></td></tr>"
	
	# Create the body of the message (a plain-text and an HTML version).
	text = "From Raspberry Pi startup script"
	html = ("""
	<html>
	  <head></head>
	  <body>
	  	<h1 style="color: #FDA7DF;">Raspberry PI IP</h1>
	    <table style="background-color: #FDA7DF;">
		<thead>
		<tr>
		<td><em><strong><span style="color: #ffffff;">IP ADDRESS</span></strong></em></td>
		</tr>
		</thead>
		<tbody>
		""" + ip_table +
		"""
		</tbody>
		</table>
	  </body>
	</html>
	""")

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	try:
	    server = smtplib.SMTP('smtp.gmail.com', 587)
	    server.ehlo()
	    server.starttls()
	    server.login(gmail_user, gmail_password)
	    server.sendmail(sent_from, to, msg.as_string())
	    server.close()

	    print('Email sent!')
	except:
	    print('Something went wrong: ' + str(sys.exc_info()[0]))

def get_machine_ips():
    """Get the machine's ip addresses

    :returns: list of Strings of ip addresses
    """
    addresses = []
    print("interfaces: " + str(netifaces.interfaces()))
    for interface in netifaces.interfaces():
        try:
            iface_data = netifaces.ifaddresses(interface)
            for family in iface_data:
                if family not in (netifaces.AF_INET, netifaces.AF_INET6):
                    continue
                for address in iface_data[family]:
                    addr = address['addr']

                    # If we have an ipv6 address remove the
                    # %ether_interface at the end
                    if family == netifaces.AF_INET6:
                        addr = addr.split('%')[0]
                    addresses.append(addr)
        except ValueError:
            pass
    return addresses

def wait_for_internet_connection():
    while True:
        try:
            response = urllib2.urlopen('http://google.com',timeout=1)
            return
        except urllib2.URLError:
            pass

wait_for_internet_connection()
# get ip address and send out
ip_string = get_machine_ips()
filter_ip = [x for x in ip_string if not x.startswith("127") and ":" not in x]
#send_text(str(ip_string))
send_email(filter_ip)
