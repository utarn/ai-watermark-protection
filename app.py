import gradio as gr
from PIL import Image
import numpy as np
from typing import List, Union
import io


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


def process_expand_single(image):
    """Process single image expansion"""
    if image is None:
        return None
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        expanded = expand_image(image)
        return expanded
    except Exception as e:
        print(f"Error expanding image: {e}")
        return None


def process_expand_batch(images):
    """Process batch image expansion"""
    if images is None or len(images) == 0:
        return []
    
    results = []
    for img in images:
        try:
            # Convert to PIL Image if needed
            if isinstance(img, np.ndarray):
                img = Image.fromarray(img)
            
            expanded = expand_image(img)
            results.append(expanded)
        except Exception as e:
            print(f"Error expanding image: {e}")
            continue
    
    return results


def process_crop_single(image):
    """Process single image cropping"""
    if image is None:
        return None
    
    try:
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        cropped = crop_image(image)
        return cropped
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None


def process_crop_batch(images):
    """Process batch image cropping"""
    if images is None or len(images) == 0:
        return []
    
    results = []
    for img in images:
        try:
            # Convert to PIL Image if needed
            if isinstance(img, np.ndarray):
                img = Image.fromarray(img)
            
            cropped = crop_image(img)
            results.append(cropped)
        except Exception as e:
            print(f"Error cropping image: {e}")
            continue
    
    return results


# Create Gradio interface
with gr.Blocks(title="ป้องกันลายน้ำจาก Gemini Pro") as app:
    gr.Markdown("# ป้องกันลายน้ำจาก Gemini Pro")
    gr.Markdown("แอปพลิเคชันสำหรับป้องกันและลบลายน้ำจากรูปภาพ")
    
    with gr.Tabs():
        # Tab 1: Expand (Add Protection)
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
                    expand_button = gr.Button("เพิ่มพื้นที่ป้องกัน (Add Protection)", variant="primary")
                
                with gr.Column():
                    expand_output = gr.Image(
                        label="ผลลัพธ์ (Result)",
                        type="pil"
                    )
            
            gr.Markdown("---")
            gr.Markdown("### การอัปโหลดหลายรูป (Batch Upload)")
            
            with gr.Row():
                with gr.Column():
                    expand_batch_input = gr.Files(
                        label="อัปโหลดหลายรูปภาพ (Upload Multiple Images)",
                        file_types=["image"]
                    )
                    expand_batch_button = gr.Button("ประมวลผลทั้งหมด (Process All)", variant="primary")
                
                with gr.Column():
                    expand_batch_output = gr.Gallery(
                        label="ผลลัพธ์ทั้งหมด (All Results)",
                        columns=3,
                        height="auto"
                    )
            
            expand_button.click(
                fn=process_expand_single,
                inputs=expand_input,
                outputs=expand_output
            )
            
            def process_files_expand(files):
                if files is None or len(files) == 0:
                    return []
                images = [Image.open(f.name) for f in files]
                return process_expand_batch(images)
            
            expand_batch_button.click(
                fn=process_files_expand,
                inputs=expand_batch_input,
                outputs=expand_batch_output
            )
        
        # Tab 2: Crop (Remove Protection)
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
                    crop_button = gr.Button("ตัดพื้นที่คืน (Restore Original)", variant="primary")
                
                with gr.Column():
                    crop_output = gr.Image(
                        label="ผลลัพธ์ (Result)",
                        type="pil"
                    )
            
            gr.Markdown("---")
            gr.Markdown("### การอัปโหลดหลายรูป (Batch Upload)")
            
            with gr.Row():
                with gr.Column():
                    crop_batch_input = gr.Files(
                        label="อัปโหลดหลายรูปภาพ (Upload Multiple Images)",
                        file_types=["image"]
                    )
                    crop_batch_button = gr.Button("ประมวลผลทั้งหมด (Process All)", variant="primary")
                
                with gr.Column():
                    crop_batch_output = gr.Gallery(
                        label="ผลลัพธ์ทั้งหมด (All Results)",
                        columns=3,
                        height="auto"
                    )
            
            crop_button.click(
                fn=process_crop_single,
                inputs=crop_input,
                outputs=crop_output
            )
            
            def process_files_crop(files):
                if files is None or len(files) == 0:
                    return []
                images = [Image.open(f.name) for f in files]
                return process_crop_batch(images)
            
            crop_batch_button.click(
                fn=process_files_crop,
                inputs=crop_batch_input,
                outputs=crop_batch_output
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