from rest_framework import viewsets, status
from rest_framework import serializers as rf_serializers

from . import serializers
from .. import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from .. import exceptions


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all().order_by('ename')
    serializer_class = serializers.EmployeeSerializer


class CompetitionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = models.Competition.objects.all().order_by('title')
    serializer_class = serializers.CompetitionSerializer

    def get_queryset(self):
        queryset = models.Competition.objects.filter(
            creator=self.request.user.id)
        return queryset


class AdjudicatorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdjudicatorListSerializer
    detail_serializer_class = serializers.AdjudicatorDetailSerializer
    permission_classes = (IsAuthenticated,)

    queryset = models.Adjudicator.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = models.Adjudicator.objects.all()
        # Example of url parameters.
        competition = self.request.query_params.get('competition', None)

        if competition is not None:
            competition = competition.title()
            queryset = queryset.filter(competition__id=competition)
        return queryset


class DanceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DanceListSerializer
    detail_serializer_class = serializers.DanceDetailSerializer

    queryset = models.Dance.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventListSerializer
    detail_serializer_class = serializers.EventDetailSerializer

    queryset = models.Event.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create' or  self.action == 'update':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    # def create(self, request, *args, **kwargs):
    #     try:
    #         data = request.data

    #         dances = []
    #         # Validate all dances id.
    #         for dance_id in data["dances"]:
    #             dances.append(models.Dance.objects.get(id=dance_id))

    #         serializer = self.get_serializer(data=request.data)
    #         if not serializer.is_valid():
    #             raise exceptions.DefaultError()

    #         new_event = serializer.save()
    #         for dance in dances:
    #             new_event.dances.add(dance)
    #         serializer = serializers.EventDetailSerializer(new_event)
    #         return Response(serializer.data)

    #     except:
    #         raise exceptions.DefaultError()
    #     return Response(serializer.data)
