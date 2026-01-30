from PIL import Image, ImageDraw

items = ['idli', 'dosa', 'upma', 'poha', 'vada']
for item in items:
    img = Image.new('RGB', (300, 200), color='white')
    d = ImageDraw.Draw(img)
    d.text((50, 80), f'{item.capitalize()}', fill=(0,0,0))
    img.save(f'static/images/{item}.jpg')