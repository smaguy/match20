import sys
import csv
import smtplib, ssl
from smtplib import SMTP
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def find_matches(love_dict):
	match_dict = dict()
	for suid in love_dict:
		email = suid + '@stanford.edu'
		match_dict[email] = []
		inputs = love_dict[suid]
		for name in inputs:
			if name in love_dict and suid in love_dict[name]:
				love_match = name + '@stanford.edu'
				match_dict[email].append(love_match)
	return match_dict

def read_file(filename):
	love_dict = dict()
	with open(filename, newline='') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',')
		firstline = True
		for row in csv_reader:
			if firstline:
				firstline = False
				continue
			SUID = row[0]
			love_dict[SUID] = []
			for i in row:
				if i != SUID and i != '':
					love_dict[SUID].append(i)
	return love_dict

def main():
	love_dict = read_file(sys.argv[1])
	match_dict = find_matches(love_dict)

	smtp_server = "smtp.gmail.com"
	port = 465 
	sender_email = "classof2020@gmail.com"
	password = input("Type your password and press enter: ")
	context = ssl.create_default_context()

	with smtplib.SMTP(smtp_server, port) as server:
	    server = smtplib.SMTP(smtp_server,port)
	    server.ehlo()
	    server.starttls(context=context) 
	    server.ehlo() 
	    server.login(sender_email, password)
	    for name in match_dict:
	    	server.sendmail(sender_email, name, "here are your matches: " + ', '.join(match_dict[name]))
	    	# msg = MIMEMultipart()
	    	# message = "here are your matches: " + ', '.join(match_dict[name])
	    	# msg['From'] ='jacksongeilers@gmail.com'
	    	# msg['To']=name
	    	# msg['Subject']="This is TEST"
	    	# msg.attach(MIMEText(message, 'plain'))
	    	# s.send_message(msg)
	    	# del msg
	    print("Success")
	# except Exception as e:
	#     print("ERROR")
	# finally:
	server.quit() 

if __name__ == '__main__':
	main()