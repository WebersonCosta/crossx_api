# app/models.py
from . import db
from datetime import datetime, timedelta

class Aluno(db.Model):
    __tablename__ = 'aluno'

    ID_Aluno = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(150), nullable=False)
    Endereco = db.Column(db.String(200))
    Cidade = db.Column(db.String(100))
    Estado = db.Column(db.String(2)) # UF (Ex: CE, SP)
    Telefone = db.Column(db.String(20))
    Data_Matricula = db.Column(db.Date, nullable=True)
    Data_Desligamento = db.Column(db.Date, nullable=True)
    Data_Vencimento = db.Column(db.Date, nullable=True)

    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Aluno {self.Nome}>'

    @property
    def is_ativo(self):
        """
        Verifica se o aluno está ativo.
        Regra: Se Data_Matricula está preenchida e Data_Desligamento é nula. [cite: 6]
        Adicional: Data_Matricula < Data_Vencimento (interpretado como matrícula válida até vencimento). [cite: 7]
        """
        if self.Data_Matricula and not self.Data_Desligamento:
            if self.Data_Vencimento and self.Data_Matricula < self.Data_Vencimento:
                if datetime.utcnow().date() < self.Data_Vencimento:
                    return True
        return False

    def matricular(self):
        """Realiza a matrícula do aluno."""
        self.Data_Matricula = datetime.utcnow().date()
        self.Data_Vencimento = self.Data_Matricula + timedelta(days=30)
        self.Data_Desligamento = None 

    def registrar_desligamento_por_inadimplencia(self):
        """Registra desligamento se o pagamento não for feito após o vencimento."""
        if self.Data_Vencimento and datetime.utcnow().date() > self.Data_Vencimento and not self.Data_Desligamento:
            pagamento_recente_valido = False
            if self.pagamentos:
                ultimo_pagamento = max(self.pagamentos, key=lambda p: p.Data, default=None)
                if ultimo_pagamento and ultimo_pagamento.Data >= self.Data_Vencimento - timedelta(days=30): 
                    self.Data_Vencimento = ultimo_pagamento.Data + timedelta(days=30) 
                    pagamento_recente_valido = True

            if not pagamento_recente_valido:
                 self.Data_Desligamento = datetime.utcnow().date()


class Pagamento(db.Model):
    __tablename__ = 'pagamento'

    ID_Pagamento = db.Column(db.Integer, primary_key=True)
    ID_Aluno = db.Column(db.Integer, db.ForeignKey('aluno.ID_Aluno'), nullable=False)
    Data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    Valor = db.Column(db.Float, nullable=False)
    Tipo = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Pagamento {self.ID_Pagamento} - Aluno {self.ID_Aluno}>'