package com.viewtrak.plugins.usbserial;

import com.hoho.android.usbserial.driver.UsbSerialPort;

public class UsbSerialOptions {
    public enum Protocol { NMEA, RAW }
    
    public int deviceId = 0;
    public int portNum = 0;
    public int baudRate = 9600;
    public int dataBits = UsbSerialPort.DATABITS_8;
    public int stopBits = UsbSerialPort.STOPBITS_1;
    public int parity = UsbSerialPort.PARITY_NONE;
    public boolean dtr = false;
    public boolean rts = false;
    public Protocol protocol = Protocol.NMEA; // default to existing NMEA behavior
}
