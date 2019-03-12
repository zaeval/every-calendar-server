import base64
import json
from datetime import timedelta, datetime

import pytz
import requests
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from everytime_parser import everytime
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.compat import authenticate


from rest_framework.authtoken.models import Token


# from authorize.authentication import TeacherAuthentication, VALIDATE_DAYS, StudentAuthentication, BothAuthentication
# from everyCalendarServer import settings
from django.contrib.contenttypes.models import ContentType

#
# @csrf_exempt
# @api_view(['GET', 'PUT'])
# def student(request, name=None):
#     if request.method == 'GET':
#         isSimple = request.GET.get('simply', False)
#         data = Student.objects.filter(name=name)
#         if len(data) > 0:
#             if isSimple:
#                 serialilzer = StudentSimpleSeriallizer(data[0])
#             else:
#                 serialilzer = StudentSeriallizer(data[0])
#
#             return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#         else:
#             return Response({'message': '해당학생을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'PUT':
#         data = Student.objects.filter(name__regex=r'^' + name + '$')
#         if len(data) > 0:
#             print("found")
#
#             data = data[0]
#         else:
#             print("savew")
#             data = Student.objects.create(name=name)
#             data.save()
#         serializer = StudentWriteSeriallizer(data, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(StudentSeriallizer(serializer.instance).data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET', 'POST', 'PUT'])
# def workspace(request, title=None):
#     if request.method == 'GET':
#         data = Workspace.objects.filter(title=title)
#         isSimple = request.GET.get('simply', False)
#
#         if len(data) > 0:
#             if isSimple:
#                 serialilzer = WorkspaceSimpleSeriallizer(data[0])
#             else:
#                 serialilzer = WorkspaceSeriallizer(data[0])
#
#             return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#         else:
#             return Response({'message': '해당워크스페이스를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'POST':
#         serializer = WorkspaceWriteSeriallizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(WorkspaceSeriallizer(serializer.instance).data, status=status.HTTP_201_CREATED)
#
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'PUT':
#         data = Workspace.objects.filter(title=title)
#         if len(data) > 0:
#             serialilzer = WorkspaceWriteSeriallizer(data[0], data=request.data)
#             if serialilzer.is_valid():
#                 serialilzer.save()
#                 return Response(WorkspaceSeriallizer(serialilzer.instance).data, status=status.HTTP_200_OK)
#
#         return Response({"message": "변경하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET', 'POST', 'PUT'])
# def exam(request, id=None):
#     if request.method == 'GET':
#         data = Exam.objects.filter(id=id)
#
#         if len(data) > 0:
#             serialilzer = ExamSeriallizer(data[0])
#
#             return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#         else:
#             return Response({'message': '해당 문제를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'POST':
#         serialilzer = ExamWriteSeriallizer(data=request.data)
#         if serialilzer.is_valid():
#             serialilzer.save()
#             return Response(serialilzer.data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'PUT':
#         data = Exam.objects.filter(id=id)
#         if len(data) > 0:
#             serialilzer = ExamWriteSeriallizer(data[0], data=request.data)
#             if serialilzer.is_valid():
#                 serialilzer.save()
#                 return Response(serialilzer.data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET', 'POST', 'PUT'])
# def question(request, id=None):
#     if request.method == 'GET':
#         data = Question.objects.filter(id=id)
#
#         if len(data) > 0:
#             serialilzer = QuestionSeriallizer(data[0])
#
#             return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#         else:
#             return Response({'message': '해당 문제를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'POST':
#         serialilzer = QuestionWriteSeriallizer(data=request.data)
#         if serialilzer.is_valid():
#             serialilzer.save()
#             return Response(QuestionSeriallizer(serialilzer.instance).data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'PUT':
#         data = Question.objects.filter(id=id)
#         if len(data) > 0:
#             serialilzer = QuestionWriteSeriallizer(data[0], data=request.data)
#             if serialilzer.is_valid():
#                 serialilzer.save()
#                 return Response(QuestionSeriallizer(serialilzer.instance).data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET', 'POST', 'PUT'])
# def block(request, id=None, child_id=None):
#     if request.method == 'GET':
#         data = SequenceBlock.objects.filter(id=id)
#
#         if len(data) > 0:
#             serialilzer = SequenceBlockSerializer(data[0])
#
#             return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#         else:
#             return Response({'message': '해당 문제를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'POST':
#         file_obj = request.data.get('file', None)
#         if file_obj != None:
#             return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#         serialilzer = BlockPolymorphicSerializer(data=request.data)
#         data = SequenceBlock.objects.filter(id=id)
#
#         if serialilzer.is_valid():
#             serialilzer.save()
#             if len(data) > 0:
#                 data[0].blocks.add(serialilzer.instance)
#                 data[0].save()
#             return Response(SequenceBlockSerializer(data[0]).data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'PUT':
#         data = SequenceBlock.objects.filter(id=id)
#         child = Block.objects.filter(id=child_id)
#         if len(data) > 0 and len(child) > 0:
#             print(request.data, child[0])
#             if request.data['resourcetype'] == 'TextBlock':
#                 child[0].text = request.data['text']
#                 child[0].save()
#             return Response(SequenceBlockSerializer(data[0]).data, status=status.HTTP_201_CREATED)
#         return Response({"message": "생성하는데 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET'])
# def exams(request):
#     if request.method == 'GET':
#         datas = Exam.objects.all()
#
#         serialilzer = ExamSeriallizer(datas, many=True)
#
#         return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(['GET'])
# def workspaces(request):
#     if request.method == 'GET':
#         datas = Workspace.objects.all()
#         serialilzer = WorkspaceSimpleSeriallizer(datas, many=True)
#
#         return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(['GET'])
# def tags(request):
#     if request.method == 'GET':
#         datas = Tag.objects.all()
#         serialilzer = TagSeriallizer(datas, many=True)
#
#         return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(['GET'])
# def students(request):
#     if request.method == 'GET':
#         datas = Student.objects.all()
#         serialilzer = StudentSimpleSeriallizer(datas, many=True)
#
#         return Response(serialilzer.data, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(['GET'])
# def result(request, student_name=None):
#     if request.method == 'GET':
#         data = Student.objects.filter(name=student_name)
#         if len(data) > 0:
#             serialilzer = StudentSeriallizer(data[0])
#         print(json.dumps(serialilzer.data))
#         return Response(visualiztion.result_chart_js(json.dumps(serialilzer.data)), status=status.HTTP_200_OK)
#
#

from authorize.serializers import UserSerializer

from restful.serializers import FriendSerializer


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        id = request.data.get("id")
        password = request.data.get("password")

        user = authenticate(username=id, password=password,request=request)
        if not user:
            return Response({"detail": "비밀번호나 아이디가 일치 하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(user,allow_null=True).data,status=HTTP_200_OK)

#
# @csrf_exempt
# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#
#         password = request.data.get("password", None)
#
#         email = request.data.get("email", None)
#
#         name = request.data.get("name", None)
#
#         gender = request.data.get("gender", None)
#         phone_number = request.data.get("phone_number", None)
#
#         if (id == None or password == None or
#                 email == None or name == None or gender == None
#                 or phone_number == None):
#             Response({"detail": "It's need more field"}, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = UserSerializer(data=request.data, method=request.method)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response({"success": "wait for permit"}, status=status.HTTP_201_CREATED)
#
#         return Response({"detail": "register failed"}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET'])
# @authentication_classes((TeacherAuthentication,))
# @permission_classes((IsAuthenticated,))
# def teacher(request):
#     if request.method == 'GET':
#         return Response({"detail": "wait for permit"}, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def home(request):
#     if request.method == 'GET':
#         return Response({"detail": "nice 2 meet u"}, status=status.HTTP_200_OK)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def tag(request):
#     if request.method == 'GET':
#         serializer = TagSeriallizer(Tag.objects.all(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = TagSeriallizer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def chapter(request):
#     if request.method == 'GET':
#         serializer = ChapterSeriallizer(Chapter.objects.all(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = ChapterSeriallizer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
#
# def subchapters(request):
#     if request.method == 'GET':
#         serializer = SubChapterSeriallizer(SubChapter.objects.all(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = SubChapterSeriallizer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def blocks(request):
#     if request.method == 'GET':
#         serializer = ProjectBlockSeriallizer(ProjectBlock.objects.all(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = ProjectBlockSeriallizer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def files(request):
#     if request.method == 'GET':
#         serializer = ProjectFileSeriallizer(ProjectFile.objects.all(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = ProjectFileSeriallizer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def project_simple(request):
#     if request.method == 'GET':
#         order = request.GET.get("order", "id")
#         filter = request.GET.get("filter", None)
#         if filter != None:
#             temp = {}
#             filter = filter.split("=")
#             for fi in range(0, len(filter), 2):
#                 temp[filter[fi]] = filter[fi + 1]
#             filter = temp
#         else:
#             filter = {'id__gte': 0}
#         num = int(request.GET.get("num", 100))
#
#         objs = ProjectInfo.objects.filter(**filter).order_by(order)[:num]
#         serializer = ProjectSimpleSeriallizer(objs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = ProjectSimpleWritableSeriallizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_200_OK)
#         print("simple",serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# def project(request):
#     if request.method == 'GET':
#         order = request.GET.get("order","id")
#         filter = request.GET.get("filter",None)
#         if filter != None:
#             temp = {}
#             filter = filter.split("=")
#             for fi in range(0,len(filter),2):
#                 temp[filter[fi]] = filter[fi+1]
#             filter = temp
#         else:
#             filter = {'id__gte':0}
#         num = int(request.GET.get("num",100))
#         objs = Project.objects.filter(**filter).order_by(order)[:num]
#         serializer = ProjectReadOnlySeriallizer(objs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'POST':
#         serializer = ProjectWritableSeriallizer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#         else:
#
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# def get_nextautoincrement(mymodel):
#     from django.db import connection
#     cursor = connection.cursor()
#     cursor.execute("SELECT Auto_increment FROM information_schema.tables WHERE table_name='%s';" % \
#                    mymodel._meta.db_table)
#     row = cursor.fetchone()
#     cursor.close()
#     return row[0]
#
#
# @csrf_exempt
# @api_view(['GET'])
# def get_pk(request):
#     if request.method == 'GET':
#
#         ret = {}
#         for ct in ContentType.objects.all():
#             m = ct.model_class()
#             ret[m.__name__] = get_nextautoincrement(m)
#         return Response(ret, status=status.HTTP_200_OK)
#
# @csrf_exempt
@api_view(['GET'])
def is_valid(request):
    if request.method == 'GET':
        etsid = request.headers.get('etsid')
        ses = requests.Session()
        ses.cookies.set('etsid',etsid)
        my_info = everytime.my_info(ses)
        print(my_info,etsid)
        if(my_info == None):
            return Response({'status':'false'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status':'true','user':my_info}, status=status.HTTP_200_OK)
@api_view(['GET'])
def friends(request):
    if request.method == 'GET':
        etsid = request.headers.get('etsid')
        ses = requests.Session()
        ses.cookies.set('etsid',etsid)
        friends = everytime.get_friend_list(ses)
        if(friends == None):
            return Response({'status':'false'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status':'true','friends':friends}, status=status.HTTP_200_OK)

@api_view(['POST'])
def union(request):
    if request.method == 'POST':
        etsid = request.headers.get('etsid')
        ses = requests.Session()
        ses.cookies.set('etsid', etsid)
        friends = FriendSerializer(data=request.data,many=True)

        if (not friends.is_valid()):
            return Response({'status': 'false'}, status=status.HTTP_400_BAD_REQUEST)

        friend_timetables = []
        for friend in friends.data:
            temp = everytime.get_timetable_user_id(ses, friend["userid"])
            friend_timetables.append(temp)

        union = everytime.union_time_table(friend_timetables)
        empty = everytime.empty_time_table(friend_timetables)

        return Response({'status': 'true', 'union': union,'empty':empty}, status=status.HTTP_200_OK)

@api_view(['POST'])
def sendRequest(request):
    if request.method == 'POST':
        etsid = request.headers.get('etsid')
        ses = requests.Session()
        ses.cookies.set('etsid', etsid)

        return Response({'detail':everytime.send_friend(ses, friend_id=request.data.get('friend_id'))}, status=status.HTTP_200_OK)


#
# @csrf_exempt
# @api_view(['POST'])
# def preEmail(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         email_obj, is_save = PreEmail.objects.get_or_create(email=email)
#
#         if is_save:
#             email_obj.save()
#             return Response({'status': True,'message':'등록이 정상적으로 완료되었습니다.'}, status=status.HTTP_200_OK)
#
#         return Response({'status': False,'message':'이미 등록된 이메일 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
#
#
#
