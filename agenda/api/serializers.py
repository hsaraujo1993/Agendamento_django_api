from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from datetime import date, datetime
from agenda.models import Agendamento


class AgendamentoSerializer(ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'nome', 'email', 'telefone', 'data_horario']

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
        return value

    def validate(self, attrs):
        telefone = attrs.get("telefone", "")
        email = attrs.get("email", "")
        data_horario = attrs.get("data_horario", "")
        obj = Agendamento.objects.filter(email=email, data_horario__lte=data_horario)

        if email.endswith(".br") and telefone.startswith("+") and not telefone.startswith("+55"):
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")

        elif telefone not in ['(', ')', '-'] and not telefone.startswith("+"):
            raise serializers.ValidationError("Telefone fora do formato padrão!")

        elif len(telefone) < 8:
            raise serializers.ValidationError("Telefone deve contem no minimo 8 digitos")

        elif obj:
            raise serializers.ValidationError("já existe")

        return attrs
