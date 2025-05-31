# app/resources.py
from flask_restful import Resource
from flask import request, current_app
from .models import db, Aluno, Pagamento 
from .schemas import (
    aluno_schema, alunos_schema,
    pagamento_schema, pagamentos_schema
)
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

class AlunoListResource(Resource):
    def get(self):
        """Consultar dados de todos os alunos."""
        alunos = Aluno.query.all()
        return alunos_schema.dump(alunos), 200

    def post(self):
        """Criar novo aluno."""
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Nenhum dado de entrada fornecido'}, 400
        
        try:
            novo_aluno = aluno_schema.load(json_data, partial=True)
        except ValidationError as err:
            return {'errors': err.messages}, 422

        if novo_aluno.Data_Matricula:
            novo_aluno.Data_Vencimento = novo_aluno.Data_Matricula + timedelta(days=30)
            novo_aluno.Data_Desligamento = None
        
        db.session.add(novo_aluno)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Erro de integridade ao salvar aluno. Verifique os dados.'}, 500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro desconhecido ao salvar novo aluno: {e}")
            return {'message': 'Erro desconhecido ao salvar aluno no banco de dados.'}, 500
            
        return aluno_schema.dump(novo_aluno), 201

class AlunoResource(Resource):
    def get(self, aluno_id):
        """Consultar dados de um aluno específico."""
        aluno = Aluno.query.get_or_404(aluno_id)
        return aluno_schema.dump(aluno), 200

    def put(self, aluno_id):
        """Atualizar dados pessoais ou de matrícula de um aluno."""
        aluno = Aluno.query.get_or_404(aluno_id)
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Nenhum dado de entrada fornecido'}, 400

        try:
            aluno_schema.load(json_data, instance=aluno, partial=True)
        except ValidationError as err:
            return {'errors': err.messages}, 422

        if 'Data_Matricula' in json_data: # Se o campo foi enviado na requisição
            if aluno.Data_Matricula: # Se Data_Matricula é uma data válida após o load
                aluno.Data_Vencimento = aluno.Data_Matricula + timedelta(days=30)
                aluno.Data_Desligamento = None
            elif json_data.get('Data_Matricula') is None: # Se Data_Matricula foi explicitamente enviada como null
                aluno.Data_Vencimento = None

        if 'Data_Desligamento' in json_data: # Se o campo foi enviado na requisição
            if json_data['Data_Desligamento']:
                try:
                    aluno.Data_Desligamento = datetime.strptime(json_data['Data_Desligamento'], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return {'message': 'Formato inválido para Data_Desligamento. Use YYYY-MM-DD.'}, 400
            else: 
                aluno.Data_Desligamento = None
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': f'Erro ao salvar alterações do aluno: {str(e)}'}, 500
            
        return aluno_schema.dump(aluno), 200

    def delete(self, aluno_id):
        """Excluir aluno (apenas se Data_Desligamento não for nula)."""
        aluno = Aluno.query.get_or_404(aluno_id)
        
        if aluno.Data_Matricula and not aluno.Data_Desligamento:
            return {'message': 'Aluno ativo não pode ser excluído. Registre o desligamento primeiro.'}, 400
        
        if not aluno.Data_Desligamento:
            return {'message': 'Aluno só pode ser excluído se possuir uma data de desligamento. Se nunca foi matriculado, registre um desligamento fictício ou ajuste a regra.'}, 400
        
        db.session.delete(aluno)
        db.session.commit()
        return {'message': 'Aluno excluído com sucesso.'}, 200

class AlunoMatriculaResource(Resource):
    def post(self, aluno_id):
        """Endpoint específico para matricular/renovar um aluno."""
        aluno = Aluno.query.get_or_404(aluno_id)
        
        aluno.Data_Matricula = datetime.utcnow().date()
        aluno.Data_Vencimento = aluno.Data_Matricula + timedelta(days=30)
        aluno.Data_Desligamento = None
        
        db.session.commit()
        return {
            'message': f'Aluno {aluno.Nome} matriculado/renovado com sucesso.',
            'data_vencimento': aluno.Data_Vencimento.isoformat()
        }, 200

class AlunoDesligamentoResource(Resource):
    def post(self, aluno_id):
        """Endpoint específico para registrar o desligamento de um aluno."""
        aluno = Aluno.query.get_or_404(aluno_id)
        
        aluno.Data_Desligamento = datetime.utcnow().date()
        
        db.session.commit()
        return {
            'message': f'Aluno {aluno.Nome} desligado com sucesso.',
            'data_desligamento': aluno.Data_Desligamento.isoformat()
        }, 200

class PagamentoListResource(Resource):
    def get(self, aluno_id=None): 
        """Consultar histórico de pagamentos."""
        if aluno_id:
            Aluno.query.get_or_404(aluno_id) 
            pagamentos = Pagamento.query.filter_by(ID_Aluno=aluno_id).all()
        else:
            pagamentos = Pagamento.query.all()
        return pagamentos_schema.dump(pagamentos), 200

    def post(self, aluno_id=None): 
        """Registrar novo pagamento."""
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Nenhum dado de entrada fornecido'}, 400

        target_aluno_id = aluno_id 
        
        if not target_aluno_id: 
            if 'ID_Aluno' not in json_data:
                return {'message': 'ID_Aluno não fornecido na URL nem no corpo da requisição.'}, 400
            target_aluno_id = json_data.get('ID_Aluno') 

        aluno_obj = Aluno.query.get(target_aluno_id)
        if not aluno_obj:
            return {'message': f'Aluno com ID {target_aluno_id} não encontrado.'}, 404

        try:
            novo_pagamento = pagamento_schema.load(json_data)
        except ValidationError as err:
            return {'errors': err.messages}, 422
        
        novo_pagamento.ID_Aluno = aluno_obj.ID_Aluno
        
        db.session.add(novo_pagamento)
        
        data_pagamento_efetuado = novo_pagamento.Data
        aluno_obj.Data_Vencimento = data_pagamento_efetuado + timedelta(days=30)
        if not aluno_obj.Data_Matricula:
            aluno_obj.Data_Matricula = data_pagamento_efetuado
        aluno_obj.Data_Desligamento = None

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Erro de integridade ao salvar pagamento.'}, 500
        except Exception as e:
            db.session.rollback()
            return {'message': f'Erro desconhecido ao salvar pagamento: {str(e)}'}, 500
            
        return pagamento_schema.dump(novo_pagamento), 201

class PagamentoResource(Resource):
    def get(self, pagamento_id):
        """Consultar um pagamento específico."""
        pagamento = Pagamento.query.get_or_404(pagamento_id)
        return pagamento_schema.dump(pagamento), 200

    def put(self, pagamento_id):
        """Atualizar pagamento (opcional)."""
        pagamento = Pagamento.query.get_or_404(pagamento_id)
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Nenhum dado de entrada fornecido'}, 400

        try:
            pagamento_schema.load(json_data, instance=pagamento, partial=True)
        except ValidationError as err:
            return {'errors': err.messages}, 422

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': f'Erro ao salvar alterações do pagamento: {str(e)}'}, 500
            
        return pagamento_schema.dump(pagamento), 200

    def delete(self, pagamento_id):
        """Excluir pagamento (opcional)."""
        pagamento = Pagamento.query.get_or_404(pagamento_id)
        db.session.delete(pagamento)
        db.session.commit()
        return {'message': 'Pagamento excluído com sucesso.'}, 200