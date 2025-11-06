import { PluginListenerHandle } from '@capacitor/core';

export interface UsbSerialOptions {
  deviceId: number;
  portNum: number;
  baudRate?: number;
  dataBits?: number;
  stopBits?: number;
  parity?: number;
  dtr?: boolean;
  rts?: boolean;
  protocol?: 'NMEA' | 'RAW'; // Protocol mode: NMEA (line-based, default) or RAW (binary hex)
}

export interface UsbSerialDevice {
  pid: number;
  vid: number;
  did: number;
}

export interface UsbSerialPlugin {
  connectedDevices(): Promise<{ devices: [] }>;
  openSerial(options: UsbSerialOptions): Promise<void>;
  closeSerial(): Promise<void>;
  readSerial(): Promise<{ data: string }>;
  writeSerial(options: { data: string }): Promise<void>;

  addListener(
    eventName: 'log',
    listenerFunc: (data: { text: string; tag: string }) => void
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  addListener(
    eventName: 'connected',
    listenerFunc: (data: UsbSerialDevice) => void
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  addListener(
    eventName: 'attached',
    listenerFunc: (data: UsbSerialDevice) => void
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  addListener(
    eventName: 'detached',
    listenerFunc: (data: UsbSerialDevice) => void
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  addListener(
    eventName: 'data',
    listenerFunc: (data: { data: string }) => void
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
  addListener(
    eventName: 'error',
    listenerFunc: (data: { error: string }) => void
  ): Promise<PluginListenerHandle> & PluginListenerHandle;
}
