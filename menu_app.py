import rumps
import pyaudio
from audio_processor import AudioProcessor

class AudioSwitcherApp(rumps.App):
    def __init__(self):
        super(AudioSwitcherApp, self).__init__("🎛️ FixCenterLFE")
        self.p = pyaudio.PyAudio()
        self.processor = None
        self.input_device = None
        self.output_device = None
        self.is_processing = False
        self.refresh_devices()  # Initialize menu with empty device lists
        
    def enumerate_devices(self):
        """Returns tuple of (input_devices, output_devices)"""
        input_devices = []
        output_devices = []
        
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 2:
                input_devices.append((i, dev['name']))
            if dev['maxOutputChannels'] > 2:
                output_devices.append((i, dev['name']))
                
        return input_devices, output_devices

    def build_menu(self, input_devices, output_devices):
        """Builds menu structure from device lists"""
        self.menu.clear()  # Clear existing menu items first
                    
        # Build menu items in order
        menu_items = []
        
        # Add Input Devices section
        menu_items.append("Input Devices")
        for idx, name in input_devices:
            item = rumps.MenuItem(name, callback=lambda s, t='input', idx=idx: 
                                self.select_device(t, idx))
            item.state = idx == self.input_device
            menu_items.append(item)
        if not input_devices:
            menu_items.append(rumps.MenuItem("No input devices"))
            
        # Add separator
        menu_items.append(None)
        
        # Add Output Devices section
        menu_items.append("Output Devices")
        for idx, name in output_devices:
            item = rumps.MenuItem(name, callback=lambda s, t='output', idx=idx: 
                                self.select_device(t, idx))
            item.state = idx == self.output_device
            menu_items.append(item)
        if not output_devices:
            menu_items.append(rumps.MenuItem("No output devices"))
            
        # Add separator
        menu_items.append(None)

        # Determine processing state based on device selection
        processing_enabled = (self.input_device is not None and 
                            self.output_device is not None)
        
        # Add processing control
        processing_item = rumps.MenuItem(
            "Start Fixing" if not self.is_processing else "Stop Fixing",
            callback=self.toggle_processing
        )
        if not processing_enabled:
            processing_item.set_callback(None)
        menu_items.append(processing_item)
        
        self.menu = menu_items

    def refresh_devices(self):
        """Refreshes device lists and rebuilds menu"""
        input_devices, output_devices = self.enumerate_devices()
        self.build_menu(input_devices, output_devices)

    def select_device(self, device_type, device_id):
        """Handles selection of either input or output device"""
        if device_type == 'input':
            self.input_device = device_id
        else:
            self.output_device = device_id
            
        if self.is_processing:
            self.start_processing()
        self.refresh_devices()

    def toggle_processing(self, sender):
        if self.is_processing:
            self.stop_processing()
        else:
            self.start_processing()
        self.is_processing = not self.is_processing
        self.refresh_devices()

    def start_processing(self):
        if self.processor:
            self.processor.stop_stream()
        print(f"start_processing {self.input_device}, {self.output_device}")
        self.processor = AudioProcessor(self.input_device, self.output_device)
        self.processor.start_stream()

    def stop_processing(self):
        if self.processor:
            self.processor.stop_stream()
            self.processor = None

if __name__ == "__main__":
    app = AudioSwitcherApp()
    app.run()
