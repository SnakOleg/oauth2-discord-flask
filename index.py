import requests
from flask import Flask, render_template, request, redirect, session
client_id, client_secret = '1234', 'secret' #Client id, client secret
oauth_url = "your oauth2 url"
app = Flask(__name__)
app.secret_key = "cat" # You secret app key
def access_token(code):
	payload = {
		"client_id": client_id,
		"client_secret": client_secret,
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": "http://127.0.0.1:8080/login", #your redirect uri
		"scope": "identify"
	}
	return requests.post("https://discord.com/api/oauth2/token", data=payload).json()["access_token"]
@app.route("/")
def index():
	if 'user' in session:
		return render_template('authorization.html', username=session['user']['username'], discriminator=session['user']['discriminator'])
	return render_template('index.html', url=oauth_url)
@app.route("/login")
def login():
	if 'user' not in session: 
		code = request.args.get('code')
		headers = {"authorization": f"Bearer {access_token(code)}"}
		user_object = requests.get("https://discord.com/api/users/@me", headers=headers).json()
		session['user'] = user_object
		return redirect('/')
	return "You are already logged in."
@app.route("/logout")
def logout():
	if 'user' in session:
		session.pop('user')
		return "You have successfully logged out"
	return "you are not authorized.", 401
if __name__ == "__main__":
	app.run(debug=True, host='127.0.0.1', port=8080)
 
