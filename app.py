from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client.holberton_learning_hub
users_collection = db.users
articles_collection = db.articles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Vous êtes maintenant connecté !', 'success')
            return redirect(url_for('profile'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas !', 'danger')
            return redirect(url_for('register'))

        existing_user = users_collection.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            flash("Ce nom d'utilisateur ou cet email existe déjà.", 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        flash('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = users_collection.find_one({'username': session['username']})
    return render_template('profile.html', user=user)

@app.route('/articles')
def articles():
    all_articles = articles_collection.find().sort('created_at', -1)
    return render_template('articles.html', articles=all_articles)

@app.route('/article/<article_id>')
def article_detail(article_id):
    article = articles_collection.find_one({'_id': ObjectId(article_id)})
    if not article:
        flash('Article non trouvé.', 'danger')
        return redirect(url_for('articles'))
    return render_template('article_detail.html', article=article)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if 'username' not in session:
        flash('Vous devez être connecté pour ajouter un article.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        created_at = datetime.datetime.now()

        if not title or not content:
            flash('Le titre et le contenu sont requis.', 'danger')
            return redirect(url_for('add_article'))

        articles_collection.insert_one({
            'title': title,
            'content': content,
            'author': author,
            'created_at': created_at
        })
        flash('Article ajouté avec succès !', 'success')
        return redirect(url_for('articles'))

    return render_template('add_article.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)