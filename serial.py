import serial
from serial.tools import list_ports
import time


# for p in list_ports.comports():
#     print('Description =>', p.description)
#     print('HWID =>', p.hwid)

SERIAL_PORT = 'COM7'
BAUD_RATE = 9600
TIMEOUT = 1
DATA_BITS = 8
STOP_BITS = serial.STOPBITS_ONE
PARITY = serial.PARITY_NONE
HANDSHAKING = False

# ESC (0x1B or ASCII 27) is used to indicate a command following [4].
ESC = 0x1B

# Command for PC Initiated Request Current Values/Settings (Read Weight) [7, 8]
# ESC + R + ESC + E
# R = 0x52, E = 0x45
WEIGHT_REQUEST_COMMAND = bytes([ESC, 0x52, ESC, 0x45])

# Command for Diagnostics Request (e.g., Diagnose Battery, to test connection) [9, 10]
# ESC + ABAT + ESC + E
DIAGNOSTIC_COMMAND = bytes([ESC, 0x41, 0x42, 0x41, 0x54, ESC, 0x45])


def connect_and_test_scale():
    """Attempts to connect to the serial port and verifies communication using a diagnostic command."""
    print("Attempting to initialize serial connection...")
    
    try:
        # Initialize serial connection parameters [3, 6]
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=DATA_BITS,
            stopbits=STOP_BITS,
            parity=PARITY,
            timeout=TIMEOUT
        )
        
        if ser.is_open:
            print(f"Connection established successfully on {SERIAL_PORT} (9600 baud, N81) [3, 6].")
            
            # Flush buffers before sending a command
            ser.flushInput()
            ser.flushOutput()

            # Test connection using the diagnostic command (Request Battery Status: ESC ABAT ESC E) [10]
            print("\nSending diagnostic request (ESC ABAT ESC E) to test communication integrity...")
            ser.write(DIAGNOSTIC_COMMAND)
            time.sleep(0.3) # Wait for response
            
            response = ser.read(15) # Read up to 15 bytes for the expected response length
            
            if response:
                # Expected response format starts with ESC Z... [9, 10]
                response_str = response.decode('ascii', errors='ignore').strip()
                print(f"Diagnostic response received: {response_str}")

                # Check if the scale is performing properly (Z000 response) or if the battery is low (E4U/E4L) [5, 9, 11]
                if 'Z000' in response_str:
                    print("Scale diagnostics indicate proper performance (Z000 received) [9]. Connection test successful.")
                    return ser
                elif 'ZE4U' in response_str or 'ZE4L' in response_str:
                    print(f"Scale diagnostics indicate low battery ({response_str} received) [5, 11]. Connection confirmed.")
                    return ser
                else:
                    print(f"Received unknown diagnostic response: {response_str}. Connection may be poor or protocol configuration is incorrect.")
                    ser.close()
                    return None
            else:
                print("No response received from the scale after diagnostic command. Connection failed.")
                ser.close()
                return None
                
        else:
            print(f"Failed to open port {SERIAL_PORT}.")
            return None

    except serial.SerialException as e:
        print(f"Failed to connect to scale on {SERIAL_PORT}. Error: {e}")
        print("Please ensure the port name is correct and the cable is connected [3, 5].")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during connection: {e}")
        return None

def read_weight_from_scale(ser):
    """Sends the weight request command and attempts to parse the weight from the response."""
    
    if not ser or not ser.is_open:
        print("Serial connection is not active.")
        return

    print("\nRequesting weight data (ESC R ESC E)...")
    try:
        # Clear buffers and send the weight request command
        ser.flushInput()
        ser.write(WEIGHT_REQUEST_COMMAND)
        time.sleep(0.3) 
        
        # Read the response (Weight response packet includes ESC, R, W, value, N, units, E) [7, 9]
        # We read a large buffer to ensure the entire packet is captured.
        response = ser.read(30)
        
        if response:
            response_str = response.decode('ascii', errors='ignore')
            print(f"Raw data received: {response_str.strip()}")
            
            # The weight data format is typically Wnnn.n [9]. We look for 'W' followed by digits/decimal.
            
            # Simple parsing: Find 'W' and extract the weight segment
            if 'W' in response_str:
                start_index = response_str.find('W') + 1
                
                # The weight is a numeric value (e.g., W02000 means 200.0) [9].
                # We need to find the next control character or space to delineate the weight value.
                
                # Assuming the weight value follows W and is fixed or ends before the next ESC or N.
                # We look for the numeric value following 'W'
                
                # A robust parsing approach using regex might be necessary, but based purely on sources:
                # Wnnn.n (where nnn.n is the weight) [9]
                
                import re
                weight_match = re.search(r'W(\-?\d+\.?\d+)', response_str)
                
                if weight_match:
                    raw_weight_value = weight_match.group(1).lstrip('0')
                    
                    # Determine units based on the response format (N followed by m or c) [9, 12]
                    units = ''
                    if 'Nm' in response_str:
                        units = 'kg (Metric)'
                    elif 'Nc' in response_str:
                        units = 'lb (Constitutional)'
                    else:
                        units = 'UNKNOWN UNIT'
                        
                    print(f"\n=======================================================")
                    print(f"Successfully read weight: {raw_weight_value} {units}")
                    print(f"=======================================================")
                
                # If scale is overloaded or underloaded, '999.99' might be returned [9]
                elif '999.99' in response_str:
                     print("\nWeight Reading Status: Scale is overloaded or underloaded [9].")
                     
                else:
                    print("Could not extract numerical weight data from response.")
            
            else:
                print("Error: 'W' indicator not found in response. Scale might be busy or sent an error.")
                
        else:
            print("No weight data response received.")

    except Exception as e:
        print(f"An error occurred while reading or parsing weight: {e}")

if __name__ == '__main__':
    # 1. Test Connection
    scale_connection = connect_and_test_scale()
    
    # 2. Read Weight
    if scale_connection:
        try:
            read_weight_from_scale(scale_connection)
        finally:
            scale_connection.close()
            print("\nSerial port closed.")





