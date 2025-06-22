from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        msg = str(exc)

        if "UNIQUE constraint failed" in msg:
            detail = "Já existe um registro com esse valor"

        elif "NOT NULL constraint failed" in msg:
            detail = "Preencha todos os campos obrigatórios"

        elif "FOREIGN KEY constraint failed" in msg:
            detail = "Relacionamento inválido. Verifique os dados informados"

        elif "CHECK constraint failed" in msg:
            detail = "Algum dado informado não atende às regras do sistema"

        else:
            detail = "Erro ao salvar o registro"

        return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)
    return response
