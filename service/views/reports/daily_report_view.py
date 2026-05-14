from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

from service.constants import ResponseMessages
from service.models import DailyReport
from service.serializers import DailyReportGetSerializer
from service.utils import Authentication, ResponseHandler


class DailyReportView(APIView):
    def get(self,request):
        user, token =  Authentication.authenticate(request=request)
        query_params = request.query_params
        is_valid = self._validate_params(query_params)

        if not is_valid:
            return ResponseHandler(
                success=False,
                errors= "Invalid Input",
                status = status.HTTP_400_BAD_REQUEST
                )

        filters = self._build_filters(user, query_params)
        daily_report = DailyReport.objects.filter(filters).distinct()
        serializer = DailyReportGetSerializer(daily_report, many=True)
        
        return ResponseHandler(
            success=True,
            message=ResponseMessages.DAILY_REPORT_FETCH,
            data=serializer.data,
            status = status.HTTP_200_OK
        )

    def _build_filters(self, user, query_params):
        on_date = query_params.get("on_date")
        from_date = query_params.get("from_date")
        to_date = query_params.get("to_date")
        search = query_params.get("search")
        filters = Q(user=user)

        if from_date and to_date:
            filters &= Q(report_date__range=[from_date, to_date])
        if search:
            filters &= (Q(description__icontains=search) | Q(tasks__title__icontains=search) | Q(tasks__description__icontains=search))
        if on_date:
            filters &= Q(report_date=on_date)
        return filters

    def _validate_params(self, query_params):
        on_date = query_params.get("on_date")
        from_date = query_params.get("from_date")
        to_date = query_params.get("to_date")

        if on_date:
            if not self._is_valid_date(on_date):
                return False
        if from_date:
            if not self._is_valid_date(from_date):
                return False
        if to_date:
            if not self._is_valid_date(to_date):
                return False
        return True

    def _is_valid_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
