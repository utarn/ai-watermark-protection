# ป้องกันลายน้ำจาก Gemini Pro

แอปพลิเคชัน Gradio สำหรับป้องกันและลบลายน้ำจากรูปภาพโดยการเพิ่มและตัดพื้นที่ขาว

A Gradio application for protecting images from watermarks by adding and removing white canvas areas.

## 🎯 Features / คุณสมบัติ

### 1. เพิ่มพื้นที่ป้องกัน (Add Protection Area)
- เพิ่มพื้นที่สีขาวด้านขวา 10% ของความกว้างภาพ
- เพิ่มพื้นที่สีขาวด้านล่าง 10% ของความสูงภาพ
- ภาพต้นฉบับจะไม่ถูกย่อขนาด เพียงแค่เพิ่มพื้นที่
- รองรับการอัปโหลดทั้งรูปเดียวและหลายรูป

**Description:**
- Adds white canvas to the right: 10% of image width
- Adds white canvas to the bottom: 10% of image height
- Original image is not resized, only canvas is expanded
- Supports both single and batch upload

### 2. ตัดพื้นที่คืน (Restore Original)
- คำนวณย้อนกลับเพื่อหาขนาดเดิมก่อนการขยาย (หาร 1.1)
- ลบพื้นที่ที่เพิ่มเข้ามาออกให้หมด
- ได้ภาพขนาดเดิมกลับมาแบบแม่นยำ
- รองรับการอัปโหลดทั้งรูปเดียวและหลายรูป

**Description:**
- Calculates original dimensions by dividing by 1.1
- Removes all added canvas areas
- Restores exact original image size
- Supports both single and batch upload

## 📦 Installation / การติดตั้ง

### Prerequisites / ความต้องการ
- Python 3.10 or higher
- UV package manager

### Install UV / ติดตั้ง UV

If you don't have UV installed, install it using one of these methods:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**With pip:**
```bash
pip install uv
```

### Setup Project / ตั้งค่าโปรเจค

```bash
# Create virtual environment and install dependencies
# สร้าง virtual environment และติดตั้ง dependencies
uv sync
```

This command will:
- Create a virtual environment if it doesn't exist
- Install all project dependencies from pyproject.toml
- Lock dependencies in uv.lock file

คำสั่งนี้จะ:
- สร้าง virtual environment หากยังไม่มี
- ติดตั้ง dependencies ทั้งหมดจาก pyproject.toml
- ล็อก dependencies ในไฟล์ uv.lock

## 🚀 Usage / การใช้งาน

### Option 1: Command Line Interface (CLI) / ส่วนติดต่อบรรทัดคำสั่ง

The AI Watermark Fighter now supports command-line processing for batch operations with automatic file naming!

**Key Features:**
- **Automatic Suffix Naming**: Input files get suffixes added automatically
  - Enlarge operation: `filename.jpg` → `filename-enlarge.jpg`
  - Restore operation: `filename.jpg` → `filename-restore.jpg`
- **Batch Processing**: Process multiple files at once
- **Flexible Input**: Support single files, directories, and glob patterns
- **Custom Output Directory**: Specify where to save processed files

**Installation for CLI:**
```bash
# Install the package in development mode
pip install -e .
```

**Basic CLI Usage:**
```bash
# Enlarge a single image
ai-watermark-fighter enlarge image.jpg

# Enlarge multiple images with custom output directory
ai-watermark-fighter enlarge *.jpg --output-dir ./processed

# Restore enlarged images
ai-watermark-fighter restore image-enlarge.jpg

# Process all images in a directory
ai-watermark-fighter enlarge ./images/ --output-dir ./output

# Verbose output
ai-watermark-fighter enlarge *.png --verbose
```

**Output Examples:**
```
Input:          Output:
photo.jpg       → photo-enlarge.jpg
image.png       → image-enlarge.png
diagram.webp    → diagram-enlarge.webp
```

**Advanced Usage:**
```bash
# Restore all enlarged images in a directory
ai-watermark-fighter restore ./enlarge_images/ --output-dir ./restored/

# Process using glob patterns
ai-watermark-fighter enlarge "photos/**/*.jpg" --output-dir ./protected/

# Alternative direct usage
python cli.py enlarge image.jpg --output-dir ./results
```

**Programming Usage:**
```python
from ai_watermark_fighter import process_enlarge_images, process_restore_images
from pathlib import Path

# Process files programmatically
input_files = [Path("image1.jpg"), Path("image2.png")]
enlarged = process_enlarge_images(input_files, Path("./output"))
restored = process_restore_images(enlarged, Path("./restored"))
```

### Option 2: Using Docker (Recommended for Web UI) / ใช้งานกับ Docker (แนะนำสำหรับ Web UI)

**Prerequisites / ความต้องการ:**
- Docker
- Docker Compose

**Quick Start:**
```bash
# Build and start the container
# สร้างและเริ่ม container
docker-compose up -d

# View logs
# ดูล็อก
docker-compose logs -f

# Stop the container
# หยุด container
docker-compose down
```

The application will be available at `http://localhost:7860`

แอปพลิเคชันจะพร้อมใช้งานที่ `http://localhost:7860`

**Rebuild after code changes / สร้างใหม่หลังแก้ไขโค้ด:**
```bash
docker-compose up -d --build
```

### Option 2: Local Development / การพัฒนาแบบโลคัล

**Starting the Application / เริ่มแอปพลิเคชัน:**

```bash
# Run with UV
# รันด้วย UV
uv run python app.py
```

**Alternative (if you activated the virtual environment):**
```bash
# Activate virtual environment first
# เปิดใช้งาน virtual environment ก่อน
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Then run normally
# จากนั้นรันตามปกติ
python app.py
```

The application will start and open in your default web browser at `http://127.0.0.1:7860`

แอปพลิเคชันจะเริ่มทำงานและเปิดในเว็บเบราว์เซอร์เริ่มต้นของคุณที่ `http://127.0.0.1:7860`

### Using the Interface / การใช้งานอินเทอร์เฟซ

#### Tab 1: เพิ่มพื้นที่ป้องกัน (Add Protection Area)

**Single Image / รูปเดียว:**
1. Click "Upload Image" to select an image
2. Click "เพิ่มพื้นที่ป้องกัน (Add Protection)" button
3. The processed image will appear on the right
4. Right-click on the result to save

**Batch Upload / หลายรูป:**
1. Click "Upload Multiple Images" to select multiple images
2. Click "ประมวลผลทั้งหมด (Process All)" button
3. All processed images will appear in the gallery
4. Click on each image to view full size and save

#### Tab 2: ตัดพื้นที่คืน (Restore Original)

**Single Image / รูปเดียว:**
1. Upload the image that has been expanded
2. Click "ตัดพื้นที่คืน (Restore Original)" button
3. The cropped image will appear on the right

**Batch Upload / หลายรูป:**
1. Upload multiple expanded images
2. Click "ประมวลผลทั้งหมด (Process All)" button
3. All cropped images will appear in the gallery

## 📐 Calculation Logic / ตรรกะการคำนวณ

### Add Protection Example / ตัวอย่างการเพิ่มพื้นที่:
```
Original Image: 1000px (width) × 800px (height)
Add to right: 1000 × 0.1 = 100px
Add to bottom: 800 × 0.1 = 80px
Result: 1100px × 880px
```

### Restore Original Example / ตัวอย่างการตัดพื้นที่:
```
Expanded Image: 1100px × 880px
Restore width: 1100 ÷ 1.1 = 1000px (exact!)
Restore height: 880 ÷ 1.1 = 800px (exact!)
Result: 1000px × 800px (exact original size!)
```

**Important Note / หมายเหตุสำคัญ:**
- Expansion adds 10% to **each dimension independently** (width and height)
- Cropping divides by 1.1 to reverse the expansion **exactly**
- This ensures you get back the exact original dimensions
- การขยายเพิ่ม 10% ให้กับ **แต่ละมิติแยกกัน** (ความกว้างและความสูง)
- การตัดใช้การหารด้วย 1.1 เพื่อย้อนกลับการขยาย **อย่างแม่นยำ**
- วิธีนี้ทำให้ได้ขนาดเดิมกลับมาอย่างแม่นยำ

## 🛠️ Technical Details / รายละเอียดทางเทคนิค

### Core Functions / ฟังก์ชันหลัก

#### `expand_image(image: Image.Image) -> Image.Image`
Expands an image by adding white canvas to the right and bottom based on 10% of the current width.

#### `crop_image(image: Image.Image) -> Image.Image`
Crops an image by removing canvas from the right and bottom based on 10% of the current width.

### Error Handling / การจัดการข้อผิดพลาด
- Invalid image files are skipped with error messages in console
- Images too small to crop will raise a ValueError
- Batch processing continues even if individual images fail

## 📁 Project Structure / โครงสร้างโปรเจค

```
/
├── app.py              # Main Gradio application
├── cli.py              # Command Line Interface for batch processing
├── examples.py         # Usage examples and demonstrations
├── __init__.py         # Package initialization file
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock             # Locked dependencies
├── test_logic.py       # Unit tests for image processing logic
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker build exclusions
└── README.md           # This file
```

**File Descriptions:**

- **`app.py`**: Gradio web interface for interactive image processing
- **`cli.py`**: Command-line tool for batch processing with automatic suffix naming
- **`examples.py`**: Demonstrates both programmatic and CLI usage patterns
- **`__init__.py`**: Makes the project importable as a Python package

## 🔧 Dependencies / Dependencies

Managed via [`pyproject.toml`](pyproject.toml) and UV:

- **gradio** (>=4.44.1, <5.0.0): Web UI framework
- **Pillow** (>=10.3.0, <11.0.0): Image processing library

### Development Dependencies:
- **pytest** (>=7.0.0): Testing framework

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Notes / หมายเหตุ

- All processed images are converted to PNG format with transparency support
- Original transparency is preserved for RGBA images
- White canvas is used for expansion to ensure compatibility with most images
- Batch processing is efficient and handles multiple images simultaneously
- ภาพที่ประมวลผลทั้งหมดถูกแปลงเป็นรูปแบบ PNG พร้อมรองรับความโปร่งใส
- ความโปร่งใสต้นฉบับจะถูกรักษาไว้สำหรับภาพ RGBA
- ใช้พื้นที่สีขาวในการเพิ่มพื้นที่เพื่อความเข้ากันได้กับภาพส่วนใหญ่
- การประมวลผลแบบกลุ่มมีประสิทธิภาพและจัดการหลายภาพพร้อมกัน

## 🐛 Troubleshooting / การแก้ไขปัญหา

### Docker Issues / ปัญหา Docker
- Check Docker is running: `docker ps`
- View container logs: `docker-compose logs -f`
- Rebuild container: `docker-compose up -d --build`
- Remove all containers and rebuild: `docker-compose down && docker-compose up -d --build`
- ตรวจสอบว่า Docker ทำงานอยู่: `docker ps`
- ดูล็อกของ container: `docker-compose logs -f`
- สร้าง container ใหม่: `docker-compose up -d --build`

### Application won't start / แอปพลิเคชันไม่เริ่มทำงาน
- Ensure all dependencies are installed: `uv sync`
- Check Python version: `python --version` (should be 3.10+)
- Try running with UV: `uv run python app.py`
- ตรวจสอบว่าติดตั้ง dependencies ครบ: `uv sync`
- ตรวจสอบเวอร์ชัน Python: `python --version` (ควรเป็น 3.10+)

### Dependencies issues / ปัญหา Dependencies
- Remove lock file and reinstall: `rm uv.lock && uv sync`
- Clear UV cache: `uv cache clean`
- ลบ lock file และติดตั้งใหม่: `rm uv.lock && uv sync`
- ล้าง cache ของ UV: `uv cache clean`

### Images not processing / ภาพไม่ถูกประมวลผล
- Check console for error messages
- Ensure image files are valid formats (PNG, JPG, JPEG, etc.)
- For cropping, ensure the image is large enough (width > 100px recommended)
- ตรวจสอบข้อความ error ใน console
- ตรวจสอบว่าไฟล์รูปภาพเป็นรูปแบบที่ถูกต้อง (PNG, JPG, JPEG ฯลฯ)
- สำหรับการตัด ตรวจสอบว่ารูปภาพมีขนาดใหญ่พอ (แนะนำความกว้าง > 100px)

### Batch upload not working / การอัปโหลดหลายรูปไม่ทำงาน
- Make sure to select image files only
- Check file permissions
- Try with fewer images if experiencing issues
- ตรวจสอบว่าเลือกเฉพาะไฟล์รูปภาพเท่านั้น
- ตรวจสอบสิทธิ์การเข้าถึงไฟล์
- ลองใช้รูปภาพน้อยลงหากพบปัญหา