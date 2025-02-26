import numpy as np
from scipy.fft import fft, ifft
import wave

class PhaseCoding:
    def __init__(self):
        self.DELIMITER = "###"
        self.SEGMENT_LENGTH = 2048
        self.PHASE_SHIFT = np.pi/2
        
    def text_to_bits(self, text):
        """Chuyển text sang dãy bits"""
        bits = ''
        text_with_delimiter = text + self.DELIMITER
        for char in text_with_delimiter:
            bits += format(ord(char), '08b')
        print(f"Text to bits: {text} -> {bits}")
        return bits
    
    def bits_to_text(self, bits):
        """Chuyển dãy bits sang text"""
        text = ""
        if len(bits) % 8 != 0:
            bits = bits[:-(len(bits) % 8)]
            
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                try:
                    char = chr(int(byte, 2))
                    text += char
                except:
                    continue
        return text

    def hide_message(self, audio_path, message, output_path):
        """Giấu tin nhắn bằng phase coding"""
        try:
            print(f"\nHiding message: {message}")
            # Đọc file audio
            with wave.open(audio_path, 'rb') as wav:
                params = wav.getparams()
                frames = wav.readframes(wav.getnframes())
            
            # Chuyển frames thành mảng số
            audio_data = np.frombuffer(frames, dtype=np.int16)
            print(f"Audio length: {len(audio_data)} samples")
            
            # Chuyển message thành bits
            message_bits = self.text_to_bits(message)
            n_bits = len(message_bits)
            
            # Kiểm tra độ dài audio
            if len(audio_data) < n_bits * self.SEGMENT_LENGTH:
                return False, "Audio file too short for this message"
            
            # Xử lý từng segment
            modified_audio = audio_data.copy()
            for i in range(n_bits):
                start = i * self.SEGMENT_LENGTH
                end = start + self.SEGMENT_LENGTH
                segment = audio_data[start:end].astype(np.float64)
                
                # FFT
                spectrum = fft(segment)
                magnitude = np.abs(spectrum)
                phase = np.angle(spectrum)
                
                # Encode bit vào phase của frequency thấp
                if message_bits[i] == '1':
                    phase[1:5] = self.PHASE_SHIFT
                else:
                    phase[1:5] = -self.PHASE_SHIFT
                
                # IFFT
                modified_spectrum = magnitude * np.exp(1j * phase)
                modified_segment = np.real(ifft(modified_spectrum))
                
                # Normalize và chuyển về int16
                if np.max(np.abs(modified_segment)) > 0:
                    modified_segment = modified_segment * 32767 / np.max(np.abs(modified_segment))
                modified_audio[start:end] = modified_segment.astype(np.int16)
            
            # Lưu file mới
            with wave.open(output_path, 'wb') as wav:
                wav.setparams(params)
                wav.writeframes(modified_audio.tobytes())
            
            print("Message hidden successfully")
            return True, "Message hidden successfully"
            
        except Exception as e:
            print(f"Error hiding message: {str(e)}")
            return False, f"Error hiding message: {str(e)}"

    def extract_message(self, audio_path):
        """Trích xuất tin nhắn từ file audio"""
        try:
            print(f"\nExtracting from: {audio_path}")
            # Đọc file audio
            with wave.open(audio_path, 'rb') as wav:
                frames = wav.readframes(wav.getnframes())
            
            # Chuyển frames thành mảng số
            audio_data = np.frombuffer(frames, dtype=np.int16)
            print(f"Audio length: {len(audio_data)} samples")
            
            # Trích xuất bits
            extracted_bits = ''
            max_bits = 2000  # Tăng giới hạn bits
            
            for i in range(min(len(audio_data) // self.SEGMENT_LENGTH, max_bits)):
                start = i * self.SEGMENT_LENGTH
                end = start + self.SEGMENT_LENGTH
                segment = audio_data[start:end].astype(np.float64)
                
                # FFT
                spectrum = fft(segment)
                phase = np.angle(spectrum)
                
                # Decode bit từ phase trung bình của các frequency thấp
                avg_phase = np.mean(phase[1:5])
                bit = '1' if avg_phase > 0 else '0'
                extracted_bits += bit
                
                # Thử chuyển thành text sau mỗi byte
                if len(extracted_bits) % 8 == 0:
                    text = self.bits_to_text(extracted_bits)
                    print(f"Current text: {text}")
                    
                    # Kiểm tra nếu tìm thấy tin nhắn hoàn chỉnh
                    if self.DELIMITER in text:
                        message = text[:text.index(self.DELIMITER)]
                        print(f"Found message: {message}")
                        return True, message
                    
                    # Dừng nếu text quá dài (100 ký tự)
                    if len(text) > 100:
                        break
            
            print("No message found")
            return False, "No hidden message found"
            
        except Exception as e:
            print(f"Error extracting message: {str(e)}")
            return False, f"Error extracting message: {str(e)}"