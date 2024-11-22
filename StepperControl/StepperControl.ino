#include <Stepper.h>

// 스텝 모터의 스텝 수 (28BYJ-48은 한 바퀴에 2048 스텝, Half-Step 모드)
#define STEPS_PER_REV 2048

// 1도당 필요한 스텝 수 계산
#define STEPS_PER_DEGREE (STEPS_PER_REV / 360.0)  // 한 바퀴(360도)를 2048로 나눈 값

// 스텝 모터 핀 설정 (8, 9, 10, 11)
Stepper myStepper(STEPS_PER_REV, 8, 10, 9, 11);
int stepMap[]={57, 57, 57, 57, 57, 57, 57, 57, 56, 56, 57, 57, 57, 57, 57, 57, 57, 57}
int stepIndex=0;
void setup() {
  // 모터 속도 설정 (10 RPM)
  myStepper.setSpeed(10);

  // 시리얼 통신 시작
  Serial.begin(9600);
}

void loop() {
  // 키보드 입력 확인
  if (Serial.available() > 0) {
    char input = Serial.read(); 
    
    if (input=='s'){
      myStepper.step(-stepMap[stepIndex]);
      stepIndex++;
    }
    if (input=='r'){
      myStepper.step(STEPS_PER_REV/2);
      stepIndex=0;
    }
  }
}
