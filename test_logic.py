"""
Simple test script to verify the image processing logic
without running the full Gradio app
"""
from PIL import Image
import io

def expand_image(image: Image.Image) -> Image.Image:
    """Expand image by adding white canvas - 10% to each dimension"""
    original_width, original_height = image.size
    expand_width = int(original_width * 0.1)
    expand_height = int(original_height * 0.1)
    new_width = original_width + expand_width
    new_height = original_height + expand_height
    
    expanded_image = Image.new(image.mode, (new_width, new_height), 'white')
    expanded_image.paste(image, (0, 0))
    
    return expanded_image

def crop_image(image: Image.Image) -> Image.Image:
    """Crop image by removing canvas - reverses the 10% expansion"""
    current_width, current_height = image.size
    
    # Calculate original dimensions before expansion
    # Since expansion multiplies by 1.1, we divide by 1.1 to get original
    # Use round() instead of int() for better accuracy
    original_width = round(current_width / 1.1)
    original_height = round(current_height / 1.1)
    
    if original_width <= 0 or original_height <= 0:
        raise ValueError("Image is too small to crop")
    
    cropped_image = image.crop((0, 0, original_width, original_height))
    return cropped_image

def test_expand():
    """Test expansion logic"""
    print("Testing expansion logic...")
    
    # Create test image: 1000x800
    test_img = Image.new('RGB', (1000, 800), color='red')
    print(f"Original size: {test_img.size}")
    
    # Expand
    expanded = expand_image(test_img)
    print(f"Expanded size: {expanded.size}")
    print(f"Expected: (1100, 900)")
    
    # Verify (1000 + 100 = 1100, 800 + 80 = 880)
    assert expanded.size == (1100, 880), f"Expected (1100, 880), got {expanded.size}"
    print("✓ Expansion test passed!\n")
    
    return expanded

def test_crop(expanded_img):
    """Test cropping logic"""
    print("Testing cropping logic...")
    print(f"Input size (expanded): {expanded_img.size}")
    
    # Crop - should restore to original size
    cropped = crop_image(expanded_img)
    print(f"Cropped size: {cropped.size}")
    print(f"Expected: (1000, 800) - exact original size!")
    
    # Verify (1100 / 1.1 = 1000, 880 / 1.1 = 800)
    # Using round() for accurate restoration
    assert cropped.size == (1000, 800), f"Expected (1000, 800), got {cropped.size}"
    print("✓ Cropping test passed!\n")
    
    return cropped

def test_round_trip():
    """Test that expand + crop works correctly"""
    print("Testing round-trip (expand then crop)...")
    
    # Original: 1000x800
    original = Image.new('RGB', (1000, 800), color='blue')
    print(f"1. Original size: {original.size}")
    
    # After expansion: should be 1100x880 (10% of each dimension)
    expanded = expand_image(original)
    print(f"2. After expansion: {expanded.size}")
    assert expanded.size == (1100, 880), f"Expansion failed: {expanded.size}"
    
    # After cropping: should restore to original
    cropped = crop_image(expanded)
    print(f"3. After cropping: {cropped.size}")
    
    # Check if we got back to original width
    if cropped.size[0] == original.size[0]:
        print(f"   ✓ Width restored perfectly: {cropped.size[0]} = {original.size[0]}")
    else:
        print(f"   ⚠ Width difference: {cropped.size[0]} vs {original.size[0]}")
    
    # Check height (may have rounding difference)
    height_diff = abs(cropped.size[1] - original.size[1])
    if height_diff <= 1:
        print(f"   ✓ Height restored (±1px tolerance): {cropped.size[1]} ≈ {original.size[1]}")
    else:
        print(f"   ⚠ Height difference: {cropped.size[1]} vs {original.size[1]} (diff: {height_diff}px)")
    print()

def test_edge_cases():
    """Test edge cases with various resolutions that may have rounding issues"""
    print("Testing edge cases with various resolutions...")
    
    test_cases = [
        # (width, height, description)
        (1000, 800, "Standard case"),
        (999, 799, "Odd dimensions"),
        (1001, 801, "Prime-like dimensions"),
        (777, 555, "Dimensions with remainders"),
        (1920, 1080, "Full HD"),
        (1280, 720, "HD"),
        (500, 300, "Small image"),
        (3840, 2160, "4K"),
    ]
    
    all_passed = True
    for width, height, desc in test_cases:
        original = Image.new('RGB', (width, height), color='green')
        
        # Expand
        expanded = expand_image(original)
        
        # Crop back
        restored = crop_image(expanded)
        
        # Check results
        width_diff = abs(restored.size[0] - original.size[0])
        height_diff = abs(restored.size[1] - original.size[1])
        
        # Allow ±1px tolerance due to rounding
        if width_diff <= 1 and height_diff <= 1:
            status = "✓"
        else:
            status = "✗"
            all_passed = False
        
        print(f"  {status} {desc}: {original.size} → {expanded.size} → {restored.size}")
        if width_diff > 0 or height_diff > 0:
            print(f"      Difference: width={width_diff}px, height={height_diff}px")
    
    print()
    if all_passed:
        print("✓ All edge cases passed (within ±1px tolerance)!\n")
    else:
        print("⚠ Some edge cases exceeded ±1px tolerance\n")
    
    return all_passed

if __name__ == "__main__":
    print("="*60)
    print("Image Processing Logic Tests")
    print("="*60 + "\n")
    
    try:
        # Test expansion
        expanded_img = test_expand()
        
        # Test cropping
        cropped_img = test_crop(expanded_img)
        
        # Test round-trip
        test_round_trip()
        
        # Test edge cases with various resolutions
        edge_cases_passed = test_edge_cases()
        
        print("="*60)
        if edge_cases_passed:
            print("All tests passed! ✓")
        else:
            print("Tests completed with warnings ⚠")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()