from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class SMSCodeView(APIView):
    def get(self, request, mobile):
        """

        :param request:
        :param mobile:
        :return:
        """
        return Response({"message": "ok"})
