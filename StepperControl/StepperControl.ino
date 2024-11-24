#include <Stepper.h>

// 스텝 모터의 스텝 수 (28BYJ-48은 한 바퀴에 2048 스텝, Half-Step 모드)
#define STEPS_PER_REV 2048

// 1도당 필요한 스텝 수 계산
#define STEPS_PER_DEGREE (STEPS_PER_REV / 360.0)  // 한 바퀴(360도)를 2048로 나눈 값

// 스텝 모터 핀 설정 (8, 9, 10, 11)
Stepper myStepper(STEPS_PER_REV, 8, 10, 9, 11);

int stepMap[]={57, 57, 57, 57, 57, 57, 57, 57, 56, 56, 57, 57, 57, 57, 57, 57, 57, 57};
int stepIndex=0;
bool s90 = true;
void setup() {
  // 모터 속도 설정 (10 RPM)
  myStepper.setSpeed(10);

  // 시리얼 통신 시작
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read(); 
    
    // one step
    if (input=='s'){
      myStepper.step(STEPS_PER_REV+stepMap[stepIndex]);
      stepIndex++;
    }
    // reset
    if (input=='r'){
      myStepper.step(STEPS_PER_REV/2);
      stepIndex=0;
    }
    // backword
    if(input=='b'){
      myStepper.step(-STEPS_PER_REV-stepMap[stepIndex]);
      stepIndex--;
    }
    // for setting
    if (input=='i'){
      myStepper.step(1);
    }
    
    // rotate all with extends
    if (input=='g'){
      if(s90){
        myStepper.step(STEPS_PER_REV/4);
        s90 = false;
      }
      else{
        myStepper.step(3*STEPS_PER_REV/4+stepMap[stepIndex]);
        ++stepIndex;
        s90 = true;
      }
    }
    // Status print
    Serial.println(stepIndex*10-90);
  }
}
