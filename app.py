from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)

MONGO_URI = "mongodb+srv://linuxlord:XaBQsM@cluster0.9xfckur.mongodb.net/?appName=Cluster0"
DB_NAME = "simple_form_db"
COLLECTION_NAME = "submissions"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    is_success = False

    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message_text = request.form.get('message', '').strip()

            if not name or not email:
                message = "Name and Email are required!"
            else:
                # Insert into MongoDB
                result = collection.insert_one({
                    "name": name,
                    "email": email,
                    "message": message_text
                })

                # If we got here → success
                return redirect(url_for('success'))

        except PyMongoError as e:
            message = f"Database error: {str(e)}"
        except Exception as e:
            message = f"Something went wrong: {str(e)}"

    return render_template('index.html', message=message, is_success=is_success)


@app.route('/success')
def success():
    return render_template('index.html', 
                         message="Data submitted successfully!", 
                         is_success=True)


if __name__ == '__main__':
    app.run(debug=True)