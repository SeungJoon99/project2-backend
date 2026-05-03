from .map_router import map_bp

def init_app(app):
    app.register_blueprint(map_bp, url_prefix="/api")
