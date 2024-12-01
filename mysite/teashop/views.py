from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from .forms import SignupForm
from .models import *
from django.db import connection
from django.contrib import messages
# Create your views here.
def mainpage_before(request):
    sort_by = request.GET.get('sort', 'tealeaf')
    menus = Menu.objects.all().order_by(sort_by)
    return render(request, "teashop/mainpage_before.html", { 'menus': menus, 'sort_by': sort_by })

def mainpage_after(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = MemberInfo.objects.get(memID=user_id)
        sort_by = request.GET.get('sort', 'tealeaf')
        menus = Menu.objects.all().order_by(sort_by)
        count = OrderBasket.objects.count()
        return render(request, 'teashop/mainpage_after.html', {'user': user, 'menus': menus, 'sort_by': sort_by, 'count': count})
    else:
        #로그인하지 않은 상태에서 이 페이지에 접근한 경우
        return redirect('/login')
    
###카트에 데이터 처리하는 로직
def addcart(request):
    if request.method == 'POST':  # POST 요청만 처리
        data = json.loads(request.body.decode('utf-8'))
        menu_id = data.get('menu_id')# 메뉴 ID
        user_id = request.session.get('user_id')  # 세션에서 사용자 ID 가져오기

        if not user_id:
            return JsonResponse({'message': '로그인이 필요합니다.'}, status=400)

        try:
            # OrderBasket에 데이터 추가
            user = MemberInfo.objects.get(memID=user_id)
            OrderBasket.objects.create(basketID=user, MenuID=menu_id)
            return JsonResponse({'success': True, 'message': '메뉴가 카트에 추가되었습니다.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': '잘못된 요청입니다.'}, status=405)

def detail(request):
    #데이터베이스 Menu-Eff join하고 데이터 불러오기-using raw sql
    query = """
        SELECT m.MenuID, m.tealeaf, m.price, m.origin, e.explanation, e.ex_detail
        FROM teashop_menu m
        INNER JOIN teashop_effectiveness e ON m.effID = e.EffID
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    menuID = int(request.GET.get('menuID'))
    for row in results:
        if row[0] == menuID:
            menu = row
            break
    return render(request, 'teashop/detail.html', {'menu': menu})

def login(request):
    if request.method == 'POST':
        ID = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = MemberInfo.objects.get(memID=ID)
            if user.password == password:  # 평문 비밀번호 비교
                # 로그인 성공 처리 (직접 세션 관리 필요)
                request.session['user_id'] = user.memID
                return JsonResponse({'message': '로그인 성공!'}, status=200)
            else:
                return JsonResponse({'message': '잘못된 비밀번호입니다.'}, status=400)
        except MemberInfo.DoesNotExist:
            return JsonResponse({'message': '존재하지 않는 계정입니다.'}, status=400)

    return render(request, 'teashop/login.html')

#로그아웃(세션 flushing) 과정 구현
def logout(request):
    if request.method == 'POST':
        request.session.flush()  # 세션 삭제 (로그아웃 처리)
        return JsonResponse({'message': '로그아웃 성공!'}, status=200)
    return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=400)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            ID = form.cleaned_data['ID']
            password = form.cleaned_data['password']
            MemberInfo.objects.create(memID=ID, password=password)
            messages.success(request, '회원가입이 완료되었습니다!')
            return redirect('login')
        else:
            messages.error(request, '입력 정보를 확인해주세요.')
    return render(request, 'teashop/signup.html')

def cart(request):
    count = OrderBasket.objects.count()
    ###orderbasket의 menuID를 기준으로 Menu table과 join
    query = """
        SELECT 
            teashop_menu.MenuID, 
            teashop_menu.tealeaf, 
            teashop_menu.price, 
            teashop_menu.origin, 
            teashop_menu.effID,
            teashop_orderbasket.basketID
        FROM 
            teashop_menu
        JOIN 
            teashop_orderbasket ON teashop_menu.MenuID = teashop_orderbasket.MenuID;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        
    carts = []
    for result in results:
        tealeaf, price, origin = result[1], result[2], result[3]
        carts.append((tealeaf, price, origin))
    return render(request, 'teashop/cart.html', {'carts': carts, 'count': count})

from django.db import connection

def order(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        # basket_items = OrderBasket.objects.filter(basketID=user_id)
        # OrderBasket에서 basketID와 MenuID를 직접 쿼리
        query = """
            SELECT basketID, MenuID FROM teashop_orderbasket WHERE basketID = %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            basket_items = cursor.fetchall()
        
        if not basket_items:
            return JsonResponse({'message': '장바구니에 담은 것이 없습니다.'}, status=400)
        
        try:
            for item in basket_items:
                OrderInfo.objects.create(order_basketID=item[0], order_menuID=item[1])
            
            # 주문이 완료되면 장바구니 비우기
            delete_query = """
                DELETE FROM teashop_orderbasket WHERE basketID = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(delete_query, [user_id])

            return JsonResponse({'success': True, 'message': '주문이 완료되었습니다.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return redirect('/mainpage_after')
