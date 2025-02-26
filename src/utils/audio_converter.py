import subprocess
import os
import wave

class AudioConverter:
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    
    @staticmethod
    def convert_to_wav(input_path, output_path=None):
        """Chuyển đổi file audio sang WAV sử dụng ffmpeg"""
        try:
            # Lấy định dạng file input
            file_ext = os.path.splitext(input_path)[1].lower()
            
            # Kiểm tra định dạng được hỗ trợ
            if file_ext not in AudioConverter.SUPPORTED_FORMATS:
                return False, f"Unsupported format: {file_ext}"
                
            # Nếu đã là WAV thì copy
            if file_ext == '.wav':
                if output_path:
                    import shutil
                    shutil.copyfile(input_path, output_path)
                    return True, output_path
                return True, input_path
            
            # Tạo output path nếu không được chỉ định
            if not output_path:
                output_path = os.path.splitext(input_path)[0] + '_converted.wav'

            # Chuyển đổi sang WAV sử dụng ffmpeg
            command = [
                'ffmpeg',
                '-i', input_path,  # Input file
                '-acodec', 'pcm_s16le',  # Convert to 16-bit PCM
                '-ac', '2',  # Stereo
                '-ar', '44100',  # 44.1kHz sample rate
                '-y',  # Overwrite output file if exists
                output_path
            ]
            
            # Chạy ffmpeg command
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            # Kiểm tra kết quả
            if process.returncode == 0:
                print(f"Successfully converted {input_path} to {output_path}")
                return True, output_path
            else:
                error_msg = stderr.decode()
                print(f"FFmpeg error: {error_msg}")
                return False, f"Conversion failed: {error_msg}"
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            return False, f"Error processing audio: {str(e)}"
    
    @staticmethod
    def get_supported_formats():
        """Trả về danh sách định dạng được hỗ trợ"""
        return ' '.join(f"*{fmt}" for fmt in AudioConverter.SUPPORTED_FORMATS) 