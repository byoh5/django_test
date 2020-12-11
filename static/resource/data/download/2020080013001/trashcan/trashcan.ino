/*
   RunCoding TrashCan
   주석을 지우지 말고 영상과 함께
   천천히 생각하며 코딩해보세요 ^^
*/

#include <Servo.h> //서보모터의 라이브러리 선언

Servo myservo;

// 초음파 센서의 연결 핀을 선언해준다. 
int trig = 13;
int echo = 10;

// 서보모터의 연결 핀을 선언해준다.
int servoPin = 9;

// no delete by runcoding
boolean eventOpen = 0;

// 서보모터의 강제 사용을 막기 위한 runcoding이 제공하는 코드
void eventTrigger()  // no delete by runcoding
{ 
  if (Serial.available() > 0)
  {
    // read the incoming byte:
    char incomingByte = Serial.read();

    if (incomingByte == 'o')
    {
      myservo.write(0);
      eventOpen = 1;
    }
    else if (incomingByte == 'c')
    {
      myservo.write(110);
      eventOpen = 0;
    }
    Serial.print(incomingByte);
  }
}

void setup() // setup()함수는 한번 수행된다.
{
  Serial.begin(9600); //시리얼 모니터를 사용하기 위한 선언

  pinMode(trig, OUTPUT); //trig의 pin에 mode를 OUTPUT으로 선언
  pinMode(echo, INPUT); //echo pin에 mode를 INPUT으로 선언

  myservo.attach(servoPin); //서보모터의 연결 pin을 서보객체에 연결
}

void loop() // loop()함수는 무한반복 수행된다.
{
  eventTrigger(); // no delete by runcoding

  digitalWrite(trig, LOW); //초기 설정
  digitalWrite(echo, LOW); //초기 설정

  // delay와 같은 기능이지만 조금 더 정밀한 조절이 가능함
  // 마이크로초 (us)
  delayMicroseconds(2);

  // 트리거 신호 발생
  digitalWrite(trig, HIGH);
  delayMicroseconds(10); // 10us = 0.000001 초
  digitalWrite(trig, LOW);
  
  if (eventOpen == 0) // no delete by runcoding
  {
    unsigned long duration = pulseIn(echo, HIGH);
    // 소문자 엘 , 대문자 아이

    long distance = ((340 * duration) / 10000) / 2;

    Serial.print(distance); //시리얼 모니터에 계산된 거리를 출력한다.
    Serial.println("cm"); // 시리얼 모니터에 거리의 단위를 cm로 출력한다.

    if () // 미션 1) 거리가(distance) 20cm 보다 작으면
    {
       // 미션 3) 0도로 열림
       // 미션 5)0.5초 기다림
    }
    // 미션 2) 아니면
    {
       // 미션 4) ?도로 닫힘 (상자의 각을 잘 생각해보자)
       // 미션 5) 0.5초 기다림
    }
  }
}

