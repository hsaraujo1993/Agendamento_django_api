import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
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
        horario_data = Agendamento.objects.filter(email=email, data_horario__date=data_horario)
        horario_existe = Agendamento.objects.filter(data_horario=data_horario)
        mais_trinta = data_horario + datetime.timedelta(minutes=30)
        menos_trinta = data_horario - datetime.timedelta(minutes=30)
        # intervalo_agendamento = Agendamento.objects.filter(data_horario__=data_horario)

        if email.endswith(".br") and telefone.startswith("+") and not telefone.startswith("+55"):
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")

        elif telefone not in ['(', ')', '-'] and not telefone.startswith("+"):
            raise serializers.ValidationError({"message": "Telefone fora do formato padrão!"})

        elif len(telefone) < 8:
            raise serializers.ValidationError({"message": "Telefone deve contem no minimo 8 digitos"})

        elif horario_data:
            raise serializers.ValidationError({"message": "E-mail já possui agendamento para essa data!"})

        elif horario_existe.exists():
            raise serializers.ValidationError({"message": f"Já existe agendamento para essa data! Favor inserir {menos_trinta} ou {mais_trinta}"})

        return attrs
