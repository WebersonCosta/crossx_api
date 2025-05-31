# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api 
from flask_marshmallow import Marshmallow
from .config import Config 


db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=Config): 

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class) 

    db.init_app(app)
    ma.init_app(app)
    
    from . import models 

    from .resources import (
        AlunoListResource, AlunoResource, AlunoMatriculaResource, AlunoDesligamentoResource,
        PagamentoListResource, PagamentoResource
    )

    api_manager = Api(app, prefix="/api/v1") 

    api_manager.add_resource(AlunoListResource, '/alunos')
    api_manager.add_resource(AlunoResource, '/alunos/<int:aluno_id>')
    api_manager.add_resource(AlunoMatriculaResource, '/alunos/<int:aluno_id>/matricular')
    api_manager.add_resource(AlunoDesligamentoResource, '/alunos/<int:aluno_id>/desligar')
    api_manager.add_resource(PagamentoListResource, '/pagamentos', '/alunos/<int:aluno_id>/pagamentos')
    api_manager.add_resource(PagamentoResource, '/pagamentos/<int:pagamento_id>')

    with app.app_context():
        db.create_all() 

    @app.route('/health')
    def health_check():
        return "API Saudável!", 200 
        
    return app