import os
import random
import string
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

USER = os.getenv('API_USER', 'username')
PASS = os.getenv('API_PASS', 'password')  # Set your password in environment


def validate_credentials(auth):
    return auth and auth.username == USER and auth.password == PASS


def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_date():
    start_date = datetime(2010, 1, 1)
    end_date = datetime.now()
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime('%d %b %Y')


def random_url():
    base = "https://www.fake.com/resource/en/datasheet/"
    filename = random_string('st', 8) + ".pdf"
    return base + filename


@app.route('/api/v1/filemetadata', methods=['GET'])
def file_metadata():
    auth = request.authorization
    if not validate_credentials(auth):
        resp = make_response('Authentication required', 401)
        resp.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
        return resp

    results = []
    for _ in range(50):
        id = random_url()
        data = {
            "alternate_name_s": random_string('ds'),
            "associationType_s": random.choice(["Datasheet", "Manual", "Specification"]),
            "id": id,
            "intentDocumentType_s": random.choice(["Technical Documents", "User Guide", "Reference Manual"]),
            "last_modification_date_s": random_date(),
            "locale_s": random.choice(["en", "fr", "de", "it"]),
        }
        results.append(data)
    return jsonify(results)


if __name__ == '__main__':
    # For local HTTPS, generate cert.pem and key.pem using OpenSSL
    app.run()  # This runs on localhost:5000 by default
