from flask import Flask, render_template, request, redirect, url_for
import user_management
import queries_flask

app = Flask(__name__, static_url_path='/static')

# @app.route('/')
# def logpage():
#     return render_template('login.html')

# @app.route('/', methods=["POST", "GET"])
# def login():
#     username = str(request.form.get("username")).capitalize()
#     password = request.form.get("password")
#     access = user_management.log_func(username, password)
#     if access:
#         return redirect('/home')
#     if not access:
#         message = "Invalid username or password"
#         return render_template('login.html', message=message)


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/display", methods=["POST", "GET"])
def display():
    display = queries_flask.display_products()
    return render_template("display.html", display=display)

@app.route("/update", methods=["POST", "GET"])
def update():
    def check():
        if request.method == "POST":
            product_name = request.form.get("product_name")
            new_quantity = request.form.get("quantity")
            new_price = request.form.get("price")
            new_location = request.form.get("location")
            if product_name:
                update_product = queries_flask.update_product(product_name, new_quantity, new_price, new_location)

                if update_product:
                    message = f"The {product_name} was updated successfully"
                    return (message)
                if not update_product:
                    message = f"The {product_name} doesn't exist in the inventory."
                    return (message)
    message = check()  
    return render_template("update.html", message=message)

@app.route("/add", methods=["POST", "GET"])
def add():
    def check():
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            price = request.form.get("price")
            location = request.form.get("location")
            if product_name and quantity and price and location:
                add_product = queries_flask.add_new_product(product_name, quantity, price, location)
                if add_product:
                    message_done = f"The product {product_name} was added sucessfully!"
                    return (message_done)
                if not add_product:
                    message_not = "Something went wrong. Please make sure the product is new to the inventory and insert a valid input."
                    return (message_not)
    message = check()
    return render_template("add.html", message=message)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    def check():
        if request.method == "POST":
            product = request.form.get("product_name")
            product_name = str(product).capitalize()
            if product_name:
                delete_product = queries_flask.delete_func(product_name)
                if delete_product:
                    message = f"Product {product_name} got deleted successfully."
                    return (message)
                if not delete_product:
                    message = "Please insert a valid product name"
                    return (message)
    message = check()
    return render_template("delete.html", message=message)
    


if __name__ == "__main__":
    app.run(debug=True)