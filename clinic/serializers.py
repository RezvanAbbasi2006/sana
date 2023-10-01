from rest_framework import serializers
from clinic.models import Reception, UserProfile, UserReception, Visit


class ReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data['title']
        date = validated_data['date']
        time = validated_data['time']
        profile_id = validated_data['profile_id']

        profile = UserProfile.objects.get(id__exact=profile_id)

        reception = Reception(
            title=title,
            date=date,
            time=time,
            doctor=profile
        )
        reception.save()
        return reception


class UserReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReception
        fields = '__all__'

    def create(self, instance, **validated_data):
        user_id = validated_data['validated_data']['user_id']
        user = UserProfile.objects.get(id=user_id)

        if not instance.in_use:
            user_reception = UserReception(
                user=user,
                reception=instance
            )
            user_reception.save()
            instance.in_use = True
            instance.save()
            return user_reception
        else:
            return "Reception In Use!"

    def list(self, **validated_data):
        return validated_data


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def create(self, **validated_data):
        reception_id = validated_data['validated_data']['reception_id']
        reception = UserReception.objects.get(id=reception_id)
        result = validated_data['validated_data']['result']

        visit = Visit(
            reception=reception,
            result=result
        )
        visit.save()
        return visit
