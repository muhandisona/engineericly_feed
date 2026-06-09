from PIL import Image, ImageDraw

def make_circle_favicon():
    # Open the logo
    try:
        img = Image.open('assets/images/logo.jpg').convert("RGBA")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Resize to a square if not already
    size = min(img.size)
    img = img.crop((0, 0, size, size))
    img = img.resize((256, 256), Image.Resampling.LANCZOS)

    # Create a circular mask
    mask = Image.new('L', (256, 256), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 256, 256), fill=255)

    # Apply mask
    output = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask=mask)

    # Save as favicon.ico
    output.save('assets/images/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    output.save('assets/images/logo_circle.png', format='PNG')
    print("Created circular favicon successfully.")

if __name__ == "__main__":
    make_circle_favicon()
