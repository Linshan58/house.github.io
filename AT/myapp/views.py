from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from pymongo import MongoClient
from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm




# @首頁 與基本設定相關-------------------------------------------------------------------------------------------------------------------------------------
# 連接 MongoDB
client = MongoClient('mongodb://localhost:27017')
def home(request):  
   cities = {
        'taipei': {
            'name': '台北市',
            'images': ['taipei1.jpg', 'taipei2.jpg', 'taipei3.jpg']
        },
        'kaohsiung': {
            'name': '高雄市',
            'images': ['kaohsiung1.jpg', 'kaohsiung2.jpg']
        },
        # 其他城市資料...
    }
   # 檢查 session 中是否存在 username
   username = request.session.get('username', None)
   return render(request, 'home.html', {'username': username,'cities': cities})

# @會員相關-------------------------------------------------------------------------------------------------------------------------------------

# 連接IH資料庫中的會員資料
db = client.IH.members
#最基本的註冊  @ 沒問題V1
def register(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        name = request.POST.get('name')
        member_type = request.POST.get('member_type')  # 從表單中獲取會員類型

        # 驗證數據
        if not account or not password or not name:
            error_message = "請填寫所有欄位"
            return render(request, 'register.html', {'error_message': error_message})

        # 檢查帳號是否已存在
        if db.find_one({'account': account}):
            error_message = "帳號已被使用"
            return render(request, 'register.html', {'error_message': error_message})

        # 獲取下一個可用的 member_id
        last_member = db.find_one(sort=[('member_id', -1)])
        if last_member:
            next_member_id = last_member['member_id'] + 1
        else:
            next_member_id = 1

        # 保存數據到 MongoDB
        member_data = {
            'member_id': next_member_id,
            'account': account,
            'password': password,
            'name': name,
            'favorites': [],
            'member_type': member_type  # 將會員類型加入數據
        }
        db.insert_one(member_data)

        # 重定向到登錄頁面或其他頁面
        return redirect('login')

    return render(request, 'register.html')

#最基本的登入  @ 沒問題V1    
def login_view(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        # 檢查帳號和密碼是否匹配
        user = db.find_one({'account': account, 'password': password})
        if user:
            # 登入成功，將帳號存儲在 session 中
            request.session['account'] = account
            request.session['username'] = user['name']  # 将用户的姓名存储在会话中
            return redirect('home')
        else:
            # 登入失敗，返回登入頁面，並顯示錯誤訊息
            error_message = "無效的帳號或密碼"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout_view(request):
   # 刪除 session 中的 username
   del request.session['username']
   # 執行其他登出邏輯
   return redirect('login')

# @商品相關-------------------------------------------------------------------------------------------------------------------------------------

# 設計連結商品資料庫
db2= client.IH.house_products

#顯示商品列表  @ 沒問題V1
def product_list(request):
    products = list(db2.find())  # 从 MongoDB 中获取商品数据并转换为列表
    paginator = Paginator(products, 5)  # 每页显示5个商品

    page_number = request.GET.get('page')  # 从GET请求中获取页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的商品对象

    return render(request, 'product_list.html', {'page_obj': page_obj})


# 访问 admin 数据库中的 members 集合
db = client.IH.members

def member_favorites(request):
    # 获取当前用户的账号
    account = request.session.get('account')
    if account:
        # 从 MongoDB 中获取当前用户的收藏信息
        member = db.find_one({'account': account}, {'_id': 0, 'favorites': 1})
        if member:
            favorites = member.get('favorites', [])
            return render(request, 'member_favorites.html', {'favorites': favorites})
        else:
            error_message = "用户不存在"
            return render(request, 'member_favorites.html', {'error_message': error_message})
    else:
        return redirect('login')  # 如果用户未登录，重定向到登录页面

def all_favorites(request):
    # 获取所有会员的收藏内容
    #值则指示是否包含该字段（1 表示包含，0 表示排除）。在这个特定的查询中：
    all_members = list(db.find({}, {'_id': 0, 'name': 1, 'favorites': 1}))
    
    # 将收藏内容传递给模板进行渲染
    return render(request, 'all_favorites.html', {'all_members': all_members})

