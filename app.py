from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'TEST_SECRET_KEY'

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column('password', db.String(), nullable=False)

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)

new_user = User(username="admin")
new_user.set_password("admin")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)


    



@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route('/auth', methods=['POST'])
def Auth():
    return render_template("auth.html")

@app.route('/login', methods=['GET', 'POST'])
def loginIn():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    print(user.password)
    if user and user.check_password(password):
        session['logged_in'] = True             # проверка через метод
        return redirect(url_for('admin_panel'))
    return "Invalid credentials", 401


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    return "Invalid credentials", 401


@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if not session.get('logged_in'):
        return "ABORTED", 401
    if request.method == "POST":
        # Получаем данные из формы
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        image_url = request.form.get("image_url")

        # Создаем новый товар
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            image_url=image_url
        )
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for("index"))
    return render_template("admin.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        db.session.add(new_user)
        # db.session.commit()
    app.run(debug=True)
    

