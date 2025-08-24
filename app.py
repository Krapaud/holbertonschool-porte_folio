from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev' # Should be a real secret in production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here we will add the authentication logic later
        print(f"Username: {username}, Password: {password}")
        flash('Vous êtes maintenant connecté !')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas !')
            return redirect(url_for('register'))

        # Here we will add the user creation logic later
        print(f"Username: {username}, Email: {email}, Password: {password}")
        flash('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)