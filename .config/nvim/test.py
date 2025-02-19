import sys
import subprocess 
from pathlib import Path

from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq

class KeyInterceptor:
    def __init__(self):
        self.local_display = display.Display()
        self.record_display = display.Display()
        self.pressed_keys = set()
        self.keymap = {v: k for k, v in XK.__dict__.items()}

    def lookup_keysym(self, keysym):
        return self.keymap.get(keysym, None)

    def record_callback(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print("Received swapped endian data, not supported.")
            return
        if not len(reply.data) or reply.data[0] < 2:
            return
        
        data = reply.data
        event, keycode = data[1], data[2]
        keysym = self.local_display.keycode_to_keysym(keycode, 0)
        key = self.lookup_keysym(keysym)

        if event == X.KeyPress:
            self.pressed_keys.add(key)
            print(f"Key Pressed: {key}, Current Pressed: {self.pressed_keys}")
        elif event == X.KeyRelease:
            self.pressed_keys.discard(key)
            print(f"Key Released: {key}, Current Pressed: {self.pressed_keys}")

    def start_intercepting(self):
        ctx = self.record_display.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.KeyRelease),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }]
        )
        self.record_display.record_enable_context(ctx, self.record_callback)
        self.record_display.record_free_context(ctx)

    def run(self):
        try:
            print("Starting key interception...")
            self.start_intercepting()
        except KeyboardInterrupt:
            print("Stopping key interception.")
            self.record_display.close()

if __name__ == "__main__":
    interceptor = KeyInterceptor()
    interceptor.run()

