import gradio as gr
from PIL import Image
import numpy as np
from typing import List, Union
import io
import zipfile
import tempfile
import os
from pathlib import Path
from datetime import datetime


def expand_image(image: Image.Image) -> Image.Image:
    """
    Expand image by adding white canvas to right and bottom.
    Adds 10% to width and 10% to height (each based on its own dimension).
    Preserves transparency for RGBA images.
    
    Args:
        image: PIL Image object
        
    Returns:
        Expanded PIL Image object in RGB/RGBA mode (PNG compatible)
    """
    if image is None:
        return None
    
    # Get original dimensions
    original_width, original_height = image.size
    
    # Calculate expansion amount (10% of each dimension)
    expand_width = int(original_width * 0.1)
    expand_height = int(original_height * 0.1)
    
    # Calculate new dimensions
    new_width = original_width + expand_width
    new_height = original_height + expand_height
    
    # Preserve transparency if present, otherwise convert to RGB
    if image.mode == 'RGBA':
        # Create new RGBA image with white background and full opacity
        expanded_image = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 255))
        # Paste with alpha channel as mask to preserve transparency
        expanded_image.paste(image, (0, 0), image)
    else:
        # Convert to RGB for non-transparent images
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        elif image.mode == 'L':
            image = image.convert('RGB')
        
        # Create new RGB image with white background
        expanded_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))
        expanded_image.paste(image, (0, 0))
    
    return expanded_image


def crop_image(image: Image.Image) -> Image.Image:
    """
    Crop image by removing canvas from right and bottom.
    Calculates the original dimensions before expansion (reverses the 10% expansion).
    Preserves transparency for RGBA images.
    
    Formula:
    - If expanded: new_size = original × 1.1
    - To restore: original = current / 1.1
    
    Args:
        image: PIL Image object
        
    Returns:
        Cropped PIL Image object in RGB/RGBA mode (PNG compatible)
    """
    if image is None:
        return None
    
    # Preserve RGBA mode for transparent images, convert others to RGB
    if image.mode == 'RGBA':
        # Keep RGBA mode to preserve transparency
        pass
    elif image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')
    elif image.mode == 'L':
        image = image.convert('RGB')
    
    # Get current dimensions
    current_width, current_height = image.size
    
    # Calculate original dimensions before expansion
    # Since expansion adds 10% (multiply by 1.1), we divide by 1.1 to get original
    # Use round() instead of int() for better accuracy
    original_width = round(current_width / 1.1)
    original_height = round(current_height / 1.1)
    
    # Ensure dimensions are positive
    if original_width <= 0 or original_height <= 0:
        raise ValueError("Image is too small to crop")
    
    # Crop image from top-left to original dimensions (preserves mode)
    cropped_image = image.crop((0, 0, original_width, original_height))
    
    return cropped_image


def process_expand_single(image, output_format='WEBP'):
    """Process single image expansion"""
    if image is None:
        return None
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        expanded = expand_image(image)
        
        # Convert image to the selected format for proper download
        output_format = output_format.upper()
        if output_format == 'JPG':
            # Convert to RGB for JPEG
            if expanded.mode in ['RGBA', 'LA']:
                # Create white background
                background = Image.new('RGB', expanded.size, (255, 255, 255))
                if expanded.mode == 'RGBA':
                    background.paste(expanded, mask=expanded.split()[-1])
                else:
                    background.paste(expanded)
                expanded = background
            elif expanded.mode not in ['RGB']:
                expanded = expanded.convert('RGB')
        elif output_format == 'PNG':
            # Keep original mode for PNG to preserve transparency
            pass
        elif output_format == 'WEBP':
            # Keep original mode for WebP to preserve transparency
            pass
        
        return expanded
    except Exception as e:
        print(f"Error expanding image: {e}")
        return None


def process_expand_batch(images, output_format='WEBP'):
    """Process batch image expansion"""
    if images is None or len(images) == 0:
        return []
    
    results = []
    output_format = output_format.upper()
    
    for img in images:
        try:
            # Convert to PIL Image if needed
            if isinstance(img, np.ndarray):
                img = Image.fromarray(img)
            
            expanded = expand_image(img)
            
            # Convert image to the selected format for proper download
            if output_format == 'JPG':
                # Convert to RGB for JPEG
                if expanded.mode in ['RGBA', 'LA']:
                    # Create white background
                    background = Image.new('RGB', expanded.size, (255, 255, 255))
                    if expanded.mode == 'RGBA':
                        background.paste(expanded, mask=expanded.split()[-1])
                    else:
                        background.paste(expanded)
                    expanded = background
                elif expanded.mode not in ['RGB']:
                    expanded = expanded.convert('RGB')
            elif output_format == 'PNG':
                # Keep original mode for PNG to preserve transparency
                pass
            elif output_format == 'WEBP':
                # Keep original mode for WebP to preserve transparency
                pass
            
            results.append(expanded)
        except Exception as e:
            print(f"Error expanding image: {e}")
            continue
    
    return results


def process_crop_single(image, output_format='WEBP'):
    """Process single image cropping"""
    if image is None:
        return None
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        cropped = crop_image(image)
        
        # Convert image to the selected format for proper download
        output_format = output_format.upper()
        if output_format == 'JPG':
            # Convert to RGB for JPEG
            if cropped.mode in ['RGBA', 'LA']:
                # Create white background
                background = Image.new('RGB', cropped.size, (255, 255, 255))
                if cropped.mode == 'RGBA':
                    background.paste(cropped, mask=cropped.split()[-1])
                else:
                    background.paste(cropped)
                cropped = background
            elif cropped.mode not in ['RGB']:
                cropped = cropped.convert('RGB')
        elif output_format == 'PNG':
            # Keep original mode for PNG to preserve transparency
            pass
        elif output_format == 'WEBP':
            # Keep original mode for WebP to preserve transparency
            pass
        
        return cropped
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None


def process_crop_batch(images, output_format='WEBP'):
    """Process batch image cropping"""
    if images is None or len(images) == 0:
        return []
    
    results = []
    output_format = output_format.upper()
    
    for img in images:
        try:
            # Convert to PIL Image if needed
            if isinstance(img, np.ndarray):
                img = Image.fromarray(img)
            
            cropped = crop_image(img)
            
            # Convert image to the selected format for proper download
            if output_format == 'JPG':
                # Convert to RGB for JPEG
                if cropped.mode in ['RGBA', 'LA']:
                    # Create white background
                    background = Image.new('RGB', cropped.size, (255, 255, 255))
                    if cropped.mode == 'RGBA':
                        background.paste(cropped, mask=cropped.split()[-1])
                    else:
                        background.paste(cropped)
                    cropped = background
                elif cropped.mode not in ['RGB']:
                    cropped = cropped.convert('RGB')
            elif output_format == 'PNG':
                # Keep original mode for PNG to preserve transparency
                pass
            elif output_format == 'WEBP':
                # Keep original mode for WebP to preserve transparency
                pass
            
            results.append(cropped)
        except Exception as e:
            print(f"Error cropping image: {e}")
            continue
    
    return results


def create_zip_from_images(images, output_format='WEBP', prefix='image'):
    """
    Create a zip file containing all processed images.
    
    Args:
        images: List of PIL Image objects
        output_format: Format to save images (PNG, JPG, WEBP)
        prefix: Prefix for image filenames
        
    Returns:
        Path to the created zip file
    """
    if not images or len(images) == 0:
        return None
    
    # Ensure output_format is uppercase for consistency
    output_format = output_format.upper() if output_format else 'WEBP'
    
    # Determine file extension and format name based on output_format
    if output_format == 'JPG' or output_format == 'JPEG':
        ext = '.jpg'
        format_name = 'JPEG'
    elif output_format == 'PNG':
        ext = '.png'
        format_name = 'PNG'
    else:  # Default to WEBP
        ext = '.webp'
        format_name = 'WEBP'
    
    # Create temporary zip file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{prefix}_batch_{timestamp}.zip"
    zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for idx, img in enumerate(images, 1):
                # Create temporary file for each image
                img_filename = f"{prefix}_{idx:03d}{ext}"
                
                # Save image to bytes
                img_bytes = io.BytesIO()
                
                if output_format == 'JPG':
                    # Convert to RGB for JPEG if needed
                    if img.mode in ['RGBA', 'LA']:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        background.save(img_bytes, format_name, quality=95)
                    else:
                        img.save(img_bytes, format_name, quality=95)
                else:
                    img.save(img_bytes, format_name, quality=95)
                
                # Add to zip
                zipf.writestr(img_filename, img_bytes.getvalue())
        
        return zip_path
    except Exception as e:
        print(f"Error creating zip file: {e}")
        return None


# Create Gradio interface
with gr.Blocks(title="ป้องกันลายน้ำจาก Gemini Pro") as app:
    gr.Markdown("# ป้องกันลายน้ำจาก Gemini Pro")
    gr.Markdown("แอปพลิเคชันสำหรับป้องกันและลบลายน้ำจากรูปภาพ")
    
    with gr.Tabs():
        # Tab 1: Instructions (New)
        with gr.Tab("วิธีใช้งาน (How to Use)"):
            gr.Markdown("""
            # คู่มือการใช้งานแอปพลิเคชัน
            
            ## 📱 แอปนี้ทำอะไร?
            
            แอปพลิเคชันนี้ช่วยให้คุณสามารถ**ขยายรูปภาพไปทางขวาและด้านล่าง**เพื่อป้องกันลายน้ำจาก Google Gemini Pro Image Generation
            โดยเฉพาะอย่างยิ่งเหมาะสำหรับการใช้งานบนมือถือ เพราะมีอินเทอร์เฟซที่ใช้งานง่าย
            
            ---
            
            ## ⚡ วิธีการใช้งาน (แนะนำ)
            
            ### ขั้นตอนที่ 1: ใช้ Gemini สร้างหรือแก้ไขรูปภาพ
            - ใช้ Google Gemini Pro สร้างรูปภาพหรือแก้ไขรูปภาพของคุณ
            - Gemini จะใส่ลายน้ำ (ดาวสีขาว) ที่มุมล่างขวาของรูปภาพ
            
            ### ขั้นตอนที่ 2: ขยายรูปภาพเพื่อป้องกันลายน้ำ
            1. นำรูปภาพที่ได้จาก Gemini มาอัปโหลดในแท็บ **"เพิ่มพื้นที่ป้องกัน"**
            2. กดปุ่ม "เพิ่มพื้นที่ป้องกัน"
            3. รูปภาพจะถูกขยายออกไป 10% ทางขวาและด้านล่าง (เพิ่มพื้นที่สีขาว)
            4. ดาวน์โหลดรูปที่ขยายแล้ว
            
            ### ขั้นตอนที่ 3: ใช้ Gemini ลบลายน้ำ
            1. นำรูปที่ขยายแล้วไปให้ Gemini แก้ไข
            2. สั่งให้ Gemini **"ลบดาวสีขาวที่อยู่รอบๆ มุมล่างขวาก่อนพื้นที่สีขาว"**
            3. Gemini จะลบดาวเดิมออก และสร้างลายน้ำใหม่ที่พื้นที่สีขาวที่เราเพิ่มเข้าไป
            
            ### ขั้นตอนที่ 4: ตัดพื้นที่สีขาวออก
            1. นำรูปที่ Gemini แก้ไขแล้วมาอัปโหลดในแท็บ **"ตัดพื้นที่คืน"**
            2. กดปุ่ม "ตัดพื้นที่คืน"
            3. แอปจะตัดพื้นที่สีขาวที่มีลายน้ำออก
            4. ได้รูปภาพสะอาดไม่มีลายน้ำ! ✨
            
            ---
            
            ## 🎯 ตัวอย่างการทำงาน
            
            ```
            รูปต้นฉบับจาก Gemini (มีลายน้ำที่มุมล่างขวา)
                    ↓
            [ขั้นตอนที่ 2] ขยายรูป → เพิ่มพื้นที่สีขาว 10% ขวาและล่าง
                    ↓
            [ขั้นตอนที่ 3] ให้ Gemini ลบดาวเดิม → ลายน้ำใหม่ไปอยู่บนพื้นที่สีขาว
                    ↓
            [ขั้นตอนที่ 4] ตัดพื้นที่สีขาว → ได้รูปสะอาดไม่มีลายน้ำ
            ```
            
            ---
            
            ## 💡 เคล็ดลับ
            
            - **ใช้บนมือถือได้สะดวก**: UI ออกแบบมาให้ใช้งานง่ายบนหน้าจอมือถือ
            - **รองรับหลายรูป**: สามารถประมวลผลหลายรูปพร้อมกันได้ในโหมด Batch
            - **เลือกรูปแบบไฟล์ได้**: รองรับ PNG, JPG, และ WEBP
            - **ความแม่นยำสูง**: การตัดคืนใช้สูตรคำนวณแบบย้อนกลับเพื่อความแม่นยำ
            
            ---
            
            ## 📐 สูตรคำนวณ
            
            **การขยาย (Expand):**
            - ความกว้างใหม่ = ความกว้างเดิม × 1.1 (เพิ่ม 10%)
            - ความสูงใหม่ = ความสูงเดิม × 1.1 (เพิ่ม 10%)
            
            **การตัดคืน (Restore):**
            - ความกว้างเดิม = ความกว้างปัจจุบัน ÷ 1.1
            - ความสูงเดิม = ความสูงปัจจุบัน ÷ 1.1
            
            ตัวอย่าง: 1000×800px → ขยาย → 1100×880px → ตัดคืน → 1000×800px ✓
            
            ---
            
            ## ⚠️ หมายเหตุสำคัญ
            
            - แอปนี้**ไม่ได้ลบลายน้ำโดยตรง** แต่ช่วยให้ Gemini ลบลายน้ำได้ง่ายขึ้น
            - ต้องใช้ร่วมกับ Google Gemini Pro Image Generation
            - รูปภาพจะถูกแปลงเป็น PNG/JPG/WEBP ตามที่เลือก
            - รองรับความโปร่งใส (transparency) สำหรับไฟล์ PNG
            """)
        
        # Tab 2: Expand (Add Protection) - moved from Tab 1
        with gr.Tab("เพิ่มพื้นที่ป้องกัน (Add Protection Area)"):
            gr.Markdown("""
            ### คำอธิบาย:
            - เพิ่มพื้นที่สีขาวด้านขวา 10% ของความกว้างภาพ
            - เพิ่มพื้นที่สีขาวด้านล่าง 10% ของความกว้างภาพ
            - ภาพต้นฉบับจะไม่ถูกย่อขนาด เพียงแค่เพิ่มพื้นที่
            
            ### Description:
            - Add white canvas to the right: 10% of image width
            - Add white canvas to the bottom: 10% of image width
            - Original image is not resized, only canvas is expanded
            """)
            
            with gr.Row():
                with gr.Column():
                    expand_input = gr.Image(
                        label="อัปโหลดรูปภาพ (Upload Image)",
                        type="pil",
                        sources=["upload"]
                    )
                    expand_format = gr.Dropdown(
                        choices=["WEBP", "PNG", "JPG"],
                        value="WEBP",
                        label="Output Format (รูปแบบไฟล์)"
                    )
                    expand_button = gr.Button("เพิ่มพื้นที่ป้องกัน (Add Protection)", variant="primary")
                
                with gr.Column():
                    expand_output = gr.Image(
                        label="ผลลัพธ์ (Result)",
                        type="pil"
                    )
                    expand_download = gr.File(
                        label="📥 Download Processed Image",
                        visible=True
                    )
            
            gr.Markdown("---")
            gr.Markdown("### การอัปโหลดหลายรูป (Batch Upload)")
            
            with gr.Row():
                with gr.Column():
                    expand_batch_input = gr.Files(
                        label="อัปโหลดหลายรูปภาพ (Upload Multiple Images)",
                        file_types=["image"]
                    )
                    expand_batch_format = gr.Dropdown(
                        choices=["WEBP", "PNG", "JPG"],
                        value="WEBP",
                        label="Output Format (รูปแบบไฟล์)"
                    )
                    expand_batch_button = gr.Button("ประมวลผลทั้งหมด (Process All)", variant="primary")
                
                with gr.Column():
                    expand_batch_output = gr.Gallery(
                        label="ผลลัพธ์ทั้งหมด (All Results)",
                        columns=3,
                        height="auto"
                    )
                    expand_batch_download_zip = gr.File(
                        label="📦 ดาวน์โหลดไฟล์ ZIP ทั้งหมด (Download All as ZIP)",
                        visible=True
                    )
            
            def process_and_save_expand(image, output_format):
                if image is None:
                    return None, None
                    
                processed_image = process_expand_single(image, output_format)
                if processed_image is None:
                    return None, None
                
                # Save to temporary file for download with correct format
                output_format = output_format.upper() if output_format else 'WEBP'
                
                if output_format == 'JPG' or output_format == 'JPEG':
                    ext = '.jpg'
                    format_name = 'JPEG'
                elif output_format == 'PNG':
                    ext = '.png'
                    format_name = 'PNG'
                else:
                    ext = '.webp'
                    format_name = 'WEBP'
                
                # Create temp file with proper naming: image-enlarge.ext
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext, prefix='image-enlarge_', dir=tempfile.gettempdir())
                
                # Rename to have clean filename
                final_name = os.path.join(tempfile.gettempdir(), f'image-enlarge{ext}')
                
                # Save with format conversion if needed
                if output_format == 'JPG' or output_format == 'JPEG':
                    if processed_image.mode in ['RGBA', 'LA']:
                        # Create white background for JPEG
                        background = Image.new('RGB', processed_image.size, (255, 255, 255))
                        if processed_image.mode == 'RGBA':
                            background.paste(processed_image, mask=processed_image.split()[-1])
                        else:
                            background.paste(processed_image)
                        background.save(final_name, format_name, quality=95)
                    else:
                        processed_image.save(final_name, format_name, quality=95)
                else:
                    processed_image.save(final_name, format_name, quality=95)
                
                tmp_file.close()
                os.unlink(tmp_file.name)  # Remove the temp file
                return processed_image, final_name
            
            expand_button.click(
                fn=process_and_save_expand,
                inputs=[expand_input, expand_format],
                outputs=[expand_output, expand_download]
            )
            
            def process_files_expand(files, output_format):
                if files is None or len(files) == 0:
                    return [], None
                
                # Store original filenames
                original_filenames = [Path(f.name).stem for f in files]
                images = [Image.open(f.name) for f in files]
                processed_images = process_expand_batch(images, output_format)
                
                # Create zip file
                zip_path = create_zip_from_images(processed_images, output_format, prefix='expanded')
                
                # Save processed images to temporary files with correct extensions for gallery display
                output_format = output_format.upper() if output_format else 'WEBP'
                if output_format == 'JPG' or output_format == 'JPEG':
                    ext = '.jpg'
                    format_name = 'JPEG'
                elif output_format == 'PNG':
                    ext = '.png'
                    format_name = 'PNG'
                else:
                    ext = '.webp'
                    format_name = 'WEBP'
                
                gallery_files = []
                for idx, (img, orig_name) in enumerate(zip(processed_images, original_filenames)):
                    # Use original filename with -enlarge suffix
                    filename = f'{orig_name}-enlarge{ext}'
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    
                    if output_format == 'JPG' or output_format == 'JPEG':
                        if img.mode in ['RGBA', 'LA']:
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'RGBA':
                                background.paste(img, mask=img.split()[-1])
                            else:
                                background.paste(img)
                            background.save(temp_path, format_name, quality=95)
                        else:
                            img.save(temp_path, format_name, quality=95)
                    else:
                        img.save(temp_path, format_name, quality=95)
                    
                    gallery_files.append(temp_path)
                
                return gallery_files, zip_path
            
            expand_batch_button.click(
                fn=process_files_expand,
                inputs=[expand_batch_input, expand_batch_format],
                outputs=[expand_batch_output, expand_batch_download_zip]
            )
        
        # Tab 3: Crop (Remove Protection) - moved from Tab 2
        with gr.Tab("ตัดพื้นที่คืน (Restore Original)"):
            gr.Markdown("""
            ### คำอธิบาย:
            - ลบพื้นที่ด้านขวา 10% ของความกว้างภาพปัจจุบัน
            - ลบพื้นที่ด้านล่าง 10% ของความกว้างภาพปัจจุบัน
            - ใช้สำหรับคืนค่าภาพที่เพิ่มพื้นที่ป้องกันแล้ว
            
            ### Description:
            - Remove canvas from the right: 10% of current image width
            - Remove canvas from the bottom: 10% of current image width
            - Use this to restore images that have been expanded
            """)
            
            with gr.Row():
                with gr.Column():
                    crop_input = gr.Image(
                        label="อัปโหลดรูปภาพ (Upload Image)",
                        type="pil",
                        sources=["upload"]
                    )
                    crop_format = gr.Dropdown(
                        choices=["WEBP", "PNG", "JPG"],
                        value="WEBP",
                        label="Output Format (รูปแบบไฟล์)"
                    )
                    crop_button = gr.Button("ตัดพื้นที่คืน (Restore Original)", variant="primary")
                
                with gr.Column():
                    crop_output = gr.Image(
                        label="ผลลัพธ์ (Result)",
                        type="pil"
                    )
                    crop_download = gr.File(
                        label="📥 Download Processed Image",
                        visible=True
                    )
            
            gr.Markdown("---")
            gr.Markdown("### การอัปโหลดหลายรูป (Batch Upload)")
            
            with gr.Row():
                with gr.Column():
                    crop_batch_input = gr.Files(
                        label="อัปโหลดหลายรูปภาพ (Upload Multiple Images)",
                        file_types=["image"]
                    )
                    crop_batch_format = gr.Dropdown(
                        choices=["WEBP", "PNG", "JPG"],
                        value="WEBP",
                        label="Output Format (รูปแบบไฟล์)"
                    )
                    crop_batch_button = gr.Button("ประมวลผลทั้งหมด (Process All)", variant="primary")
                
                with gr.Column():
                    crop_batch_output = gr.Gallery(
                        label="ผลลัพธ์ทั้งหมด (All Results)",
                        columns=3,
                        height="auto"
                    )
                    crop_batch_download_zip = gr.File(
                        label="📦 ดาวน์โหลดไฟล์ ZIP ทั้งหมด (Download All as ZIP)",
                        visible=True
                    )
            
            def process_and_save_crop(image, output_format):
                if image is None:
                    return None, None
                    
                processed_image = process_crop_single(image, output_format)
                if processed_image is None:
                    return None, None
                
                # Save to temporary file for download with correct format
                output_format = output_format.upper() if output_format else 'WEBP'
                
                if output_format == 'JPG' or output_format == 'JPEG':
                    ext = '.jpg'
                    format_name = 'JPEG'
                elif output_format == 'PNG':
                    ext = '.png'
                    format_name = 'PNG'
                else:
                    ext = '.webp'
                    format_name = 'WEBP'
                
                # Create temp file with proper naming: image-restore.ext
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext, prefix='image-restore_', dir=tempfile.gettempdir())
                
                # Rename to have clean filename
                final_name = os.path.join(tempfile.gettempdir(), f'image-restore{ext}')
                
                # Save with format conversion if needed
                if output_format == 'JPG' or output_format == 'JPEG':
                    if processed_image.mode in ['RGBA', 'LA']:
                        # Create white background for JPEG
                        background = Image.new('RGB', processed_image.size, (255, 255, 255))
                        if processed_image.mode == 'RGBA':
                            background.paste(processed_image, mask=processed_image.split()[-1])
                        else:
                            background.paste(processed_image)
                        background.save(final_name, format_name, quality=95)
                    else:
                        processed_image.save(final_name, format_name, quality=95)
                else:
                    processed_image.save(final_name, format_name, quality=95)
                
                tmp_file.close()
                os.unlink(tmp_file.name)  # Remove the temp file
                return processed_image, final_name
            
            crop_button.click(
                fn=process_and_save_crop,
                inputs=[crop_input, crop_format],
                outputs=[crop_output, crop_download]
            )
            
            def process_files_crop(files, output_format):
                if files is None or len(files) == 0:
                    return [], None
                
                # Store original filenames
                original_filenames = [Path(f.name).stem for f in files]
                images = [Image.open(f.name) for f in files]
                processed_images = process_crop_batch(images, output_format)
                
                # Create zip file
                zip_path = create_zip_from_images(processed_images, output_format, prefix='restored')
                
                # Save processed images to temporary files with correct extensions for gallery display
                output_format = output_format.upper() if output_format else 'WEBP'
                if output_format == 'JPG' or output_format == 'JPEG':
                    ext = '.jpg'
                    format_name = 'JPEG'
                elif output_format == 'PNG':
                    ext = '.png'
                    format_name = 'PNG'
                else:
                    ext = '.webp'
                    format_name = 'WEBP'
                
                gallery_files = []
                for idx, (img, orig_name) in enumerate(zip(processed_images, original_filenames)):
                    # Use original filename with -restore suffix
                    filename = f'{orig_name}-restore{ext}'
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    
                    if output_format == 'JPG' or output_format == 'JPEG':
                        if img.mode in ['RGBA', 'LA']:
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'RGBA':
                                background.paste(img, mask=img.split()[-1])
                            else:
                                background.paste(img)
                            background.save(temp_path, format_name, quality=95)
                        else:
                            img.save(temp_path, format_name, quality=95)
                    else:
                        img.save(temp_path, format_name, quality=95)
                    
                    gallery_files.append(temp_path)
                
                return gallery_files, zip_path
            
            crop_batch_button.click(
                fn=process_files_crop,
                inputs=[crop_batch_input, crop_batch_format],
                outputs=[crop_batch_output, crop_batch_download_zip]
            )
    
    gr.Markdown("""
    ---
    ### ตัวอย่างการคำนวณ (Calculation Example):
    
    **การเพิ่มพื้นที่ป้องกัน (Add Protection):**
    - ภาพต้นฉบับ: 1000px (กว้าง) × 800px (สูง)
    - เพิ่มด้านขวา: 1000 × 0.1 = 100px
    - เพิ่มด้านล่าง: 1000 × 0.1 = 100px
    - ผลลัพธ์: 1100px × 900px
    
    **การตัดพื้นที่คืน (Restore Original):**
    - ภาพปัจจุบัน: 1100px × 900px
    - ตัดด้านขวา: 1100 × 0.1 = 110px
    - ตัดด้านล่าง: 1100 × 0.1 = 110px
    - ผลลัพธ์: 990px × 790px
    """)


if __name__ == "__main__":
    app.launch()