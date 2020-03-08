from flask import Flask, render_template, request, send_from_directory
import requests
import json

app = Flask(__name__)

@app.route('/')
def receiver():
	return render_template('receiver.html')

@app.route('/app')
def sender():
	return render_template('index.html')

@app.route('/message-passer')
def pass_message_to_fcm():

	f = open("./token.txt", "r")
	token_data = f.read()

	tokens = token_data.split("\n")
		
	url = 'https://fcm.googleapis.com/fcm/send'
	
	body = {  
		"data":{  
			"title":"mytitle",
			"body":"mybody",
			"url":"myurl"
		},
		"notification":{  
			"title":request.args.get('title'),
			"body":request.args.get('body'),
			"content_available": "true"
		},
		"registration_ids":tokens
	}

	print(body)

	headers = {
		"Content-Type":"application/json",
        "Authorization": "key=AIzaSyABGIZgHr0ZvTONWS2a8sqikjnGKOrpK94"
    }
	response = requests.post(url, data=json.dumps(body), headers=headers)
	print(response.json())

	return "Message Sent"


@app.route('/firebase-messaging-sw.js')
def service_worker():
	return send_from_directory('./assets/', 'firebase-messaging-sw.js')

@app.route('/capture-token')
def capture_token():
	token = request.args.get('token')
	
	f = open("./token.txt", "a")
	f.write(token + "\n")
	f.close()
	
	return 'message = Success'

app.run()