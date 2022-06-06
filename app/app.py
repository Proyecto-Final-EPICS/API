from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask
from v1 import v1
from v2 import v2
import datetime
import os

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRETKEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

app.register_blueprint(v1)
app.register_blueprint(v2, url_prefix='/v2.0')

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    debug = os.getenv('DEBUG', True)
    # print(os.getenv('DB_URL', 'hola'))
    app.run(host="0.0.0.0", port=port, debug=debug)