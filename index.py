import requests
from flask import Flask, render_template, request, redirect, session
OAUTH2_CLIENT_ID = '949418697813008384'
OAUTH2_CLIENT_SECRET = 'Jn-wM-IuXx7_SwCySD_pPoNf27QI3EqN'
authURL = 'https://discord.com/api/oauth2/authorize'
tokenURL = 'https://discord.com/api/oauth2/token'
apiURLBase = 'https://discord.com/api/users/@me'
revokeURL = 'https://discord.com/api/oauth2/token/revoke'
app = Flask(__name__)
app.secret_key = "NZrEgg9FjFDHEI463G0d"
def access_token(code):
	payload = {
		"client_id": OAUTH2_CLIENT_ID,
		"client_secret": OAUTH2_CLIENT_SECRET,
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": "http://127.0.0.1:8080/login",
		"scope": "identify"
	}
	return requests.post(url=tokenURL, data=payload).json()["access_token"]
@app.route("/")
def index():
	try:
		return render_template('authorization.html', username=session['user']['username'], discriminator=session['user']['discriminator'])
	except KeyError:
		return render_template('index.html')
@app.route("/login")
def login():
	code = request.args.get('code')
	try:
		headers = {"authorization": f"Bearer {access_token(code)}"}
		user_object = requests.get(url=apiURLBase, headers=headers).json()
		session['user'] = user_object
		return redirect('/')
	except Exception:
		return redirect('/')
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8080)
