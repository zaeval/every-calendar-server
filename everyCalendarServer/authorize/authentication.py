import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from everytime_parser import everytime

UserModel = get_user_model()

VALIDATE_DAYS = 30
class AuthBackend(ModelBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get_by_natural_key(username)

        except Exception as e:

            UserModel().set_password(password)

            ses, req = everytime.login(username, password)

            if len(ses.cookies.items()) > 0:

                my_info = everytime.my_info(ses)
                my_info['etsid'] = ses.cookies.items()[0][1]
                my_info['id']=username
                my_info['password']=password

                user = UserModel.objects.create_user(**my_info)
                user.save()
                return user

            else:
                everytime.register(username, password, username+"@naver.com", username, username)
                ses, req = everytime.login(username, password)

                if len(ses.cookies.items()) > 0:

                    my_info = everytime.my_info(ses)
                    my_info['etsid'] = ses.cookies.items()[0][1]
                    my_info['id'] = username
                    my_info['password'] = password

                    user = UserModel.objects.create_user(**my_info)
                    user.save()
                    return user

                else:
                    return None

        else:
            user.check_password(password)
            if user.check_password(password):
                if user.is_staff:
                    return user
                else:
                    ses = requests.Session()
                    ses.cookies.set('etsid',user.etsid)
                    my_info = everytime.my_info(ses)
                    if my_info == None:
                        ses, req = everytime.login(username, password)
                        my_info = everytime.my_info(ses)
                        my_info['etsid'] = ses.cookies.items()[0][1]
                        UserModel.objects.filter(pk=username).update(**my_info)
                    return user