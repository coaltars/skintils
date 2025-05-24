from PIL import Image, ImageDraw, ImageFont
import os, shutil, glob

class Processor:
    def create_backup(self, skin_path, files):
        backup_path = os.path.join(skin_path, 'backup')
        os.makedirs(backup_path, exist_ok=True)
        
        for file in files:
            if os.path.exists(file):
                shutil.copy2(file, backup_path)

    def get_hitcircle_path(self, skin_path):
        hitcircle_hd = os.path.join(skin_path, 'hitcircle@2x.png')
        hitcircle_normal = os.path.join(skin_path, 'hitcircle.png')
        
        if os.path.exists(hitcircle_hd):
            return hitcircle_hd
        elif os.path.exists(hitcircle_normal):
            return hitcircle_normal
        return None

    def create_blank_image(self):
        return Image.new('RGBA', (1, 1), (0, 0, 0, 0))

    def merge_images(self, base_path, overlay_path):
        base = Image.open(base_path).convert('RGBA')
        overlay = Image.open(overlay_path).convert('RGBA')
        return Image.alpha_composite(base, overlay)

    def triplestack_circles(self, skin_path):
        hitcircle_path = self.get_hitcircle_path(skin_path)
        if not hitcircle_path:
            raise Exception("hitcircle.png or hitcircle@2x.png not found in skin folder")
        
        default_files = []
        for i in range(10):
            default_path = os.path.join(skin_path, f'default-{i}.png')
            default_2x_path = os.path.join(skin_path, f'default-{i}@2x.png')
            if os.path.exists(default_path):
                existing_defaults.append(default_path)
            if os.path.exists(default_2x_path):
                existing_defaults.append(default_2x_path)
                
        self.create_backup(skin_path, default_files + [hitcircle_path])
        for i in range(1, 10):
            default_path = os.path.join(skin_path, f'default-{i}.png')
            if os.path.exists(default_path):
                merged = self.merge_images(hitcircle_path, default_path)
                merged.save(default_path)
                
        blank = self.create_blank_image()
        blank.save(os.path.join(skin_path, 'default-0.png'))
        for overlay_file in glob.glob(os.path.join(skin_path, 'hitcircleoverlay*.png')):
            os.remove(overlay_file)
        shutil.copy2(hitcircle_path, os.path.join(skin_path, 'hitcircleoverlay.png'))

    def instafade_circles(self, skin_path):
        hitcircle_path = self.get_hitcircle_path(skin_path)
        if not hitcircle_path:
            raise Exception("hitcircle.png or hitcircle@2x.png not found in skin folder")
        
        default_files = []
        for i in range(10):
            default_path = os.path.join(skin_path, f'default-{i}.png')
            default_2x_path = os.path.join(skin_path, f'default-{i}@2x.png')
            if os.path.exists(default_path):
                existing_defaults.append(default_path)
            if os.path.exists(default_2x_path):
                existing_defaults.append(default_2x_path)
                
        circle_files = glob.glob(os.path.join(skin_path, 'hitcircle*.png'))
        self.create_backup(skin_path, default_files + circle_files)
        for i in range(1, 10):
            default_path = os.path.join(skin_path, f'default-{i}.png')
            if os.path.exists(default_path):
                merged = self.merge_images(hitcircle_path, default_path)
                merged.save(default_path)
                
        blank = self.create_blank_image()
        blank.save(os.path.join(skin_path, 'default-0.png'))
        for circle_file in ['hitcircle.png', 'hitcircle@2x.png', 'hitcircleoverlay.png', 'hitcircleoverlay@2x.png']:
            circle_path = os.path.join(skin_path, circle_file)
            blank.save(circle_path)

    def apply_font_file(self, skin_path, font_path):
        existing_defaults = []
        for i in range(10):
            default_path = os.path.join(skin_path, f'default-{i}.png')
            default_2x_path = os.path.join(skin_path, f'default-{i}@2x.png')
            if os.path.exists(default_path):
                existing_defaults.append(default_path)
            if os.path.exists(default_2x_path):
                existing_defaults.append(default_2x_path)
        if existing_defaults:
            self.create_backup(skin_path, existing_defaults)
            
        font = ImageFont.truetype(font_path, 120)
        for i in range(10):
            img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            text = str(i)
            bbox = draw.textbbox((0, 0), text, font=font)
            
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (200 - text_width) // 2
            y = (200 - text_height) // 2
            
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
            default_path = os.path.join(skin_path, f'default-{i}@2x.png')
            img.save(default_path)
