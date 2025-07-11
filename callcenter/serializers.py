from rest_framework import serializers

class BeneficiarySerializer(serializers.Serializer):
    Case_Number         = serializers.CharField()
    Status              = serializers.CharField()
    partner_name        = serializers.CharField(allow_blank=True, required=False)

    HoH_FirstName_Ar    = serializers.CharField()
    HoH_FatherName_Ar   = serializers.CharField()
    HoH_FamilyName_Ar   = serializers.CharField()
    HoH_FirstName_En    = serializers.CharField(allow_blank=True, required=False)
    HoH_FatherName_En   = serializers.CharField(allow_blank=True, required=False)
    HoH_FamilyName_En   = serializers.CharField(allow_blank=True, required=False)
    HoH_DOB             = serializers.CharField()
    HoH_id_type         = serializers.CharField(allow_blank=True, required=False)
    HoH_id_number       = serializers.CharField(allow_blank=True, required=False)
    HoH_Nationality     = serializers.CharField()
    HoH_Gender          = serializers.CharField()
    HoH_Mobile          = serializers.CharField()

    Alt_FirstName_Ar    = serializers.CharField(allow_blank=True, required=False)
    Alt_FatherName_Ar   = serializers.CharField(allow_blank=True, required=False)
    Alt_FamilyName_Ar   = serializers.CharField(allow_blank=True, required=False)
    Alt_FirstName_En    = serializers.CharField(allow_blank=True, required=False)
    Alt_FatherName_En   = serializers.CharField(allow_blank=True, required=False)
    Alt_FamilyName_En   = serializers.CharField(allow_blank=True, required=False)
    Alt_DOB             = serializers.CharField(allow_blank=True, required=False)
    Alt_id_type         = serializers.CharField(allow_blank=True, required=False)
    alT_id_number       = serializers.CharField(allow_blank=True, required=False)
    Alt_Nationality     = serializers.CharField(allow_blank=True, required=False)
    Alt_Gender          = serializers.CharField(allow_blank=True, required=False)
    Alt_Mobile          = serializers.CharField(allow_blank=True, required=False)

    Family_Size2        = serializers.IntegerField()
