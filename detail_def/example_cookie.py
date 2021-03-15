from flask import Flask, request, redirect, make_response, Blueprint

app = Flask(__name__)
bp = Blueprint('bp', __name__)

@app.route("/example/cookie")
def example_cookie():
    print(request.cookies)
    return ""

@app.route("/example/cooke_set")
def example_cookie_set():
    redirect_to_cookie = redirect("/example/cookie")
    response = make_response(redirect_to_cookie)
    response.set_cookie('Cookie Register', value='Examplet Cookie')
    return response

@app.route("/example/environ", methods=["GET", "POST"])
def example_environ():
    print(request.is_xhr)
    return ""

@bp.route("/example/blueprint", methods=["GETS", "POST"]) 
def example_environ():
    print(request.blueprint)
    return ""

@app.route("/example/environ", methods=["GET", "POST"])
def example_environ():
    return request.endpoint

app.register_blueprint(bp)
app.run() 