import argparse
import pyaudio
from audio_processor import AudioProcessor
from device import Device

def list_devices():
    """List available audio devices"""
    p = pyaudio.PyAudio()
    print("\nAvailable audio devices:")
    for i in range(p.get_device_count()):
        dev = Device(i, p.get_device_info_by_index(i))
        print(dev)
    p.terminate()

def main():
    parser = argparse.ArgumentParser(description='FixSurround Audio Channel Swapper')
    parser.add_argument('--list-devices', action='store_true', help='List audio devices')
    parser.add_argument('--input', type=int, help='Input device index')
    parser.add_argument('--output', type=int, help='Output device index')
    args = parser.parse_args()
    
    if args.list_devices:
        list_devices()
    else:
        p = pyaudio.PyAudio()
        try:
            input_device = Device(args.input, p.get_device_info_by_index(args.input))
            output_device = Device(args.output, p.get_device_info_by_index(args.output))

            processor = AudioProcessor(input_device, output_device)
            try:
                processor.start_stream()
                input("Press Enter to stop...")
            except KeyboardInterrupt:
                pass
            finally:
                processor.stop_stream()
        finally:
            p.terminate()

if __name__ == "__main__":
    main()
