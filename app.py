"""
This shall be split into managable chunks later. So separate files.
"""
from os import getenv
import secrets
from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime



app = Flask(__name__, static_url_path = '/static', static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


@app.route("/")
def front():
    """
    The front page for non loggged users.
    """
    restaurants = db.session.execute(
        text("SELECT r.id, r.name, AVG(re.rating) as average_rating "
             "FROM restaurants r "
             "LEFT JOIN reviews re ON r.id = re.restaurant_id "
             "GROUP BY r.id, r.name "
             "ORDER BY average_rating DESC "
             "LIMIT 5") 
    ).fetchall()
    return render_template("front_page.html", restaurants=restaurants)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login page, also check here if account is deleted (column = TRUE)
    """
    error_message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check username and password against the database
        user = db.session.execute(
            text("SELECT * FROM users WHERE username=:username AND deleted = FALSE"),
            {"username": username}
        ).fetchone()

        if user and check_password_hash(user.password, password):
            csrf_token = secrets.token_hex(16)
            session["csrf_token"] = csrf_token
            # Login successful -> store the username in the session
            session["username"] = username
            return redirect("/dashboard")

        #In case of wrong input.
        error_message = "Invalid username or password. Please try again."
        return render_template("login.html", error_message=error_message)
        
    #fetching the actual login page...     
    return render_template("login.html", error_message=error_message)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    The register a new user page, keep in mind the delete 
    """
    error_message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username already exists in the database
        existing_user = db.session.execute(
            text("SELECT id FROM users WHERE username=:username"),
            {"username": username}
        ).fetchone()

        if existing_user:
            error_message = "Username already exists. Please choose a different one."
        else:
            #Hash the password before storing it in the database for safety.
            hash_value = generate_password_hash(password)
            

            created_at = datetime.now()
            # Insert the new user into the database
            sql = text("INSERT INTO users (username, password, created_at) VALUES (:username, :password, :created_at)")
            db.session.execute(sql, {"username": username, "password": hash_value, "created_at": created_at})
            db.session.commit()

            # Redirect to the login page if register is successfull
            return redirect("/login")
	#In case of unnsuccessfull register
    return render_template("register.html", error_message=error_message)

def is_authenticated():
    return 'username' in session  # Check if the 'username' key exists in the session



@app.route("/logout")
def logout():
    """
    User logout. 
    """
    del session["username"]
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    """
    The "front-page" for logged in users.
    """
    if not is_authenticated():
        # Redirect unauthenticated users to the login page
        return redirect(url_for('login'))
         # Limit the result to the top 5 restaurants so it doesnt overflow. 
    restaurants = db.session.execute(
        text("SELECT r.id, r.name, AVG(re.rating) as average_rating "
             "FROM restaurants r "
             "LEFT JOIN reviews re ON r.id = re.restaurant_id "
             "GROUP BY r.id, r.name "
             "ORDER BY average_rating DESC "
             "LIMIT 5") 
    ).fetchall()

    return render_template("dashboard.html", restaurants=restaurants)


@app.route("/review", methods=["POST"])
def review():
    """
    The add and review a new restaurant page.
    """
    if not is_authenticated():
        # Redirect unauthenticated users to the login page
        return redirect(url_for('login'))
    if request.method == "POST":
        restaurant_name = request.form["restaurant_name"]
        rating = int(request.form["rating"])
        review_text = request.form["review_text"]
        hashtags = request.form["hashtags"].split(",")#Split hashtags by comma

        # Check if the restaurant already exists, if not, add it
        existing_restaurant = db.session.execute(
            text("SELECT id FROM restaurants WHERE name=:name"),
            {"name": restaurant_name}
        ).fetchone()

        if not existing_restaurant:
            # Create the restaurant if it doesn't exist and obtain its id
            result = db.session.execute(
                text("INSERT INTO restaurants (name, average_rating)\
                 VALUES (:name, :average_rating) RETURNING id"),
                {"name": restaurant_name, "average_rating": rating}
            )
            restaurant_id = result.fetchone()[0]
        else:
            restaurant_id = existing_restaurant[0]

        #Insert the review into the database using
        #the obtained restaurant_id
        result = db.session.execute(
            text("INSERT INTO reviews (restaurant_id, rating, review_text) \
            VALUES (:restaurant_id, :rating, :review_text) RETURNING id"),
            {"restaurant_id": restaurant_id, "rating": rating,\
             "review_text": review_text}
        )
        review_id = result.fetchone()[0]  # Obtain the review_id

        #Insert associations between the review and hashtags for easier access later.
        for hashtag_text in hashtags:
            hashtag_text = hashtag_text.strip()
            if hashtag_text:
                # Check if the hashtag already exists in the database
                existing_hashtag = db.session.execute(
                    text("SELECT id FROM hashtags WHERE hashtag_text=:hashtag_text"),
                    {"hashtag_text": hashtag_text}
                ).fetchone()

                if existing_hashtag:
                    hashtag_id = existing_hashtag[0]
                else:
                    # If the hashtag doesn't exist, insert it into the hashtags table
                    result = db.session.execute(
                    text("INSERT INTO hashtags (hashtag_text) VALUES \
                    (:hashtag_text) RETURNING id"),
                    {"hashtag_text": hashtag_text}
                    )
                    hashtag_id = result.fetchone()[0]

                # Insert the association between the review and hashtag
                db.session.execute(
                    text("INSERT INTO review_hashtags (review_id, hashtag_id)\
                    VALUES (:review_id, :hashtag_id)"),
                    {"review_id": review_id, "hashtag_id": hashtag_id}
                )

                # Insert the association between the restaurant and hashtag
                db.session.execute(
                    text("INSERT INTO restaurant_hashtags (restaurant_id, hashtag_id)\
                    VALUES (:restaurant_id, :hashtag_id)"),
                    {"restaurant_id": restaurant_id, "hashtag_id": hashtag_id}
                )

        db.session.commit()


        return redirect("/dashboard")




@app.route("/restaurant/<int:restaurant_id>")
def restaurant(restaurant_id):
    """
    The page if the user clicks "More information" on the restaurant.
    """
    if not is_authenticated():
        # Redirect unauthenticated users to the login page
        return redirect(url_for('login'))
    restaurant = db.session.execute(
        text("SELECT r.id, r.name, AVG(re.rating) as average_rating "
             "FROM restaurants r "
             "LEFT JOIN reviews re ON r.id = re.restaurant_id "
             "WHERE r.id = :restaurant_id "
             "GROUP BY r.id, r.name"),
             {"restaurant_id": restaurant_id}
    ).fetchone()

    if restaurant:
        # Fetch associated hashtags for the restaurant using restaurant_hashtags
        hashtags = db.session.execute(
            text("""
                SELECT DISTINCT h.hashtag_text
                FROM hashtags h
                JOIN restaurant_hashtags rh ON h.id = rh.hashtag_id
                WHERE rh.restaurant_id = :restaurant_id
            """),
            {"restaurant_id": restaurant_id}
        ).fetchall()

        # Fetch reviews for the restaurant
        reviews = db.session.execute(
            text("SELECT * FROM reviews WHERE restaurant_id = :restaurant_id"),
            {"restaurant_id": restaurant_id}
        ).fetchall()

        return render_template("restaurant_details.html", restaurant=restaurant, \
        hashtags=hashtags, reviews=reviews)

    flash("Restaurant not found.", "error")
    return redirect("/dashboard")



@app.route("/search", methods=["GET"])
def search():
    """
    A search, hashtags possibility not yet implemented,
    this only searches for restaurant names similar to
    the search word.
    """
    if not is_authenticated():
        # Redirect unauthenticated users to the login page
        return redirect(url_for('login'))
    # Get the search text from the query parameters
    search_text = request.args.get("search_text")

    if search_text:
        # Perform a database query to search for restaurants based on the search criteria
        search_result = db.session.execute(
            text("""
                SELECT R.*, AVG(re.rating) as average_rating 
                FROM restaurants R 
                LEFT JOIN reviews re ON R.id = re.restaurant_id
                WHERE R.name ILIKE :search_text
                GROUP BY R.id
            """),    
            {"search_text": f"%{search_text}%"}  # Use ILIKE for case-insensitive search
        ).fetchall()
        
        #Perform a database quert to search for restaurants also related to a certain hashtag... 
        hashtag_result = db.session.execute(
            text("""SELECT R.*, AVG(re.rating) as average_rating
                FROM restaurants R
            	INNER JOIN restaurant_hashtags H ON H.restaurant_id = R.id 
            	INNER JOIN hashtags Y ON Y.id = H.hashtag_id
            	LEFT JOIN reviews re ON R.id = re.restaurant_id
            	WHERE Y.hashtag_text ILIKE :search_text
            	GROUP BY R.id
             """),
            {"search_text": f"%{search_text}%"}
        ).fetchall()
        #add the option of searching via hashtags, somehow displaying the combination of both... 
        

        return render_template("search_results.html", \
        search_text=search_text, search_result=search_result, hashtag_result = hashtag_result)


@app.route("/profile")
def profile():
    if not is_authenticated():
        return redirect(url_for('login'))

    username = session["username"]

    # Fetch the user's join date
    user = db.session.execute(
        text("SELECT created_at FROM users WHERE username=:username"),
        {"username": username}
    ).fetchone()

    # Format the join, looks nicer. 
    user_joined_date = user.created_at.strftime("%B %d, %Y")

    return render_template("profile.html", username=username, user_joined_date=user_joined_date)

@app.route("/confirm_delete", methods=["GET"])
def confirm_delete():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    return render_template("confirm_delete.html")

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if not is_authenticated():
        return redirect(url_for('login'))

    # Validate the user's credentials 
    username = session.get("username")
    password = request.form.get("password") 

    user = db.session.execute(
        text("SELECT * FROM users WHERE username=:username"),
        {"username": username}
    ).fetchone()

    if user and check_password_hash(user.password, password):
        #Deleting kind of:
        db.session.execute(
            text("UPDATE users SET deleted = TRUE WHERE username = :username"),
            {"username": username}
        )
        db.session.commit()

        # Log the user out
        del session["username"]

        # Redirect to a confirmation page
        return redirect("/deleted_confirmation")
    else:
        # Password is incorrect, provide an error message
        error_message = "Incorrect password. Please try again."
        return render_template("delete_account.html", error_message=error_message)


@app.route("/deleted_confirmation")
def deleted_confirmation():
    return render_template("deleted_confirmation.html")

@app.route("/successful_logout")
def successful_logout():
    return render_template("successful_logout.html")
