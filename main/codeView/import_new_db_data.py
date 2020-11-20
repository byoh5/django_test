# 새로 디비를 구성할때 사용 될 초기 데이터
# 절대 active database에 올리면 안되고, 바뀐 디비 테이블이 있다면 늘 update가 필요함
# 2020.11.04 - agnes


from main.models import *
import bcrypt

myclass_list_info = MyClassListTB(user_id=pay_info[0].pay_email, prd=order_info[0].prd,
                                  pay_num=pay_info[0].pay_num,
                                  expire_time=timezone.now())

def register():
    password_encrypt = bcrypt.hashpw("runcoding!".encode('utf-8'), bcrypt.gensalt())
    RegisterTB_new = RegisterTB(regi_email="runcoding@naver.com", regi_name="런코딩", regi_phone="07078678866", regi_receiver1_add01="16692",
                                regi_receiver1_add02="경기도 수원시 영통구", regi_receiver1_add03="런코딩회사", regi_pass=password_encrypt.decode('utf-8'),
                                level=100, stime=timezone.now())
    RegisterTB_new.save()

def prd():
    PrdTB_new_1 = PrdTB(prd_code="2020080013001", title="[아두이노 + AI] 스마트 휴지통", title2="스마트 휴지통", title3="[아두이노 + AI]",
                      img="/static/resource/img/Trashcan/trashcan_main.jpg", gif="/static/resource/img/Trashcan/trashcan_gif.gif",
                      period=3, class_count=13, price=45000, option1="아두이노 보드, 러닝캠", option1_price=0, goal="서보모터/초음파센서/러닝캠/러닝봇",
                      keyword="아두이노")

    PrdTB_new_1.save()

    PrdTB_new_2 = PrdTB(prd_code="2020080023001", title="[엠블럭 + AI] 스마트 휴지통", title2="스마트 휴지통", title3="[엠블럭 + AI]",
                        img="/static/resource/img/Trashcan/trashcan_main.jpg",
                        gif="/static/resource/img/Trashcan/trashcan_gif.gif",
                        period=3, class_count=12, price=45000, option1="아두이노 보드, 러닝캠", option1_price=0,
                        goal="서보모터/초음파센서/러닝캠/러닝봇",
                        keyword="엠블럭")

    PrdTB_new_2.save()

    ItemCommonTB_new_1 = ItemCommonTB(item_code="arduino_intall", title="아두이노 설치 [환경구축]", time="3:54",
                                      data="arduino_install.mp4")
    ItemCommonTB_new_1.save()

    ItemCommonTB_new_2 = ItemCommonTB(item_code="arudino_variable", title="변수 [이론/문법]", time="7:48",
                                      data="arduino_variable.mp4")
    ItemCommonTB_new_2.save()

    ItemCommonTB_new_3 = ItemCommonTB(item_code="arduino_operator", title="연산자 기초 [이론/문법]", time="9:08",
                                      data="arduino_operator.mp4")
    ItemCommonTB_new_3.save()

    ItemCommonTB_new_4 = ItemCommonTB(item_code="arduino_serial", title="시리얼 모니터 [이론/문법]", time="1:49",
                                      data="arduino_serial.mp4")
    ItemCommonTB_new_4.save()

    ItemCommonTB_new_5 = ItemCommonTB(item_code="arduino_function", title="함수 [이론/문법]", time="7:32",
                                      data="arduino_function.mp4")
    ItemCommonTB_new_5.save()

    ItemCommonTB_new_6 = ItemCommonTB(item_code="arduino_if", title="함수 [이론/문법]", time="14:47",
                                      data="arduino_if.mp4")
    ItemCommonTB_new_6.save()


    # 커리큘럼
    ItemTB_new_1 = ItemTB(prd=PrdTB_new_1, common=ItemCommonTB_new_1, title="아두이노 설치 [환경구축]", time="3:54",
                          data="arduino_install.mp4", order=1, downdata="driver_install_arduino.pptx",
                          downdata_name="드라이버 설치")
    ItemTB_new_1.save()