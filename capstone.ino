#include <Servo.h>

// Servo objects
Servo servo_left;
Servo servo_right;
Servo piston;

// Input pins yellow, orange, red
const int pin_balut = 7;
const int pin_bugok = 8;
const int pin_penoy = 9;

// Servo pins
const int servo_right_pin = 4;
const int servo_left_pin = 5;
const int piston_pin = 3;

// Timing
unsigned long currentMillis;
unsigned long pushTimer = 0;

// States
enum State { IDLE, BALUT, BUGOK, PENOY };
State currentState = IDLE;

enum SubState { INIT, PUSH_START, PUSH_MID, PUSH_END };
SubState subState = INIT;

void setup() {
  servo_right.attach(servo_right_pin);
  servo_left.attach(servo_left_pin);
  piston.attach(piston_pin);

  pinMode(pin_balut, INPUT);
  pinMode(pin_bugok, INPUT);
  pinMode(pin_penoy, INPUT);

  pinMode(pinDone, OUTPUT);
  digitalWrite(pinDone, LOW);

  centerServo();
  piston.write(30); // Initial piston position
}

void loop() {
  currentMillis = millis();

  // Only change state if we're not in the middle of a sequence
  if (currentState == IDLE) {
    if (digitalRead(pin_balut) == HIGH) {
      currentState = BALUT;
      subState = INIT;
    } else if (digitalRead(pin_bugok) == HIGH) {
      currentState = BUGOK;
      subState = INIT;
    } else if (digitalRead(pin_penoy) == HIGH) {
      currentState = PENOY;
      subState = INIT;
    }
  }

  switch (currentState) {
    case BALUT:
      handleBalut();
      break;
    case BUGOK:
      handleBugok();
      break;
    case PENOY:
      handlePenoy();
      break;
    case IDLE:
    default:
      // Do nothing
      break;
  }
}

void handleBalut() {
  switch (subState) {
    case INIT:
      turnLeft();
      subState = PUSH_START;
      pushTimer = currentMillis;
      break;

    case PUSH_START:
      if (currentMillis - pushTimer >= 1000) {
        piston.write(30);
        pushTimer = currentMillis;
        subState = PUSH_MID;
      }
      break;

    case PUSH_MID:
      if (currentMillis - pushTimer >= 100) {
        piston.write(0);
        pushTimer = currentMillis;
        subState = PUSH_END;
      }
      break;

    case PUSH_END:
      if (currentMillis - pushTimer >= 100) {
        piston.write(30);
        centerServo();
        currentState = IDLE;
      }
      break;
  }
}

void handleBugok() {
  switch (subState) {
    case INIT:
      centerServo();
      subState = PUSH_START;
      pushTimer = currentMillis;
      break;

    case PUSH_START:
      if (currentMillis - pushTimer >= 1000) {
        piston.write(30);
        pushTimer = currentMillis;
        subState = PUSH_MID;
      }
      break;

    case PUSH_MID:
      if (currentMillis - pushTimer >= 100) {
        piston.write(0);
        pushTimer = currentMillis;
        subState = PUSH_END;
      }
      break;

    case PUSH_END:
      if (currentMillis - pushTimer >= 100) {
        piston.write(30);
        centerServo();
        currentState = IDLE;
      }
      break;
  }
}

void handlePenoy() {
  switch (subState) {
    case INIT:
      turnRight();
      subState = PUSH_START;
      pushTimer = currentMillis;
      break;

    case PUSH_START:
      if (currentMillis - pushTimer >= 1000) {
        piston.write(30);
        pushTimer = currentMillis;
        subState = PUSH_MID;
      }
      break;

    case PUSH_MID:
      if (currentMillis - pushTimer >= 100) {
        piston.write(0);
        pushTimer = currentMillis;
        subState = PUSH_END;
      }
      break;

    case PUSH_END:
      if (currentMillis - pushTimer >= 100) {
        piston.write(30);
        centerServo();
        currentState = IDLE;
      }
      break;
  }
}

void ledOn() {

  }
void turnLeft() {
  servo_left.write(90);
  servo_right.write(90);
}

void turnRight() {
  servo_left.write(0);
  servo_right.write(0);
}

void centerServo() {
  servo_left.write(25);
  servo_right.write(60);
}
