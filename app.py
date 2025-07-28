import mercadopago
from flask import Flask, render_template
from flask import request, jsonify


app = Flask(__name__)

sdk = mercadopago.SDK("TU_ACCESS_TOKEN")  

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/crear_preferencia", methods=["POST"])
def crear_preferencia():
    data = request.get_json()

    preference_data = {
        "items": [
            {
                "title": data["titulo"],
                "quantity": 1,
                "unit_price": float(data["precio_total"]),
                "currency_id": "ARS"
            }
        ],
        "back_urls": {
            "success": "https://tuweb.com/success",
            "failure": "https://tuweb.com/failure",
            "pending": "https://tuweb.com/pending"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    return jsonify(preference_response["response"])


if __name__ == '__main__':
    app.run(debug=True)  