
char my2dArray[4][8]={{'0','0','0','0','0','0','0','0'},
                       {'0','0','0','0','0','0','0','0'},
                        {'0','0','0','0','0','0','0','0'},
                         {'0','0','0','0','0','0','0','0'}};
String Data;
bool received = false;
String msg = "";

void setup() {
  Serial.begin(9600);

}

void Dataline()
{
        Data = "([";
      for(int j=0; j<4;j++){
        for (int i=0; i <7; i++){
        String data = String(my2dArray[j][i]);
        Data = Data + data + ",";
        } 
        String data = String(my2dArray[j][7]);
        Data = Data + data;
        Data = (j!=3)? Data + "] [": Data;
      }
        
        Data = Data + "])";
        received = true;

      
      
      
      
  
}

void switchinput()
{
  Serial.println("Getting Data");
  if (my2dArray[0][7] == '0'){
  for(int i=0; i <8; i++){
    my2dArray[0][i] = '1';
    }
  }
  else if (my2dArray[0][7] == '1'){
  for(int i=0; i <8; i++){
    my2dArray[0][i] = '0';
    }
  }
  
}




void loop() {
  if (Serial.available() > 0) {
  
   msg = Serial.readStringUntil('\n');

  }

  if (msg == "send") {

    msg = "";

    switchinput();
    
    Dataline();
    if (received){
      received = false;
    Serial.println(Data);
    Serial.println("sent");
    }
    delay(500);

  }
  
}
