import { registerPlugin } from '@capacitor/core';

import type { UsbSerialPlugin } from './definitions';

const UsbSerial = registerPlugin<UsbSerialPlugin>('UsbSerial', {
  web: () => import('./web.js').then((m) => new m.UsbSerialWeb()),
});

export * from './definitions.js';
export { UsbSerial };
