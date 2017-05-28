from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from django.http import HttpResponse
from database import MongoConnection
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from models import Sites
from models import Images
from datetime import datetime
from time import time
import os
from django.conf import settings
from django.core.files.base import ContentFile
# Create your views here.

#class SiteList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
class SiteList(APIView):

    def get(self, request, *args, **kwargs):
        conditions = dict(request.query_params)
        for key,value in conditions.iteritems():
            conditions[key] = conditions[key][0]
        sites = MongoConnection.find_data("Sites",conditions=None)
        serializer = serializers.SiteSerializer(
                            instance=[ Sites(**element) for element in sites],
                            many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        parameters = request.data
        MongoConnection.insert_data("Sites",parameters)
        return Response({"status":"ok"})

    def put(self, request, *args, **kwargs):
        conditions = dict(request.query_params)
        for key,value in conditions.iteritems():
            conditions[key] = conditions[key][0]
        parameters = request.data
        print conditions
        print parameters
        MongoConnection.update_data("Sites",parameters,conditions)
        return Response({"status":"ok"})

class ImageList(APIView):
    def get(self, request, *args, **kwargs):
        conditions = dict(request.query_params)
        images = MongoConnection.find_data("Images",conditions=conditions)
        serializer = serializers.ImageSerializer(
                            instance=[ Images(**element) for element in images],
                            many=True)
        print serializer.data
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        conditions = dict(request.query_params)
        print str(conditions["site_code"][0])
        created_time = str(time())
        image_name = '%s_%s'%(created_time.replace('.','_'),"test")

        parameters = {
            "image_name":image_name,
            "site_code": conditions["site_code"][0],
            "created_time":created_time,
        }

        MongoConnection.insert_data("Images",parameters)


        directory = os.path.join(settings.MEDIA_ROOT,"images",conditions["site_code"][0])

        # create the folder for storing images if it doesn't exist.
        try:
            os.mkdir(directory)
        except:
            pass

        # write image to storage
        image = request.FILES.get("media")
        filename = '%s_%s'%(str(time()).replace('.','_'),image.name)
        full_filename = os.path.join(directory,image_name)
        output_image = open(full_filename, 'wb+')
        image_content = ContentFile(image.read())

        # iterate through the chunks.
        for chunk in image_content.chunks():
            output_image.write(chunk)
        output_image.close()

        return Response({"status":"ok"})

class DataValues(APIView):
    def get(self, request, *args, **kwargs):
            conditions = dict(request.query_params)
            #print parametesr["sensor_code"][0]
            conditions.update({"datetime":{}})
            for key,value in conditions.iteritems():
                if key == "start_time":
                    # (conditions["datetime"]).update({"$gte": datetime.strptime(conditions[key][0], "%Y-%m-%d %H:%M:%S" )})
                    (conditions["datetime"]).update({"$gte": conditions[key][0]})
                elif key == "end_time":
                    # (conditions["datetime"]).update({"$lte": datetime.strptime(conditions[key][0], "%Y-%m-%d %H:%M:%S" )})
                    (conditions["datetime"]).update({"$lte": conditions[key][0]})
                elif key == "datetime":
                    pass
                else:
                    conditions[key] = conditions[key][0]
            conditions.pop('start_time', None)
            conditions.pop('end_time', None)

            if conditions["datetime"]=={}:
                conditions.pop('datetime', None)

            if "number_of_data" in conditions.keys():
                number_of_data = conditions["number_of_data"][0]
                print number_of_data
                conditions.pop('number_of_data', None)
                datvalues = MongoConnection.find_lastest_data("DataValues",conditions,int(number_of_data))
            else:
                datvalues = MongoConnection.find_data("DataValues",conditions=conditions)

            serializer = serializers.DataValueSerializer(
                                instance=[ DataValues(**element) for element in datvalues],
                                many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
            parameters = request.data
            MongoConnection.insert_data("DataValues",parameters)
            return Response({"status":"ok"})