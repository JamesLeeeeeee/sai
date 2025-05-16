from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 라우트 등록
    from app.routes.mbti_routes import mbti_bp
    app.register_blueprint(mbti_bp)
    
    return app