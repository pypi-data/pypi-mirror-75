from rest_framework import serializers
from ..models import Like


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        exclude = (
            'uuid',
            'object_id',
            'content_type',
        )
