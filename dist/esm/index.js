import { registerPlugin } from '@capacitor/core';
const UsbSerial = registerPlugin('UsbSerial', {
    web: () => import('./web.js').then((m) => new m.UsbSerialWeb()),
});
export * from './definitions.js';
export { UsbSerial };
//# sourceMappingURL=index.js.map