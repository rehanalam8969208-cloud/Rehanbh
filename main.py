from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
from PIL import Image
import random
import os

# Android Storage Permission
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

GALLERY_PATH = "/storage/emulated/0/DCIM/Camera/"

class GlitchApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1) # Dark hacker theme
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.title_label = Label(text="[color=00FF00]🌀 PIXEL GLITCH & RESTORE 🌀[/color]", markup=True, font_size=24, size_hint=(1, 0.2))
        self.img_input = TextInput(hint_text="Photo ka naam (e.g. image.jpg)", background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 1, 0, 1))
        self.out_input = TextInput(hint_text="Output naam (e.g. output.png)", background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 1, 0, 1))
        self.key_input = TextInput(hint_text="Secret Key (Password)", password=True, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 1, 0, 1))
        
        self.glitch_btn = Button(text="Glitch Photo", background_color=(0.8, 0, 0, 1))
        self.glitch_btn.bind(on_press=self.do_glitch)
        
        self.restore_btn = Button(text="Restore Photo", background_color=(0, 0.5, 1, 1))
        self.restore_btn.bind(on_press=self.do_restore)

        self.status_label = Label(text="Status: Ready", color=(1, 1, 0, 1), size_hint=(1, 0.2))

        layout.add_widget(self.title_label)
        layout.add_widget(self.img_input)
        layout.add_widget(self.out_input)
        layout.add_widget(self.key_input)
        layout.add_widget(self.glitch_btn)
        layout.add_widget(self.restore_btn)
        layout.add_widget(self.status_label)

        return layout

    def find_photo(self, image_name):
        if os.path.exists(image_name): return image_name
        paths = [os.path.join(GALLERY_PATH, image_name), os.path.join(os.getcwd(), image_name)]
        for path in paths:
            if os.path.exists(path): return path
        return None

    def process_image(self, is_glitch):
        img_path = self.img_input.text
        out_path = self.out_input.text
        key = self.key_input.text

        if not img_path or not out_path or not key:
            self.status_label.text = "Error: Sabhi fields bharna zaroori hai!"
            return

        real_path = self.find_photo(img_path)
        if not real_path:
            self.status_label.text = f"Error: Photo nahi mili -> {img_path}"
            return

        try:
            img = Image.open(real_path).convert('RGB')
            width, height = img.size
            pixels = list(img.getdata())

            random.seed(key)
            indices = list(range(len(pixels)))
            random.shuffle(indices)

            new_pixels = [None] * len(pixels)
            if is_glitch:
                for i, new_idx in enumerate(indices):
                    new_pixels[new_idx] = pixels[i]
            else:
                for i, new_idx in enumerate(indices):
                    new_pixels[i] = pixels[new_idx]

            new_img = Image.new('RGB', (width, height))
            new_img.putdata(new_pixels)

            if not (out_path.endswith('.png') or out_path.endswith('.jpg')):
                out_path += '.png'
            
            save_path = os.path.join(os.getcwd(), out_path)
            new_img.save(save_path)
            
            action = "Glitch" if is_glitch else "Restore"
            self.status_label.text = f"Success! {action} photo saved as {out_path}"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def do_glitch(self, instance):
        self.process_image(is_glitch=True)

    def do_restore(self, instance):
        self.process_image(is_glitch=False)

if __name__ == "__main__":
    GlitchApp().run()
