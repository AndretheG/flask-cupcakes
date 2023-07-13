"""Flask app for Cupcakes"""
"""Models for Cupcake app."""

from flask import Flask, request, jsonfify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "itsasecret"

connect_db(app)

@app.route("/")
def homepage():
    """Show homepage."""
    return render_template("home.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Shows all cupacakes and returns JSON."""

    cupcakes = [cupcake.todict() for cupcake in Cupcake.query.all()]
    return jsonfify(cupcakes=cupcakes)


@app.route("/api/cupcakes", methods=["POST"])
def make_cupcake():
    """Make a cupcake and return JSON data about it."""

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()

    return (jsonfify(cupcake=cupcake.todict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Show data about specific cupcake in JSON."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonfify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake with data from request. Return updated data in JSON."""

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['rating']

    db.session.add(cupcake)
    db.session.commit()

    return jsonfify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in URL. Respond with JSON message: deleted"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonfify(message="Deleted")
    