# usb-serial-plugin

This plugin can be used for reading data from other device over the usb channel

## Install

```bash
npm install usb-serial-plugin
npx cap sync
```

## API

<docgen-index>

* [`connectedDevices()`](#connecteddevices)
* [`openSerial(...)`](#openserial)
* [`closeSerial()`](#closeserial)
* [`readSerial()`](#readserial)
* [`writeSerial(...)`](#writeserial)
* [`addListener('log', ...)`](#addlistenerlog-)
* [`addListener('connected', ...)`](#addlistenerconnected-)
* [`addListener('attached', ...)`](#addlistenerattached-)
* [`addListener('detached', ...)`](#addlistenerdetached-)
* [`addListener('data', ...)`](#addlistenerdata-)
* [`addListener('error', ...)`](#addlistenererror-)
* [Interfaces](#interfaces)

</docgen-index>

<docgen-api>
<!--Update the source file JSDoc comments and rerun docgen to update the docs below-->

### connectedDevices()

```typescript
connectedDevices() => Promise<{ devices: []; }>
```

**Returns:** <code>Promise&lt;{ devices: []; }&gt;</code>

--------------------


### openSerial(...)

```typescript
openSerial(options: UsbSerialOptions) => Promise<void>
```

| Param         | Type                                                          |
| ------------- | ------------------------------------------------------------- |
| **`options`** | <code><a href="#usbserialoptions">UsbSerialOptions</a></code> |

--------------------


### closeSerial()

```typescript
closeSerial() => Promise<void>
```

--------------------


### readSerial()

```typescript
readSerial() => Promise<{ data: string; }>
```

**Returns:** <code>Promise&lt;{ data: string; }&gt;</code>

--------------------


### writeSerial(...)

```typescript
writeSerial(options: { data: string; }) => Promise<void>
```

| Param         | Type                           |
| ------------- | ------------------------------ |
| **`options`** | <code>{ data: string; }</code> |

--------------------


### addListener('log', ...)

```typescript
addListener(eventName: 'log', listenerFunc: (data: { text: string; tag: string; }) => void) => Promise<PluginListenerHandle> & PluginListenerHandle
```

| Param              | Type                                                           |
| ------------------ | -------------------------------------------------------------- |
| **`eventName`**    | <code>'log'</code>                                             |
| **`listenerFunc`** | <code>(data: { text: string; tag: string; }) =&gt; void</code> |

**Returns:** <code>Promise&lt;<a href="#pluginlistenerhandle">PluginListenerHandle</a>&gt; & <a href="#pluginlistenerhandle">PluginListenerHandle</a></code>

--------------------


### addListener('connected', ...)

```typescript
addListener(eventName: 'connected', listenerFunc: (data: UsbSerialDevice) => void) => Promise<PluginListenerHandle> & PluginListenerHandle
```

| Param              | Type                                                                           |
| ------------------ | ------------------------------------------------------------------------------ |
| **`eventName`**    | <code>'connected'</code>                                                       |
| **`listenerFunc`** | <code>(data: <a href="#usbserialdevice">UsbSerialDevice</a>) =&gt; void</code> |

**Returns:** <code>Promise&lt;<a href="#pluginlistenerhandle">PluginListenerHandle</a>&gt; & <a href="#pluginlistenerhandle">PluginListenerHandle</a></code>

--------------------


### addListener('attached', ...)

```typescript
addListener(eventName: 'attached', listenerFunc: (data: UsbSerialDevice) => void) => Promise<PluginListenerHandle> & PluginListenerHandle
```

| Param              | Type                                                                           |
| ------------------ | ------------------------------------------------------------------------------ |
| **`eventName`**    | <code>'attached'</code>                                                        |
| **`listenerFunc`** | <code>(data: <a href="#usbserialdevice">UsbSerialDevice</a>) =&gt; void</code> |

**Returns:** <code>Promise&lt;<a href="#pluginlistenerhandle">PluginListenerHandle</a>&gt; & <a href="#pluginlistenerhandle">PluginListenerHandle</a></code>

--------------------


### addListener('detached', ...)

```typescript
addListener(eventName: 'detached', listenerFunc: (data: UsbSerialDevice) => void) => Promise<PluginListenerHandle> & PluginListenerHandle
```

| Param              | Type                                                                           |
| ------------------ | ------------------------------------------------------------------------------ |
| **`eventName`**    | <code>'detached'</code>                                                        |
| **`listenerFunc`** | <code>(data: <a href="#usbserialdevice">UsbSerialDevice</a>) =&gt; void</code> |

**Returns:** <code>Promise&lt;<a href="#pluginlistenerhandle">PluginListenerHandle</a>&gt; & <a href="#pluginlistenerhandle">PluginListenerHandle</a></code>

--------------------


### addListener('data', ...)

```typescript
addListener(eventName: 'data', listenerFunc: (data: { data: string; }) => void) => Promise<PluginListenerHandle> & PluginListenerHandle
```

| Param              | Type                                              |
| ------------------ | ------------------------------------------------- |
| **`eventName`**    | <code>'data'</code>                               |
| **`listenerFunc`** | <code>(data: { data: string; }) =&gt; void</code> |

**Returns:** <code>Promise&lt;<a href="#pluginlistenerhandle">PluginListenerHandle</a>&gt; & <a href="#pluginlistenerhandle">PluginListenerHandle</a></code>

--------------------


### addListener('error', ...)

```typescript
addListener(eventName: 'error', listenerFunc: (data: { error: string; }) => void) => Promise<PluginListenerHandle> & PluginListenerHandle
```

| Param              | Type                                               |
| ------------------ | -------------------------------------------------- |
| **`eventName`**    | <code>'error'</code>                               |
| **`listenerFunc`** | <code>(data: { error: string; }) =&gt; void</code> |

**Returns:** <code>Promise&lt;<a href="#pluginlistenerhandle">PluginListenerHandle</a>&gt; & <a href="#pluginlistenerhandle">PluginListenerHandle</a></code>

--------------------


### Interfaces


#### UsbSerialOptions

| Prop           | Type                         |
| -------------- | ---------------------------- |
| **`deviceId`** | <code>number</code>          |
| **`portNum`**  | <code>number</code>          |
| **`baudRate`** | <code>number</code>          |
| **`dataBits`** | <code>number</code>          |
| **`stopBits`** | <code>number</code>          |
| **`parity`**   | <code>number</code>          |
| **`dtr`**      | <code>boolean</code>         |
| **`rts`**      | <code>boolean</code>         |
| **`protocol`** | <code>'NMEA' \| 'RAW'</code> |


#### PluginListenerHandle

| Prop         | Type                                      |
| ------------ | ----------------------------------------- |
| **`remove`** | <code>() =&gt; Promise&lt;void&gt;</code> |


#### UsbSerialDevice

| Prop      | Type                |
| --------- | ------------------- |
| **`pid`** | <code>number</code> |
| **`vid`** | <code>number</code> |
| **`did`** | <code>number</code> |

</docgen-api>
