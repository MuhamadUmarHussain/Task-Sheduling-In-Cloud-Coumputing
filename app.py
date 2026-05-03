from flask import Flask

from config import Config
from routes.main_routes import main


def create_app() -> Flask:
	app = Flask(__name__)
	app.config.from_object(Config)
	app.register_blueprint(main)
	return app


if __name__ == "__main__":
	application = create_app()
	application.run(debug=True)
