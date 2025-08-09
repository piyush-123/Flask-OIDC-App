from flask import Flask,redirect,url_for,session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token


app = Flask(__name__)
app.secret_key = 'test'


oauth = OAuth(app)

oauth.register(name='google',
               client_id='',
               client_secret='',
               server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
               client_kwargs={'scope':'openid email profile'})

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f'Hello,{user["name"]}! <a href="/logout">Logout</a>'
    return 'Welcome <a href="/login">Login with Google </a>'

@app.route('/login')
def login():
    redirect_uri = url_for('callback',_external=True)
    print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri,nonce=session['nonce'])

@app.route('/callback')
def callback():
    print('reached callbaxk')
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token,nonce=session['nonce'])
    session['user'] = {
        'name':user_info['name'],
        'email':user_info['email']
    }
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)