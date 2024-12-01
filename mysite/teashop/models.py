from django.db import models

#For Shopping Mall Manager
class Menu(models.Model):
    MenuID = models.AutoField(primary_key=True)
    tealeaf = models.CharField(max_length=10)
    price = models.IntegerField(default=10000)
    origin = models.CharField(max_length=10)
    effID = models.IntegerField(default=0)
    #image column은 mysql workbench를 통해 직접 추가
    #image = models.ImageField()

#Menu테이블과 join으로 연결
class Effectiveness(models.Model):
    EffID = models.IntegerField(primary_key=True)
    explanation = models.CharField(max_length=20)
    ex_detail = models.CharField(max_length=100)

#For Customer
class MemberInfo(models.Model):
    memID = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=16, null=False)

###
#mysql workbench에서 직접 기본 생성된 id를 없애고
#이름을 basketID로 수정
#구조는 MenuID, basketID
### 
class OrderBasket(models.Model):
    basketID = models.ForeignKey(MemberInfo, on_delete=models.CASCADE, db_column='basketID')
    MenuID = models.IntegerField(default=0, unique=True)#join으로 menu table과 연결
    class Meta:
        managed : False
 
#주문 정보를 받기 위한 별도의 데이터베이스, 다른 테이블과 연결하지 않는다.    
class OrderInfo(models.Model):
    orderID = models.AutoField(primary_key=True)
    order_basketID = models.CharField(max_length=10)#OrderBasket의 basketID를 담는 column
    order_menuID = models.IntegerField()
    order_time = models.DateTimeField(auto_now_add=True)
    
###
# Menu table과 Effectiveness table을 join해 메뉴 page 구성
# 로그인 페이지에서 MemberInfo table 정보 입력
# MemberInfo.memID와 OrderBasket.basketID를 foreign key로 연결
# OrderInfo table에 OrderBasket table의 내용물 중 basketID와 MenuID를 받아 주문시간과 함께 저장
###