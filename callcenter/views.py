from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import csv
from .serializers import BeneficiarySerializer

class BeneficiarySearchView(APIView):
    # … your authentication classes/mixins …

    def get(self, request):
        return Response(
            {"detail": "Please use POST with a JSON body of filters."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request):
        # 1) Auth check
        token = request.headers.get('X-API-KEY')
        if token != settings.API_TOKEN:
            return Response({"detail": "Unauthorized"},
                            status=status.HTTP_401_UNAUTHORIZED)

        # 2) Extract filters from JSON body
        data = request.data
        case_number = data.get('Case_Number')
        phone       = data.get('phone')
        first_name  = data.get('first_name')
        family_name = data.get('family_name')
        id_number   = data.get('id_number')
        dob         = data.get('dob')

        # 3) Require at least one filter
        if not (case_number or phone or first_name or family_name or id_number or dob):
            return Response(
                {"detail": "Please provide at least one filter parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4) Name‐search sanity
        if (first_name and not family_name) and (first_name and not dob) :
            return Response(
                {"detail": "Both first_name and family_name are required for name search."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if (family_name and not first_name) :
            return Response(
                {"detail": "Both first_name and family_name are required for name search."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (dob and not first_name):
            return Response(
                {"detail": "Both first_name and date of birth are required for name search."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 5) Load & filter CSV
        if not settings.CSV_FILE_PATH.exists():
            return Response(
                {"detail": "Data source not available"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        results = []
        with open(settings.CSV_FILE_PATH, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if case_number and row.get('Case_Number') != case_number:
                    continue
                if phone:
                    if not (row.get('HoH_Mobile') == phone
                            or row.get('Alt_Mobile') == phone):
                        continue
                if first_name and family_name:
                    # match *any* of the four name fields, not all at once
                    name_match = (
                        (row['HoH_FirstName_Ar'], row['HoH_FamilyName_Ar']) == (first_name, family_name)
                        or (row['Alt_FirstName_Ar'], row['Alt_FamilyName_Ar']) == (first_name, family_name)
                        or (row['HoH_FirstName_En'], row['HoH_FamilyName_En']) == (first_name, family_name)
                        or (row['Alt_FirstName_En'], row['Alt_FamilyName_En']) == (first_name, family_name)
                    )
                    if not name_match:
                        continue

                if id_number:
                    hoh = row.get('HoH_id_number')
                    alt = row.get('Alt_id_number')    
                    if not (hoh == id_number or alt == id_number):
                        continue

                if first_name and dob:
                    hhNameAr = row.get('HoH_FirstName_Ar')
                    hhNameEn = row.get('HoH_FirstName_En')
                    altNameAr = row.get('Alt_FirstName_Ar')
                    altNameEn = row.get('Alt_FirstName_En')
                    hoh_dob = row.get('HoH_DOB')
                    hoh_dob = hoh_dob[:10]
                    alt_dob = row.get('Alt_DOB')
                    alt_dob = alt_dob[:10]

                    name_match = (
                        (hhNameAr, hoh_dob) == (first_name, dob)
                        or (hhNameEn, hoh_dob) == (first_name, dob)
                        or (altNameAr, alt_dob) == (first_name, dob)
                        or (altNameEn, alt_dob) == (first_name, dob)
                    )

                    if not name_match:
                        continue

                results.append(row)

        # 6) Serialize & return
        serializer = BeneficiarySerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
