from flask import Flask
from DBModel import db
from routes import bp

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)