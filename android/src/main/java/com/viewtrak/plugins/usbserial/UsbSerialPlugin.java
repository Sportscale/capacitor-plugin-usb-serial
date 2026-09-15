package com.viewtrak.plugins.usbserial;

import android.hardware.usb.UsbDevice;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import org.json.JSONArray;

// Every plugin method below catches Throwable rather than Exception: UsbSerial
// signals all of its failures with java.lang.Error ("connection failed: device
// not found", "not connected", "connection lost", ...), and Error is a sibling
// of Exception under Throwable, not a subclass. Catching Exception let those
// escape the plugin method, and Bridge.callPluginMethod rethrows whatever it
// catches as a RuntimeException on the plugin HandlerThread -- so a missing
// scale killed the app instead of rejecting the call.
@CapacitorPlugin(name = "UsbSerial")
public class UsbSerialPlugin extends Plugin implements Callback {
    private UsbSerial implementation;

    @Override
    public void load() {
        super.load();
        implementation = new UsbSerial(getContext(), this);
    }

    @PluginMethod
    public void connectedDevices(PluginCall call) {
        try {
            JSObject jsObject = new JSObject();
            JSONArray devices = implementation.devices();
            jsObject.put("devices", devices);
            call.resolve(jsObject);
        } catch (Throwable e) {
            call.reject(e.toString());
        }
    }

    @PluginMethod
    public void openSerial(PluginCall call) {
        try {
            UsbSerialOptions settings = new UsbSerialOptions();

            if (call.hasOption("deviceId"))
                settings.deviceId = call.getInt("deviceId");

            if (call.hasOption("portNum"))
                settings.portNum = call.getInt("portNum");

            if (call.hasOption("baudRate"))
                settings.baudRate = call.getInt("baudRate");

            if (call.hasOption("dataBits"))
                settings.dataBits = call.getInt("dataBits");

            if (call.hasOption("stopBits"))
                settings.stopBits = call.getInt("stopBits");

            if (call.hasOption("parity"))
                settings.parity = call.getInt("parity");

            if (call.hasOption("dtr"))
                settings.dtr = call.getBoolean("dtr");

            if (call.hasOption("rts"))
                settings.rts = call.getBoolean("rts");

            if (call.hasOption("protocol")) {
                String protocolStr = call.getString("protocol");
                if ("RAW".equalsIgnoreCase(protocolStr)) {
                    settings.protocol = UsbSerialOptions.Protocol.RAW;
                } else {
                    settings.protocol = UsbSerialOptions.Protocol.NMEA;
                }
            }

            implementation.openSerial(settings);
            call.resolve(new JSObject());
        } catch (Throwable e) {
            call.reject(e.toString());
        }
    }

    @PluginMethod
    public void closeSerial(PluginCall call) {
        try {
            implementation.closeSerial();
            call.resolve(new JSObject());
        } catch (Throwable e) {
            call.reject(e.toString());
        }
    }

    @PluginMethod
    public void readSerial(PluginCall call) {
        try {
            JSObject jsObject = new JSObject();
            String result = implementation.readSerial();
            jsObject.put("data", result);
            call.resolve(jsObject);
        } catch (Throwable e) {
            call.reject(e.toString());
        }
    }

    @PluginMethod
    public void writeSerial(PluginCall call) {
        try {
            String data = call.hasOption("data") ? call.getString("data") : "";
            implementation.writeSerial(data);
            call.resolve(new JSObject());
        } catch (Throwable e) {
            call.reject(e.toString());
        }
    }

//    @Override
//    protected void handleOnResume() {
//        super.handleOnResume();
//        implementation.onResume();
//    }
//
//    @Override
//    protected void handleOnPause() {
//        implementation.onPause();
//        super.handleOnPause();
//    }

    @Override
    public void log(String TAG, String text) {
        JSObject ret = new JSObject();
        ret.put("text", text);
        ret.put("tag", TAG);
        notifyListeners("log", ret);
    }

    @Override
    public void connected(UsbDevice device) {
        JSObject ret = new JSObject();
        if (device != null) {
            ret.put("pid", device.getProductId());
            ret.put("vid", device.getVendorId());
            ret.put("did", device.getDeviceId());
        }
        notifyListeners("connected", ret);
    }

    @Override
    public void usbDeviceAttached(UsbDevice device) {
        JSObject ret = new JSObject();
        if (device != null) {
            ret.put("pid", device.getProductId());
            ret.put("vid", device.getVendorId());
            ret.put("did", device.getDeviceId());
        }
        notifyListeners("attached", ret);
    }

    @Override
    public void usbDeviceDetached(UsbDevice device) {
        JSObject ret = new JSObject();
        if (device != null) {
            ret.put("pid", device.getProductId());
            ret.put("vid", device.getVendorId());
            ret.put("did", device.getDeviceId());
        }
        notifyListeners("detached", ret);
    }

    @Override
    public void receivedData(String Data) {
        JSObject ret = new JSObject();
        ret.put("data", Data);
        notifyListeners("data", ret);
    }

    @Override
    public void error(Error error) {
        JSObject ret = new JSObject();
        ret.put("error", error.toString());
        notifyListeners("error", ret);
    }
}
