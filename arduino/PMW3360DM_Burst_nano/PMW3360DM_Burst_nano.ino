#include <SPI.h>
#include <avr/pgmspace.h>

// Configurations
// The CPI value should be in between 100 -- 12000
#define CPI       12000

// Registers
#define Product_ID  0x00
#define Revision_ID 0x01
#define Motion  0x02
#define Delta_X_L 0x03
#define Delta_X_H 0x04
#define Delta_Y_L 0x05
#define Delta_Y_H 0x06
#define SQUAL 0x07
#define Raw_Data_Sum  0x08
#define Maximum_Raw_data  0x09
#define Minimum_Raw_data  0x0A
#define Shutter_Lower 0x0B
#define Shutter_Upper 0x0C
#define Control 0x0D
#define Config1 0x0F
#define Config2 0x10
#define Angle_Tune  0x11
#define Frame_Capture 0x12
#define SROM_Enable 0x13
#define Run_Downshift 0x14
#define Rest1_Rate_Lower  0x15
#define Rest1_Rate_Upper  0x16
#define Rest1_Downshift 0x17
#define Rest2_Rate_Lower  0x18
#define Rest2_Rate_Upper  0x19
#define Rest2_Downshift 0x1A
#define Rest3_Rate_Lower  0x1B
#define Rest3_Rate_Upper  0x1C
#define Observation 0x24
#define Data_Out_Lower  0x25
#define Data_Out_Upper  0x26
#define Raw_Data_Dump 0x29
#define SROM_ID 0x2A
#define Min_SQ_Run  0x2B
#define Raw_Data_Threshold  0x2C
#define Config5 0x2F
#define Power_Up_Reset  0x3A
#define Shutdown  0x3B
#define Inverse_Product_ID  0x3F
#define LiftCutoff_Tune3  0x41
#define Angle_Snap  0x42
#define LiftCutoff_Tune1  0x4A
#define Motion_Burst  0x50
#define LiftCutoff_Tune_Timeout 0x58
#define LiftCutoff_Tune_Min_Length  0x5A
#define SROM_Load_Burst 0x62
#define Lift_Config 0x63
#define Raw_Data_Burst  0x64
#define LiftCutoff_Tune2  0x65

const int ncs = 10;  // This is the SPI "slave select" pin that the sensor is hooked up to. big one 10

byte initComplete = 0;
bool inBurst = false;

// Be sure to add the SROM file into this sketch via "Sketch->Add File"
extern const unsigned short firmware_length;
extern const unsigned char firmware_data[];

void setup() {
  Serial.begin(9600);
  while (!Serial); // Wait for serial to be available (for Leonardo/Micro)

  pinMode(ncs, OUTPUT);
  digitalWrite(ncs, HIGH); // Ensure CS pin is high

  SPI.begin();
  SPI.setDataMode(SPI_MODE3);
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV8); // Reduce SPI speed

  Serial.println("Starting...");

  performStartup();

  delay(1000);

  Serial.println("Initialization Complete");
}

void adns_com_begin() {
  digitalWrite(ncs, LOW);
}

void adns_com_end() {
  digitalWrite(ncs, HIGH);
}

byte adns_read_reg(byte reg_addr) {
  adns_com_begin();

  SPI.transfer(reg_addr & 0x7F);
  delayMicroseconds(35); // tSRAD
  byte data = SPI.transfer(0);

  delayMicroseconds(1); // tSCLK-NCS for read operation is 120ns
  adns_com_end();
  delayMicroseconds(19); //  tSRW/tSRR (=20us) minus tSCLK-NCS

  return data;
}

void adns_write_reg(byte reg_addr, byte data) {
  adns_com_begin();

  SPI.transfer(reg_addr | 0x80);
  SPI.transfer(data);

  delayMicroseconds(20); // tSCLK-NCS for write operation
  adns_com_end();
  delayMicroseconds(100); // tSWW/tSWR (=120us) minus tSCLK-NCS
}

void adns_upload_firmware() {
  Serial.println("Uploading firmware...");

  adns_write_reg(Config2, 0x00);
  adns_write_reg(SROM_Enable, 0x1d);

  delay(10);

  adns_write_reg(SROM_Enable, 0x18);

  adns_com_begin();
  SPI.transfer(SROM_Load_Burst | 0x80);
  delayMicroseconds(15);

  for (int i = 0; i < firmware_length; i++) {
    unsigned char c = (unsigned char)pgm_read_byte(firmware_data + i);
    SPI.transfer(c);
    delayMicroseconds(15);
  }

  adns_read_reg(SROM_ID);
  adns_write_reg(Config2, 0x00);

  adns_com_end();

  Serial.println("Firmware uploaded");
}

void setCPI(int cpi) {
  int cpival = constrain((cpi / 100) - 1, 0, 0x77);

  adns_com_begin();
  adns_write_reg(Config1, cpival);
  adns_com_end();

  Serial.print("DPI set to ");
  Serial.println(cpi);
}

void performStartup() {
  adns_com_end(); // ensure that the serial port is reset
  adns_com_begin(); // ensure that the serial port is reset
  adns_com_end(); // ensure that the serial port is reset
  
  adns_write_reg(Shutdown, 0xb6); // Shutdown first
  delay(300);
  
  adns_com_begin(); // drop and raise ncs to reset spi port
  delayMicroseconds(40);
  adns_com_end();
  delayMicroseconds(40);
  
  adns_write_reg(Power_Up_Reset, 0x5a); // force reset
  delay(50); // wait for it to reboot
  
  // read registers 0x02 to 0x06 (and discard the data)
  adns_read_reg(Motion);
  adns_read_reg(Delta_X_L);
  adns_read_reg(Delta_X_H);
  adns_read_reg(Delta_Y_L);
  adns_read_reg(Delta_Y_H);
  
  adns_upload_firmware();
  delay(10);

  setCPI(CPI);
  Serial.println("Optical Chip Initialized");
}

void dispRegisters() {
  int oreg[7] = {
    0x00, 0x3F, 0x2A, 0x02
  };
  char* oregname[] = {
    "Product_ID", "Inverse_Product_ID", "SROM_Version", "Motion"
  };
  byte regres;

  digitalWrite(ncs, LOW);

  for (int rctr = 0; rctr < 4; rctr++) {
    SPI.transfer(oreg[rctr]);
    delay(1);
    Serial.println("---");
    Serial.println(oregname[rctr]);
    Serial.println(oreg[rctr], HEX);
    regres = SPI.transfer(0);
    Serial.println(regres, BIN);
    Serial.println(regres, HEX);
    delay(1);
  }
  digitalWrite(ncs, HIGH);
}

void loop() {
  byte burstBuffer[12];
  
  adns_com_begin();
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE3));

  SPI.transfer(Motion_Burst);
  delayMicroseconds(35); // waits for tSRAD

  SPI.transfer(burstBuffer, 12); // read burst buffer
  delayMicroseconds(1); // tSCLK-NCS for read operation is 120ns

  SPI.endTransaction();

  int motion = (burstBuffer[0] & 0x80) > 0;
  int xl = burstBuffer[2];
  int xh = burstBuffer[3];
  int yl = burstBuffer[4];
  int yh = burstBuffer[5];
  
  int x = xh << 8 | xl;
  int y = yh << 8 | yl;
    
  adns_com_end();

  if (motion) {
    Serial.print("Motion detected: ");
    Serial.print("X: ");
    Serial.print(x);
    Serial.print(" Y: ");
    Serial.println(y);
  }

  delayMicroseconds(800);
}
