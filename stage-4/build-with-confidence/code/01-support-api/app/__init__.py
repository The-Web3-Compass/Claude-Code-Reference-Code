from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from app.routes.customers import bp as customers_bp
    from app.routes.orders import bp as orders_bp
    from app.routes.refunds import bp as refunds_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(refunds_bp, url_prefix="/refunds")

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error: Exception):
        from app.responses import json_error

        return json_error("internal_error", str(error), status=500)

    return app
