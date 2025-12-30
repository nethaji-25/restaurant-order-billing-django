from rest_framework.decorators import api_view
from .models import Empdetails
from .Serialize import Serializer
from rest_framework.response import Response
from rest_framework import status



@api_view(['GET'])
def get_apis(request):
    e=Empdetails.objects.all()
    s=Serializer(e,many=True)
    return Response(s.data)

@api_view(['POST'])
def post_apis(request):
    s=Serializer(data=request.data)
    if request.method=='POST':
        if s.is_valid():
            s.save()
            return Response(s.data)

@api_view(['PUT'])
def put_apis(request,id):
    e=Empdetails.objects.get(id=id)
    s=Serializer(e,data=request.data)
    if s.is_valid():
        s.save()
        return Response(s.data)

@api_view(['DELETE'])
def delete_api(request,id):
    e=Empdetails.objects.get(id=id)
    e.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


