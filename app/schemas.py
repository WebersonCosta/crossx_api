# app/schemas.py
from . import ma
from .models import Aluno, Pagamento
from marshmallow import fields, validate

class PagamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pagamento
        load_instance = True

    Data = fields.Date(required=True, error_messages={"required": "O campo Data é obrigatório."})
    Valor = fields.Float(required=True, validate=validate.Range(min=0), error_messages={"required": "O campo Valor é obrigatório."})
    Tipo = fields.String(
        required=True,
        validate=validate.OneOf(["dinheiro", "cartão"]),
        error_messages={"required": "O campo Tipo é obrigatório.", "oneOf": "Tipo deve ser 'dinheiro' ou 'cartão'."}
    )

    ID_Pagamento = fields.Integer(dump_only=True)
    ID_Aluno = fields.Integer(dump_only=True) 

pagamento_schema = PagamentoSchema()
pagamentos_schema = PagamentoSchema(many=True)


class AlunoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aluno
        load_instance = True
        include_relationships = True

    pagamentos = fields.List(fields.Nested(PagamentoSchema), dump_only=True)
    Nome = fields.String(required=True) 
    ID_Aluno = fields.Integer(dump_only=True) 
    Data_Matricula = fields.Date(allow_none=True) 
    Data_Desligamento = fields.Date(allow_none=True, dump_only=True) 
    Data_Vencimento = fields.Date(allow_none=True, dump_only=True) 

aluno_schema = AlunoSchema()
alunos_schema = AlunoSchema(many=True)
pagamento_schema = PagamentoSchema()
pagamentos_schema = PagamentoSchema(many=True)