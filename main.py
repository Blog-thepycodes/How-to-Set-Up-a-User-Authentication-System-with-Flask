from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
 
 
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random string
 
 
users = {
   # Example user data, replace with a proper database in a real application
   'user1': generate_password_hash('password1'),
   'user2': generate_password_hash('password2')
}
 
 
@app.route('/')
def index():
   return render_template('index.html')
 
 
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       if username in users and check_password_hash(users[username], password):
           session['username'] = username
           return redirect(url_for('dashboard'))
       else:
           error = 'Invalid username or password'
           return render_template('login.html', error=error)
   return render_template('login.html')
 
 
@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       if username not in users:
           users[username] = generate_password_hash(password)
           return redirect(url_for('login'))
       else:
           error = 'Username already exists'
           return render_template('register.html', error=error)
   return render_template('register.html')
 
 
@app.route('/dashboard')
def dashboard():
   if 'username' in session:
       return render_template('dashboard.html', username=session['username'])
   return redirect(url_for('login'))
 
 
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))
 
 
if __name__ == '__main__':
   app.run(debug=True)
