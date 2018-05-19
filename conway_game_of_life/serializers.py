from rest_framework import serializers
from conway_game_of_life.models import Grid

class GridSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    x = serializers.IntegerField(required=True)
    y = serializers.IntegerField(required=True)
    data = serializers.CharField(required=True)
    
    def create(self, validated_data):
        return Grid.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.x = validated_data.get('x', instance.x)
        instance.y = validated_data.get('y', instance.y)
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance
    
    class Meta:
        model = Grid
        fields = ('id', 'x', 'y', 'data')