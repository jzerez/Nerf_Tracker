#include <Servo.h>
Servo trackerX;

int list[100];
int listy[100];
int counter = 0;
int num_loops = 0;
int x_coor = 0;
int y_coor = 0;


void setup(){
  Serial.begin(9600);
  Serial.println("Hi there!");
  trackerX.attach(9);

  
}

void loop(){
  if (Serial.available() > 0){
    char new_char = Serial.read();
    
        
    new_char -= 48;
    switch (num_loops % 17) {
      case 4:
        x_coor += (new_char * 100);
        break;
      case 5:
        x_coor += (new_char * 10);
        break;
      case 6:
        x_coor += (new_char);
        list[counter % 100] = x_coor;
        
        //Serial.println(map(x_coor, 0, 640, 0, 180), DEC);
        trackerX.write(map(x_coor, 0, 640, 1, 179));
        delay(15);
        break;
      case 13:
        y_coor += (new_char * 100);
        break;
      case 14:
        y_coor += (new_char * 10);
        break;
      case 15:
        y_coor += (new_char);
        listy[counter % 100] = y_coor;
        break;
      case 16:
        counter++;
        x_coor = 0;
        y_coor = 0;
        
        break;
      default:
        break;
        
    }
    num_loops++;
  }
  /*
  if ((x_coor < 700) && (x_coor > 0)){
    Serial.println("gotem");
  }
  */
}
