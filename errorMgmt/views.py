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
            error_serializer = prep_data(request)
            if error_serializer.is_valid():
                error_serializer.save()
                return Response("Create successful", status.HTTP_201_CREATED)
            err = error_serializer.errors
            return Response("Failed to add entry", status.HTTP_400_BAD_REQUEST)


def response(msg, status_code):
    #return HttpResponse(msg, status=status_code)
    return Response(msg, status=status_code)


def fetch_queryset(request):
    query_param_sc = request.GET.get('sc', '')
    query_param_id = request.GET.get('id', '')
    if query_param_sc == "" and query_param_id == "":
        queryset = ResponseModel.objects.all()
    elif query_param_id == "":
        queryset = ResponseModel.objects.filter(status=query_param_sc)
    elif query_param_sc == "":
        queryset = ResponseModel.objects.filter(id=query_param_id)
    return queryset


def prep_data(request):
    # prep data for post and put
    error_data = JSONParser().parse(request)
    time_now = datetime.now(tz=timezone.utc)
    for ele in error_data:
        ele['entry_date'] = time_now
    return ResponseSerializer(data=error_data, many=True)


def get(request, queryset):
    serializer_context = {
        'request': request,
    }
    status_get = ResponseSerializer(queryset, many=True, context=serializer_context).data
    return response(status_get, status.HTTP_200_OK)


def delete(queryset):
    queryset.delete()
    return response("Successfully deleted entry", status.HTTP_204_NO_CONTENT)


def put(request, queryset):
    error_data = JSONParser().parse(request)
    no_fields = len(error_data[0])
    fields = list(error_data[0].keys())
    if no_fields == 2:
        # updating both elements (status and error)
        for items in fields:
            if items == "status" or items == "error":
                continue
            else:
                return response("Invalid input to update.", status.HTTP_400_BAD_REQUEST)
        queryset.update(status=error_data[0]["status"], error=error_data[0]["error"])
        return response("Entries Updated", status.HTTP_201_CREATED)

    elif no_fields == 1:
        # updating one element
        if fields[0] == "status":
            queryset.update(status=error_data[0]["status"])
            return response("Entries Updated", status.HTTP_201_CREATED)
        elif fields[0] == "error":
            queryset.update(error=error_data[0]["error"])
            return response("Entries Updated", status.HTTP_201_CREATED)
    return response("Invalid input to update.", status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@csrf_exempt
def RUD_action(request):
    # define RUD ops logic here
    queryset = fetch_queryset(request)
    if queryset:

        # GET request to fetch data
        if request.method == 'GET':
            return get(request, queryset)

        # DELETE request to delete existing data
        elif request.method == "DELETE":
            return delete(queryset)

        # PUT request to modify data
        elif request.method == "PUT":
            return put(request, queryset)
    else:
        return response("No matching records founds.", status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@csrf_exempt
def create_action(request):
    if request.method == "POST":
        error_serializer = prep_data(request)
        if error_serializer.is_valid():
            error_serializer.save()
            return response("Create successful", status.HTTP_201_CREATED)
        err = error_serializer.errors
        return response("Failed to add entry", status.HTTP_400_BAD_REQUEST)
