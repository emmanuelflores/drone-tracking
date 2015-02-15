void setup(){
Serial.begin(9600);
delay(5000);
}

void empty()
{
	while (Serial.available())
	{
		Serial.read();
	}
//Serial.println("Empty");
}


byte sendByte(byte value)
{
	Serial.write(value);
	return value;
}

void SendRSSI()
{
	sendByte(0x7E);
	sendByte(0x00);
	sendByte(0x10);

	long sum = 0;
// 7E 00 10 17 01 00 13 A2 00 40 BE 3B 99 FF FE 02 44 30 04 E9
	sum += sendByte(0x17);
	sum += sendByte(0x01);
	sum += sendByte(0x00);
	sum += sendByte(0x13);
	sum += sendByte(0xA2);
	sum += sendByte(0x00);
	sum += sendByte(0x40);
	sum += sendByte(0xBE);
	sum += sendByte(0x3B);
	sum += sendByte(0x99);
	sum += sendByte(0xFF);
	sum += sendByte(0xFE);
	sum += sendByte(0x02);
	sum += sendByte(0x44);
	sum += sendByte(0x30);
	sum += sendByte(0x04);

	sendByte( 0xFF - (sum & 0xFF));
//       Serial.println("Send");
	delay(200);
}

void loop()
{
	empty();
	SendRSSI();
	delay(10);
}

