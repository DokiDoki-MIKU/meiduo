
from django.middleware import http
from django.shortcuts import render

from django.views import View
from apps.goods.models import SKU
from apps.users.models import User, Address
from django.http import JsonResponse
import re

# class UsernameCountView(View):
#     def get (self,request,username):
#         if not re.match('[a-zA-Z0-9_-]{5-20}',username):
#             return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
#
#         count=User.objects.filter(username=username).count()
#         return JsonResponse({'code':0,'count':count,'errmsg':'ok'})
#         pass
from utils.views import LoginRequiredJSONMixin


class UsernameCountView(View):

    def get(self,request,username):
        # 1.  接收用户名，对这个用户名进行一下判断
        # if not re.match('[a-zA-Z0-9_-]{5,20}',username):
        #     return JsonResponse({'code':200,'errmsg':'用户名不满足需求'})
        # 2.  根据用户名查询数据库
        count=User.objects.filter(username=username).count()
        # 3.  返回响应
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})


import json


def user(args):
    pass


class RegisterView(View):
    def post(self,request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)

        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        sms_code_client = body_dict.get('sms_code')

        redis_conn = get_redis_connection('code')
        sms_code_server = redis_conn.get(mobile)
        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # 对比用户输入的和服务端存储的短信验证码是否一致
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('[0-9A-Za-z]{8,20}',password):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[0-9A-Za-z]{8,20}',password2 ):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})
        if not re.match('1[3-9]\d{9}',mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        user=User.objects.create_user(username=username,password=password,mobile=mobile)



        from django.contrib.auth import login
        login(request,user)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})

class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'count': count})

# class LoginView(View):
#
#     def post(self,request):
#         # 1. 接收数据
#         data=json.loads(request.body.decode())
#         username=data.get('username')
#         password=data.get('password')
#         remembered=data.get('remembered')
#         # 2. 验证数据
#         if not all([username,password]):
#             return JsonResponse({'code':400,'errmsg':'参数不全'})
#
#
#         # 确定 我们是根据手机号查询 还是 根据用户名查询
#
#         # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
#         # 来影响authenticate 的查询
#         # authenticate 就是根据 USERNAME_FIELD 来查询
#         if re.match('1[3-9]\d{9}',username):
#             User.USERNAME_FIELD='mobile'
#         else:
#             User.USERNAME_FIELD='username'
#
#         # from django.contrib.auth import authenticate
#         # user=authenticate(username=username,password=password)
#         # if user is None:
#         #     return JsonResponse({'code':400,'errmsg':'账号或密码错误'})
#         from django.contrib.auth import login
#         login(request, user)
#         # 5. 判断是否记住登录
#         if remembered:
#             # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
#             request.session.set_expiry(None)
#
#         else:
#             # 不记住登录  浏览器关闭 session过期
#             request.session.set_expiry(0)
#
#         # 6. 返回响应
#         response = JsonResponse({'code': 0, 'errmsg': 'ok'})
#         # 为了首页显示用户信息
#         response.set_cookie('username', username)
#
#         return response
class LoginView(View):

    def post(self,request):
        # 1. 接收数据
        data=json.loads(request.body.decode())
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')
        # 2. 验证数据
        # if not all([username,password]):
        #     return JsonResponse({'code':400,'errmsg':'参数不全'})
        #
        #
        # # 确定 我们是根据手机号查询 还是 根据用户名查询
        #
        # # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
        # # 来影响authenticate 的查询
        # # authenticate 就是根据 USERNAME_FIELD 来查询
        # if re.match('1[3-9]\d{9}',username):
        #     User.USERNAME_FIELD='mobile'
        # else:
        #     User.USERNAME_FIELD='username'

        # 3. 验证用户名和密码是否正确
        # 我们可以通过模型根据用户名来查询
        # User.objects.get(username=username)


        # 方式2
        from django.contrib.auth import authenticate
        # authenticate 传递用户名和密码
        # 如果用户名和密码正确，则返回 User信息
        # 如果用户名和密码不正确，则返回 None
        user=authenticate(username=username,password=password)

        if user is None:
            return JsonResponse({'code':400,'errmsg':'账号或密码错误'})

        # 4. session
        from django.contrib.auth import login
        login(request,user)
        # 5. 判断是否记住登录
        if remembered:
            # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
            request.session.set_expiry(None)

        else:
            #不记住登录  浏览器关闭 session过期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code':0,'errmsg':'ok'})
        # 为了首页显示用户信息
        response.set_cookie('username',username)

        from apps.carts.untils import merge_cookies_to_redis
        response = merge_cookies_to_redis(request,response)

        return response

from django.contrib.auth import logout
class LogoutView(View):
    def delete(self,request):
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')

        return response


from django.contrib.auth.mixins import LoginRequiredMixin
class CenterView(LoginRequiredMixin,View):
    def get(selfself,request):
        info_data = {
            'username':request.user.username,
            'email':request.user.email,
            'mobile':request.user.mobile,
            'email_active':request.user.email_active,


        }
        return JsonResponse({'code':0,'errmsg':'ok','info_data':info_data})
#授权码VMPXPUFURZOZQZAQ
# class EmailView(LoginRequiredMixin,View):
#
#     def put(self,request):
#         data=json.loads(request.body.decode())
#         email=data.get('email')
#

#         from django.core.mail import send_mail
#         subject='美多商城激活邮件'
#
#         message='abc'
#
#         from_email='美多商城<ciyuanjiaoyisuo@163.com>'
#
#         recipient_list=['2310105913@qq.com','m15203321882@163.com']
#
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=from_email,
#             recipient_list=recipient_list
#         )
#
#
#         return JsonResponse({'code':0,'errmsg':'ok'})
class EmailView(LoginRequiredJSONMixin,View):

    def put(self,request):
        # 1. 接收请求
        #ｐｕｔ post －－－　ｂｏdy
        data=json.loads(request.body.decode())
        # 2. 获取数据
        email=data.get('email')
        # 验证数据
        # 正则　
        if not email:
            return JsonResponse({'code': 400, 'errmsg': '缺少email参数'})
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return JsonResponse({'code': 400, 'errmsg': '请输入正确的邮箱'})
        #
        # 3. 保存邮箱地址
        user=request.user
        # user / request.user 就是　登录用户的　实例对象
        # user --> User
        user.email=email
        user.save()
        # 4. 发送一封激活邮件
        # 一会单独讲发送邮件
        from django.core.mail import send_mail
        # subject, message, from_email, recipient_list,
        # subject,      主题
        subject='美多商城激活邮件'
        # message,      邮件内容
        message=""
        # from_email,   发件人
        from_email='美多商城<ciyuanjiaoyisuo@163.com>'
        # recipient_list, 收件人列表
        recipient_list = ['ciyuanjiaoyisuo@163.com','2310105913@qq.com']
        from apps.users.utils import generic_email_verify_token
        token=generic_email_verify_token(request.user.id)
        verify_url='http://www.meiduo.site:8080/success_verify_email.html?token=%s'%token
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        # html_message='点击按钮进行激活 <a href=http://www.itcast.cn/?token=%s>激活</a>'%token
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_message
        #           )
        from celery_tasks.email.tasks import celery_send_email
        celery_send_email.delay(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )

        # 5. 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})


class EmailVerifyView(View):
    def put(self,request):
        params=request.Get
        token=params.get('token')

        if  token is None:
            return JsonResponse({'code':400,'errmsg':'参数缺失'})
        from apps.users.utils import check_verify_token
        user_id=check_verify_token(token)
        if user_id is None:
            return JsonResponse({'code':400,'errmsg':'参数错误'})

        user=User.objects.get(id=user_id)
        user.email_active=True
        user.save()
        return JsonResponse({'code':0,'errmsg':'ok'})

class AddressCreateView(LoginRequiredJSONMixin, View):

    def post(self, request):
        # 1.接收请求
        data = json.loads(request.body.decode())
        # 2.获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user
        # 验证参数 （省略）
        # 2.1 验证必传参数
        # 2.2 省市区的id 是否正确
        # 2.3 详细地址的长度
        # 2.4 手机号
        # 2.5 固定电话
        # 2.6 邮箱

        # 3.数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        address_dict = {
            'id': address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 4.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})

class AddressView(LoginRequiredJSONMixin,View):

    def get(self,request):
        # 1.查询指定数据
        user=request.user
        # addresses=user.addresses

        addresses=Address.objects.filter(user=user,is_deleted=False)
        # 2.将对象数据转换为字典数据
        address_list=[]
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
        # 3.返回响应
        return JsonResponse({'code':0,'errmsg':'ok','addresses':address_list})

class DefaultAddressView(LoginRequiredJSONMixin, View):
    def put(self,request,address_id):

        address = Address.objects.get(id=address_id)

        request.user.default_address = address
        request.user.save()
        return JsonResponse({'code': 0, 'errmsg': '设置成功'})

class UpdateTitleAddressView(LoginRequiredJSONMixin, View):
    def put(self,request,address_id):
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

class ChangePasswordView(LoginRequiredMixin, View):
    #"""修改密码"""

  def put(self, request):
        """实现修改密码逻辑"""
        # 接收参数
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        if not all([old_password,new_password, new_password2]):
            return JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({'code': 400,'errmsg': '原始密码不正确'})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400,'errmsg': '密码最少8位,最长20位'})

        if new_password != new_password2:
            return JsonResponse({'code': 400,'errmsg': '两次输入密码不一致'})

        request.user.set_password(new_password)
        request.user.save()

        logout(request)

        response = JsonResponse({'code': 0,
                                      'errmsg': 'ok'})

        response.delete_cookie('username')

        # # 响应密码修改结果：重定向到登录界面
        return response

from django_redis import get_redis_connection
class UserHistoryView(LoginRequiredMixin,View):
    def post(self,request):
        user=request.user
        data=json.loads(request.body.decode())

        sku_id = data.get('sku_id')
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'没有此商品'})

        redis_cil=get_redis_connection('history')
        redis_cil.lrem('history_%s'%user.id,sku_id)
        redis_cil.lpush('history_%s'%user.id,sku_id)
        redis_cil.ltrim('history_%s'%user.id,0,4)

        return JsonResponse({'code':0,'errmsg':'ok'})


    def get(self,request):
        redis_cli=get_redis_connection('history')
        ids=redis_cli.lrange('history_%s'%request.user.id,0,4)
        history_list=[]
        for sku_id in ids:
            sku=SKU.objects.get(id=sku_id)
            history_list.append({
                'id':sku.id,
                'name':sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        return JsonResponse({'code': 0, 'errmsg': 'OK', 'sku': history_list})