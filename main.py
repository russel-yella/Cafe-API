from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    all_cafe = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(all_cafe)
    return jsonify(cafe = random_cafe.to_dict())

@app.route("/all", methods=["GET"])
def get_all_cafe():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return jsonify(all_cafe =[cafe.to_dict() for cafe in all_cafes])

@app.route("/search", methods=["GET"])
def search():
    location = request.args.get("loc")

    result = db.session.execute(
        db.select(Cafe).where(Cafe.location == location)
    )

    cafes = result.scalar().all()

    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, no cafe at that location."})

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        new_cafe = Cafe(
        name = request.form["name"],
        map_url = request.form["map_url"],
        img_url = request.form["img_url"],
        location = request.form["location"],
        seats = request.form["seats"],
        has_wifi = bool(request.form["has_wifi"]),
        has_sockets = bool(request.form["has_sockets"]),
        has_toilet = bool(request.form["has_toilet"]),
        can_take_calls = request.form["can_take_calls"],
        coffee_price = request.form["coffee_price"],
        )
        db.session.add(new_cafe)
        db.session.commit()

    return jsonify(response={"success: Cafe successfully added"})



# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe is None:
        return jsonify(error={
                "Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    cafe.coffee_price = new_price
    db.session.commit()

    return jsonify(
        response={
            "success": "Successfully updated the price." }), 200
# HTTP DELETE - Delete Record

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")

    if api_key != "TopSecretAPIKey":
        return jsonify(
            error={
                "Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."} ), 403
    cafe = db.session.get(Cafe, cafe_id)

    if cafe is None:
        return jsonify(
            error={
                "Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    db.session.delete(cafe)
    db.session.commit()

    return jsonify(
        response={
            "success": "Successfully deleted the cafe from the database."}), 200


if __name__ == '__main__':
    app.run(debug=True)
