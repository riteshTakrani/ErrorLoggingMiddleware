from datetime import datetime
from rest_framework.decorators import renderer_classes, api_view, APIView
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import status


class Actions(APIView):
    @csrf_exempt
    def post(self, request):
        if request.method == "POST":
            error_serializer = self.prep_data(request)
            if error_serializer.is_valid():
                error_serializer.save()
                return Response("Create successful", status.HTTP_201_CREATED)
            err = error_serializer.errors
            return Response("Failed to add entry", status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = self.fetch_queryset(request)
        if queryset:
            serializer_context = {
                'request': request,
            }
            status_get = ResponseSerializer(queryset, many=True, context=serializer_context).data
            return Response(status_get, status.HTTP_200_OK)
        else:
            Response("No matching records founds.", status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        queryset = self.fetch_queryset(request)
        if queryset:
            queryset.delete()
            return Response("Successfully deleted entry", status.HTTP_202_ACCEPTED)
        else:
            Response("No matching records founds.", status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def put(self, request):
        queryset = self.fetch_queryset(request)
        error_data = JSONParser().parse(request)
        no_fields = len(error_data[0])
        fields = list(error_data[0].keys())
        if no_fields == 2:
            # updating both elements (status and error)
            for items in fields:
                if items == "status" or items == "error":
                    continue
                else:
                    return Response("Invalid input to update.", status.HTTP_400_BAD_REQUEST)
            queryset.update(status=error_data[0]["status"], error=error_data[0]["error"])
            return Response("Entries Updated", status.HTTP_201_CREATED)

        elif no_fields == 1:
            # updating one element
            if fields[0] == "status":
                queryset.update(status=error_data[0]["status"])
                return Response("Entries Updated", status.HTTP_201_CREATED)
            elif fields[0] == "error":
                queryset.update(error=error_data[0]["error"])
                return Response("Entries Updated", status.HTTP_201_CREATED)
        return Response("Invalid input to update.", status.HTTP_400_BAD_REQUEST)

    def fetch_queryset(self, request):
        query_param_sc = request.GET.get('sc', '')
        query_param_id = request.GET.get('id', '')
        if query_param_sc == "" and query_param_id == "":
            queryset = ResponseModel.objects.all()
        elif query_param_id == "":
            queryset = ResponseModel.objects.filter(status=query_param_sc)
        elif query_param_sc == "":
            queryset = ResponseModel.objects.filter(id=query_param_id)
        return queryset

    def prep_data(self, request):
        # prep data for post and put
        error_data = JSONParser().parse(request)
        time_now = datetime.now(tz=timezone.utc)
        for ele in error_data:
            ele['entry_date'] = time_now
        return ResponseSerializer(data=error_data, many=True)