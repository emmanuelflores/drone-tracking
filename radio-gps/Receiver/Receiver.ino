#include <SD.h>

void setup(){
Serial.begin(9600);
delay(5000);
}


int read_first_sample()
{
	int samples = 0;
	while (samples < 1) // 1 seconde wacht
	{
		delay(10);
		samples = Serial.available();
        }
	byte read = Serial.read();
	return read;
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

void atdb()
{
	sendByte(0x7E);
	sendByte(0x00);
	sendByte(0x04);

	long sum = 0;

	sum += sendByte(0x08);
	sum += sendByte(0x01);
	sum += sendByte('D');
	sum += sendByte('B');

	sendByte( 0xFF - (sum & 0xFF));
//       Serial.println("Send");
	delay(10);
}

void giveRSSI()
{
	int start_byte = read_first_sample(); // 7E = 126
//        Serial.println("Received");
	if (start_byte = 126)
	{
		read_first_sample(); // 00
		read_first_sample(); // 06 length
		read_first_sample(); // 88 AT response
		read_first_sample(); // frame ID 01
		read_first_sample(); // 'DB'
		read_first_sample();
		read_first_sample(); // Ok -status
		
		int value = Serial.read();
                Serial.println(value);
	}
	else
	{
	}
	delay(10);
}




void loop()
{
	empty();
	atdb();
	giveRSSI();
	delay(10);
}

