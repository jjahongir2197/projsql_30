from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meta.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    pagination = Product.query.paginate(page=page, per_page=per_page)

    return jsonify({
        "data": [p.name for p in pagination.items],
        "meta": {
            "page": page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }
    })

with app.app_context():
    db.create_all()
