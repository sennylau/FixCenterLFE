from email.mime import audio
import pyaudio
import numpy as np

class AudioProcessor:
    def __init__(self, input_device=None, output_device=None):
        self.p = pyaudio.PyAudio()
        self.input_device = input_device
        self.output_device = output_device
        self.stream = None
        self.format = np.float32
        self.frames_per_buffer = 4096
        self.sample_rate = int(self.output_device.default_sample_rate)
        self.channels = int(self.output_device.max_output_channels)

        
    def start_stream(self):
        """Initialize audio stream with callback"""
        if not self.output_device:
            raise ValueError("Output device must be set")
            
        
        print(f"Starting stream - Input: {self.input_device}, "
              f"Output: {self.output_device}")
              
        def callback(in_data, frame_count, time_info, status):
            # Process audio here
            processed_data = self.process_audio(in_data)
            return (processed_data, pyaudio.paContinue)
            
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            output=True,
            frames_per_buffer=self.frames_per_buffer,
            stream_callback=callback,
            input_device_index=self.input_device.index if self.input_device else None,
            output_device_index=self.output_device.index
        )
    
    def process_audio(self, data):
        """Swap channels 3 and 4 in audio data"""
        audio_array = np.frombuffer(data, dtype=self.format).copy()
        # Create writable copy and reshape to (frames, channels)
        # frames = len(audio_array) // 6  # Assuming 6 channels
        # print(frames)
        # audio_array = audio_array.copy().reshape(frames, 6)
        audio_array = audio_array.reshape(self.frames_per_buffer, self.channels)
        
        # Swap channels 3 and 4 (0-indexed 2 and 3)
        audio_array[:, [2, 3]] = audio_array[:, [3, 2]]
        # Return as bytes
        return audio_array.tobytes()
    
    def stop_stream(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
