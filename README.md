# Audio Steganography Application

Ứng dụng giấu tin trong audio sử dụng phương pháp LSB (Least Significant Bit) và Phase Coding.

## Giới thiệu

Audio Steganography là kỹ thuật giấu thông tin bí mật vào trong file âm thanh mà không làm thay đổi đáng kể chất lượng âm thanh. Ứng dụng này cung cấp hai phương pháp steganography:

- LSB (Least Significant Bit): Thay đổi bit ít quan trọng nhất của mỗi sample
- Phase Coding: Điều chế phase của tín hiệu âm thanh để giấu tin

## Tính năng

### Steganography

- Giấu tin trong file audio sử dụng 2 phương pháp:
  - LSB (Least Significant Bit)
  - Phase Coding
- Hỗ trợ nhiều định dạng audio:
  - WAV
  - MP3
  - FLAC
  - OGG
  - M4A
- Tự động chuyển đổi định dạng về WAV

### Analysis Tools

- Waveform comparison
- Spectrogram visualization
- Quality metrics:
  - SNR (Signal-to-Noise Ratio)
  - PSNR (Peak Signal-to-Noise Ratio)
- File info analysis:
  - Sample rate
  - Bit depth
  - Channels
  - Duration
  - File size

### Giao diện

- Dark theme hiện đại
- Audio player tích hợp
- Trực quan và dễ sử dụng
- Real-time feedback

## Cài đặt

1. Cài đặt FFmpeg:

```bash
# Windows (sử dụng Chocolatey)
choco install ffmpeg

# macOS (sử dụng Homebrew)
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install ffmpeg
```

2. Clone repository:

```bash
git clone https://github.com/baolamabcd13/datahiding-audio.git
cd datahiding-audio
```

3. Cài đặt python3.10:

```bash
sudo apt install python3.10
```

4. Cài đặt môi trường ảo cho window:

```bash
python3.10 -m venv venv
venv\Scripts\activate
```

5. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

## Sử dụng

### 1. Giấu tin (Hide Message)

1. Chạy ứng dụng: `python main.py`
2. Chuyển đến tab "Hide Message"
3. Load file audio (hỗ trợ nhiều định dạng)
4. Nhập tin nhắn cần giấu
5. Chọn phương pháp (LSB/Phase Coding)
6. Click 'Hide Message'
7. Chọn vị trí lưu file stego

### 2. Trích xuất tin (Extract Message)

1. Chuyển đến tab "Extract Message"
2. Load file audio đã giấu tin
3. Chọn phương pháp đã dùng
4. Click 'Extract Message'
5. Xem tin nhắn được trích xuất

### 3. Phân tích (Analysis)

1. Chuyển đến tab "Analysis"
2. Load file audio gốc và file stego
3. Click 'Analyze'
4. Xem các kết quả phân tích:
   - So sánh waveform
   - Spectrogram
   - SNR & PSNR
   - Thông tin file

## BÁO CÁO ĐỀ TÀI AUDIO STEGANOGRAPHY

CHƯƠNG 1: TỔNG QUAN
1.1. Giới thiệu
Khái niệm steganography
Tầm quan trọng và ứng dụng
Các phương pháp steganography phổ biến
1.2. Audio Steganography
Đặc điểm của audio steganography
Ưu điểm so với các phương pháp khác
Thách thức trong việc giấu tin vào audio

CHƯƠNG 2: CƠ SỞ LÝ THUYẾT
2.1. Phương pháp LSB (Least Significant Bit)
2.1.1. Nguyên lý hoạt động
Cấu trúc file audio WAV
Cách thức biểu diễn bit trong audio
Kỹ thuật thay đổi LSB
2.1.2. Chu trình xử lý
Quá trình giấu tin (Embedding):
Đọc file audio
Chuyển đổi message thành bits
Thay đổi LSB của mỗi sample
Lưu file stego
Quá trình trích xuất (Extraction):
Đọc file stego
Trích xuất LSB
Chuyển đổi bits thành message
2.2. Phương pháp Phase Coding
2.2.1. Nguyên lý hoạt động
Phổ tần số của audio
Phase và amplitude trong audio
Kỹ thuật điều chế phase
2.2.2. Chu trình xử lý
Quá trình giấu tin:
Phân đoạn audio
Chuyển đổi sang miền tần số (FFT)
Điều chế phase
Chuyển về miền thời gian (IFFT)
Quá trình trích xuất:
Phân đoạn audio
Chuyển sang miền tần số
Phân tích phase
Khôi phục message

CHƯƠNG 3: THIẾT KẾ VÀ TRIỂN KHAI
3.1. Kiến trúc hệ thống
Sơ đồ tổng quan
Các module chính
Luồng dữ liệu
3.2. Cài đặt các phương pháp
3.2.1. LSB Implementation
Cấu trúc code
Các hàm chính
Xử lý lỗi
3.2.2. Phase Coding Implementation
Cấu trúc code
Các hàm chính
Xử lý lỗi
3.3. Giao diện người dùng
Thiết kế UI
Các tính năng
Xử lý tương tác

CHƯƠNG 4: ĐÁNH GIÁ VÀ THỰC NGHIỆM
4.1. Môi trường thử nghiệm
Hardware/Software
Dataset test
Các metric đánh giá
4.2. Kết quả thực nghiệm
4.2.1. So sánh hai phương pháp
Capacity (dung lượng tin)
Imperceptibility (độ không nhận biết)
Robustness (độ bền vững)
Performance (hiệu năng)
4.2.2. Phân tích chất lượng
SNR (Signal-to-Noise Ratio)
PSNR (Peak Signal-to-Noise Ratio)
Spectrogram analysis
Subjective evaluation
4.3. Ưu nhược điểm
LSB method
Phase Coding method
Overall system

CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
5.1. Kết luận
Tổng kết kết quả đạt được
Đánh giá hiệu quả
Những thách thức
5.2. Hướng phát triển
Cải thiện thuật toán
Thêm tính năng bảo mật
Mở rộng hỗ trợ định dạng
Tối ưu hóa performance

## NGUYÊN LÝ HOẠT ĐỘNG

### 1. LSB (Least Significant Bit)

a. Nguyên lý hoạt động:

- Mỗi sample trong audio được biểu diễn bởi n-bit (thường là 16-bit)
- Thay đổi bit cuối cùng (LSB) của mỗi sample để giấu thông tin
- Mỗi sample có thể giấu 1 bit thông tin
- Thông tin cần giấu được chuyển thành dãy bit nhị phân trước khi nhúng

b. Chức năng:

- Mã hóa tin nhắn thành dãy bit
- Quét từng sample và thay đổi LSB
- Lưu trữ metadata (độ dài tin nhắn, checksum)
- Trích xuất tin nhắn bằng cách đọc LSB

### 2. Phase Coding

a. Nguyên lý hoạt động:

- Chia tín hiệu audio thành các segment
- Chuyển đổi mỗi segment sang miền tần số (FFT)
- Điều chế phase của các thành phần tần số để giấu tin
- Giữ nguyên magnitude để bảo toàn chất lượng âm thanh
- Chuyển đổi ngược về miền thời gian (IFFT)

b. Chức năng:

- Phân đoạn tín hiệu audio
- Biến đổi FFT và tính toán phase
- Điều chế phase để nhúng thông tin
- Tái tạo tín hiệu với IFFT
- Đảm bảo tính liên tục của phase giữa các segment

## QUÁ TRÌNH XỬ LÝ

### 1. Quá trình giấu tin (Embedding)

a. LSB Method:

- Đọc file audio và chuyển về định dạng WAV
- Chuyển đổi message thành dãy bit
- Lưu trữ độ dài message vào header
- Quét từng sample và thay đổi LSB
- Tính toán và lưu checksum
- Lưu file stego dưới dạng WAV

b. Phase Coding:

- Đọc và chuẩn hóa tín hiệu audio
- Phân đoạn tín hiệu thành các segment
- Với mỗi segment:
  - Thực hiện FFT
  - Tính toán phase và magnitude
  - Điều chế phase để nhúng thông tin
  - Thực hiện IFFT
- Ghép các segment lại
- Lưu file stego

### 2. Quá trình trích xuất (Extraction)

a. LSB Method:

- Đọc file stego
- Trích xuất độ dài message từ header
- Đọc LSB của từng sample
- Gom các bit thành byte
- Kiểm tra checksum
- Khôi phục message gốc

b. Phase Coding:

- Đọc file stego
- Phân đoạn tín hiệu
- Với mỗi segment:
  - Thực hiện FFT
  - Trích xuất phase
  - Giải điều chế để lấy thông tin
- Gom các bit thành message
- Kiểm tra tính toàn vẹn

### 3. Phân tích chất lượng

- So sánh waveform trước và sau khi giấu tin
- Phân tích spectrogram
- Tính toán các chỉ số:
  - SNR (Signal-to-Noise Ratio)
  - PSNR (Peak Signal-to-Noise Ratio)
  - MSE (Mean Square Error)
- Đánh giá chủ quan chất lượng âm thanh
