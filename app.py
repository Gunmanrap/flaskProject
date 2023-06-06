from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Table %r>' % self.id


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        table = Table(title=title, intro=intro, text=text)

        try:
            db.session.add(table)
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Пры даданні артыкула адбылася памылка'

    else:
        return render_template('create.html')


@app.route('/posts')
def posts():
    table = Table.query.order_by(Table.date.desc()).all()
    return render_template('posts.html', table=table)


@app.route('/posts/<int:id>')
def post_detail(id):
    table = Table.query.get(id)
    return render_template('post_detail.html', table=table)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    table = Table.query.get_or_404(id)

    try:
        db.session.delete(table)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Пры выдаленні артыкула адбылася памылка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    table = Table.query.get(id)
    if request.method == 'POST':
        table.title = request.form['title']
        table.intro = request.form['intro']
        table.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Пры абнаўленні артыкула адбылася памылка'

    else:
        table = Table.query.get(id)
        return render_template('post_update.html', table=table)


if __name__ == '__main__':
    app.run(debug=True)
