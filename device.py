class Device:
    def __init__(self, index, device_info):
        self.index = index
        self.name = device_info['name']
        self.max_input_channels = device_info['maxInputChannels']
        self.max_output_channels = device_info['maxOutputChannels']
        self.default_sample_rate = device_info['defaultSampleRate']
        
    def __str__(self):
        return f"{self.index}: {self.name} (in: {self.max_input_channels}, out: {self.max_output_channels}, rate: {self.default_sample_rate})"
