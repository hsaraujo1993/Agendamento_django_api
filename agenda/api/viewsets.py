
from rest_framework.viewsets import ModelViewSet

from agenda.api.serializers import AgendamentoSerializer
from agenda.models import Agendamento


class AgendamentoViewSet(ModelViewSet):

    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        return Agendamento.objects.filter(cancelamento=False)

