from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from dissect.definitions import TRAIT_DESCRIPTIONS, STD_BITLENGTHS
import dissect.utils.database_handler as database_handler

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"

auth = HTTPBasicAuth()
db = database_handler.connect()

users = {
    "user": generate_password_hash("password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def about():
    return render_template("about.html")


@app.route('/curves/')
@auth.login_required
def curve_dashboard():
    return render_template("curves.html", bitlengths=STD_BITLENGTHS)


def find_trait(curve_name, trait_name):
    # TODO move to database_handler

    trait = list(db[f"trait_{trait_name}"].find({"curve": curve_name}))
    for t in trait:
        t["trait"] = trait_name
    return trait


@app.route('/curve/<curve_name>')
@auth.login_required
def curve_detail(curve_name):
    # TODO use database_handler

    curve = db["curves"].find_one({"name": curve_name})
    traits = []
    for key in TRAIT_DESCRIPTIONS.keys():
        traits.extend(find_trait(curve_name, key))
    return render_template("curve.html", curve=curve, traits=traits)


@app.route('/analysis')
@auth.login_required
def analysis():
    return render_template("analysis.html")


@app.route('/traits')
@auth.login_required
def trait_overview():
    return render_template("traits.html", traits=TRAIT_DESCRIPTIONS)


@app.route('/trait/<trait_name>')
@auth.login_required
def trait_detail(trait_name):
    return render_template("trait.html", trait_name=trait_name)


@app.route('/api/curves/')
@auth.login_required
def curves_api():
    # TODO use database_handler

    curve_filter = {}
    if (it := request.args.get("name")):
        curve_filter["name"] = {'$regex': '.*' + it + '.*', "$options": "i"}
    if (it := request.args.get("category")):
        if it in ("std", "sim"):
            curve_filter["simulated"] = it == "sim"
        elif it != "any":
            curve_filter["category"] = it
    if (it := int(request.args.get("bitlength", 0))):
        curve_filter["field.bits"] = it
    if (it := int(request.args.get("cofactor", 0))):
        if it > 10:
            curve_filter["cofactor"] = {"$nin": list(map(hex, range(1, 11)))}
        else:
            curve_filter["cofactor"] = hex(it)
    if (it := request.args.get("field")) and it != "any":
        curve_filter["field.type"] = it


    offset = int(request.args.get("page", 0)) * 50

    result = {}
    for idx, curve in enumerate(db["curves"].find(curve_filter).skip(offset).limit(50)):
        result[idx] = {
            "name": curve["name"],
            "category": curve["category"],
            "bitlength": curve["field"]["bits"],
            "cofactor": int(curve["cofactor"], 16),
            "field": curve["field"]["type"]
        }
    return result
