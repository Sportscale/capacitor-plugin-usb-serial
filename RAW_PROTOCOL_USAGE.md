# RAW Protocol Mode Usage Guide

## Overview

The plugin now supports two protocol modes:
- **NMEA** (default): Line-based text protocol with automatic `\r\n` line endings
- **RAW**: Binary protocol for raw RS232 communication (like your Python scale code)

## Key Differences

### NMEA Mode (Default)
- Automatically adds `\r\n` to all writes
- Buffers incoming data until newline character
- Returns complete lines via data listener
- Best for: GPS devices, text-based protocols

### RAW Mode
- Sends/receives raw binary data as hex strings
- No automatic line endings added
- Flushes buffers before each write
- Returns data immediately without buffering
- Best for: Scales, binary protocols, custom RS232 devices

## Usage Example (Scale Communication)

```typescript
import { UsbSerial } from 'capacitor-plugin-usb-serial';

// 1. Open connection with RAW protocol
await UsbSerial.openSerial({
  deviceId: deviceId,
  portNum: 0,
  baudRate: 9600,
  dataBits: 8,
  stopBits: 1,
  parity: 0,
  protocol: 'RAW'  // Enable RAW mode
});

// 2. Listen for incoming data
UsbSerial.addListener('data', (response) => {
  console.log('Received hex data:', response.data);
  // response.data is a hex string like "1B5A303030301B45"
});

// 3. Send commands as hex strings (no line endings added)
// Example: ESC ABAT ESC E (diagnostic command)
const ESC = '1B';
const DIAGNOSTIC_COMMAND = ESC + '41424154' + ESC + '45';
await UsbSerial.writeSerial({ data: DIAGNOSTIC_COMMAND });

// Example: ESC R ESC E (read weight command)
const WEIGHT_REQUEST = ESC + '52' + ESC + '45';
await UsbSerial.writeSerial({ data: WEIGHT_REQUEST });
```

## Converting Python Commands to Plugin

Your Python code:
```python
ESC = 0x1B
DIAGNOSTIC_COMMAND = bytes([ESC, 0x41, 0x42, 0x41, 0x54, ESC, 0x45])
ser.write(DIAGNOSTIC_COMMAND)
```

Becomes:
```typescript
const ESC = '1B';
const DIAGNOSTIC_COMMAND = ESC + '41424154' + ESC + '45';
await UsbSerial.writeSerial({ data: DIAGNOSTIC_COMMAND });
```

## Hex String Format

- All data in RAW mode uses **uppercase hex strings without separators**
- Each byte is represented by 2 hex characters
- Example: `0x1B 0x52 0x1B 0x45` → `'1B521B45'`

## Helper Function for Byte Arrays

```typescript
function bytesToHex(bytes: number[]): string {
  return bytes.map(b => b.toString(16).toUpperCase().padStart(2, '0')).join('');
}

// Usage:
const ESC = 0x1B;
const command = bytesToHex([ESC, 0x52, ESC, 0x45]);
await UsbSerial.writeSerial({ data: command });
```

## Parsing Responses

```typescript
function hexToBytes(hex: string): number[] {
  const bytes = [];
  for (let i = 0; i < hex.length; i += 2) {
    bytes.push(parseInt(hex.substr(i, 2), 16));
  }
  return bytes;
}

UsbSerial.addListener('data', (response) => {
  const bytes = hexToBytes(response.data);
  const text = String.fromCharCode(...bytes);
  console.log('As text:', text);
  
  // Check for specific responses
  if (text.includes('Z000')) {
    console.log('Scale diagnostics OK');
  }
});
```

## Complete Scale Example

```typescript
// Constants matching your Python code
const ESC = '1B';
const WEIGHT_REQUEST_COMMAND = ESC + '52' + ESC + '45';
const DIAGNOSTIC_COMMAND = ESC + '41424154' + ESC + '45';

// Open connection
await UsbSerial.openSerial({
  deviceId: deviceId,
  portNum: 0,
  baudRate: 9600,
  dataBits: 8,
  stopBits: 1,
  parity: 0,
  protocol: 'RAW'
});

// Listen for responses
UsbSerial.addListener('data', (response) => {
  const bytes = hexToBytes(response.data);
  const text = String.fromCharCode(...bytes);
  console.log('Scale response:', text);
  
  // Parse weight data
  if (text.includes('W')) {
    const match = text.match(/W(\-?\d+\.?\d+)/);
    if (match) {
      const weight = match[1];
      const units = text.includes('Nm') ? 'kg' : 'lb';
      console.log(`Weight: ${weight} ${units}`);
    }
  }
});

// Test connection with diagnostic
await UsbSerial.writeSerial({ data: DIAGNOSTIC_COMMAND });

// Wait a bit, then request weight
setTimeout(async () => {
  await UsbSerial.writeSerial({ data: WEIGHT_REQUEST_COMMAND });
}, 500);
```

## Backward Compatibility

Existing NMEA code continues to work without changes:
```typescript
// This still works as before (NMEA is default)
await UsbSerial.openSerial({
  deviceId: deviceId,
  portNum: 0,
  baudRate: 9600
});

// Sends "HELLO\r\n"
await UsbSerial.writeSerial({ data: 'HELLO' });
```

## Troubleshooting

1. **No response from device**: Make sure you're using `protocol: 'RAW'`
2. **Corrupted data**: Verify hex strings are uppercase and properly formatted
3. **Timing issues**: Add small delays between commands (like Python's `time.sleep(0.3)`)
4. **Buffer issues**: RAW mode automatically flushes buffers before each write
