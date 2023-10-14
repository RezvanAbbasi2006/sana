from rest_framework import serializers
from clinic.models import Reception, UserProfile, Visit


class ReceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reception
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data['title']
        date = validated_data['date']
        time = validated_data['time']
        mobile = validated_data['mobile']
        doctor = validated_data['doctor']

        patient = UserProfile.objects.get(mobile__exact=mobile)

        reception = Reception(
            doctor=doctor,
            title=title,
            date=date,
            time=time,
            patient=patient
        )
        reception.save()
        return reception

    def list(self, **validated_data):
        return validated_data


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def create(self, **validated_data):
        reception_id = validated_data['validated_data']['reception_id']
        reception = Reception.objects.get(id=int(reception_id))
        result = validated_data['validated_data']['result']

        visit = Visit(
            reception=reception,
            result=result
        )
        visit.save()
        return visit

    def list(self, **validated_data):
        return validated_data
