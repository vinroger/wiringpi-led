
char switch_data [4]= {"00000000","00000000","0000000","00000000"};

void setup() {
  Serial.begin(9600);
  
}
void loop() {
  /*if (Serial.available() > 0) {
    //String data = switch_data;
    //Serial.print("You sent me: ");

  }*/
  String data1 = (switch_data[1]);
  //String data2 = switch_data[2];
  //String data3 = switch_data[3];
  //String data4 = switch_data[4];
  //String(data) = data1;
  Serial.println(data1);
}
