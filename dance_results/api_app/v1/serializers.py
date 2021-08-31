from rest_framework import serializers
from .. import models
from django.db import IntegrityError
from drf_queryfields import QueryFieldsMixin


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = "__all__"


class AdjudicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adjudicator
        fields = "__all__"


class AdjudicatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adjudicator
        fields = ('id', 'url', 'name')


class AdjudicatorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Adjudicator
        fields = ('id', 'url', 'name', 'description',
                  'country_code', 'competition', 'created_at')


class DanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dance
        fields = ("id", "title")
        read_only_fields = ('title', 'url',)


class DanceDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Dance
        fields = ("id", "title", "description", "events")
        extra_kwargs = {'events': {'required': False}}


class EventListSerializer(serializers.ModelSerializer):
    dances = DanceListSerializer(many=True, required=False)

    class Meta:
        model = models.Event
        fields = ("id", "title", "description", "dances", "competition")


class EventDetailSerializer(serializers.ModelSerializer):
    dances = DanceListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Event
        fields = ("id", "title", "description", "dances", "competition")

    def create(self, validated_data):
        try:
            dance_ids = []
            for dance in self.initial_data['dances']:
                if 'id' not in dance:
                    raise serializers.ValidationError({'detail': 'key error'})
                dance_ids.append(dance['id'])

            new_event = models.Event.objects.create(**validated_data)

            if dance_ids:
                for dance_id in dance_ids:
                    new_event.dances.add(dance_id)
            new_event.save()
            return new_event

        except Exception as e:
            raise serializers.ValidationError({'detail': e})

    def update(self, instance, validated_data):
        # Delete all records of genres.
        try:
            for current_genre in instance.dances.all():
                instance.dances.remove(current_genre)

            # Repopulate genres into instance.
            for dance in self.initial_data['dances']:
                if 'id' not in dance:
                    raise serializers.ValidationError({'detail': 'key error'})
                dance_obj = models.Dance.objects.get(pk=dance['id'])
                instance.dances.add(dance_obj)

                event_updated = super().update(instance, validated_data)

            return event_updated
        except Exception as e:
            raise serializers.ValidationError({'detail': e})


class CompetitionSerializer(serializers.ModelSerializer):
    adjudicators = AdjudicatorListSerializer(many=True, required=False)
    events = EventListSerializer(many=True, required=False)

    class Meta:
        model = models.Competition
        fields = ("id", "title", "description",
                  "adjudicators", "creator", "events")
