import numpy as np
import wave
import os

class LSBAudio:
    def __init__(self):
        self.DELIMITER = "###"
        
    def text_to_bits(self, text):
        """Chuyển text sang dãy bits"""
        bits = ''
        text_with_delimiter = text + self.DELIMITER
        for char in text_with_delimiter:
            bits += format(ord(char), '08b')
        return bits
    
    def bits_to_text(self, bits):
        """Chuyển dãy bits sang text"""
        text = ""
        # Đảm bảo độ dài bits chia hết cho 8
        if len(bits) % 8 != 0:
            bits = bits[:-(len(bits) % 8)]
            
        # Chuyển từng 8 bits thành ký tự
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
        """Giấu tin nhắn vào file audio"""
        try:
            # Đọc file audio
            with wave.open(audio_path, 'rb') as wav_in:
                # Lấy các thông số
                n_channels = wav_in.getnchannels()
                sampwidth = wav_in.getsampwidth()
                framerate = wav_in.getframerate()
                n_frames = wav_in.getnframes()
                frames = wav_in.readframes(n_frames)
                
            # Chuyển frames thành mảng số
            audio_data = np.frombuffer(frames, dtype=np.int16).copy()
            
            # Chuyển message thành bits
            message_bits = self.text_to_bits(message)
            print(f"Message: {message}")
            print(f"Message bits: {message_bits}")
            
            if len(message_bits) > len(audio_data):
                return False, "Message too long for this audio file"
            
            # Reset LSB của tất cả samples
            audio_data = audio_data & ~1
            
            # Giấu tin
            for i in range(len(message_bits)):
                if message_bits[i] == '1':
                    audio_data[i] = audio_data[i] | 1
            
            # Lưu file mới
            with wave.open(output_path, 'wb') as wav_out:
                wav_out.setnchannels(n_channels)
                wav_out.setsampwidth(sampwidth)
                wav_out.setframerate(framerate)
                wav_out.writeframes(audio_data.tobytes())
            
            return True, "Message hidden successfully"
            
        except Exception as e:
            return False, f"Error hiding message: {str(e)}"

    def extract_message(self, audio_path):
        """Trích xuất tin nhắn từ file audio"""
        try:
            # Đọc file audio
            with wave.open(audio_path, 'rb') as wav:
                n_frames = wav.getnframes()
                frames = wav.readframes(n_frames)
            
            # Chuyển frames thành mảng số
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Lấy LSB từ mỗi sample
            extracted_bits = ''
            # Chỉ lấy số bits cần thiết (8 bits * max_chars)
            max_chars = 1000  # Giới hạn độ dài tin nhắn
            max_bits = max_chars * 8
            
            for i in range(min(len(audio_data), max_bits)):
                bit = audio_data[i] & 1
                extracted_bits += str(bit)
                
                # Thử chuyển thành text sau mỗi byte
                if len(extracted_bits) % 8 == 0:
                    text = self.bits_to_text(extracted_bits)
                    if self.DELIMITER in text:
                        return True, text[:-len(self.DELIMITER)]
            
            return False, "No hidden message found"
            
        except Exception as e:
            return False, f"Error extracting message: {str(e)}"
