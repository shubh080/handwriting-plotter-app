import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.FileChooser import FileChooserListView  # For picking files on Android

# Try importing serial (used for USB OTG communication)
try:
    import serial
except ImportError:
    serial = None

class PlotterApp(App):
    def build(self):
        self.selected_file_path = None
        
        # Main layout (vertical stack)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Status Label
        self.status_label = Label(
            text='Status: Ready. Please select a G-code file.',
            font_size=18,
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.status_label)
        
        # File Chooser widget to browse phone storage
        self.file_chooser = FileChooserListView(
            path='/sdcard/',  # Points to Android phone storage
            filters=['*.gcode', '*.nc', '*.txt'],
            size_hint=(1, 0.6)
        )
        self.file_chooser.bind(selection=self.on_file_selected)
        layout.add_widget(self.file_chooser)
        
        # Start Plotting Button
        self.start_btn = Button(
            text='Start Plotting',
            font_size=24,
            size_hint=(1, 0.2),
            background_color=(0.1, 0.6, 0.1, 1)  # Green color
        )
        self.start_btn.bind(on_press=self.start_plotting)
        layout.add_widget(self.start_btn)
        
        return layout

    def on_file_selected(self, filechooser, selection):
        if selection:
            self.selected_file_path = selection[0]
            filename = os.path.basename(self.selected_file_path)
            self.status_label.text = f'Selected: {filename}'

    def start_plotting(self, instance):
        if not self.selected_file_path:
            self.status_label.text = 'Error: No G-code file selected!'
            return
        
        self.status_label.text = 'Connecting to Plotter...'
        
        # 1. Check if PySerial is working
        if serial is None:
            self.status_label.text = 'Error: PySerial module missing!'
            return
        
        try:
            # Common Android USB-serial port paths (usually ttyUSB0 or ttyACM0)
            port_path = '/dev/ttyUSB0'
            if not os.path.exists(port_path):
                port_path = '/dev/ttyACM0'
                
            # Open serial connection (Baud rate 115200 is standard for GRBL plotter boards)
            self.status_label.text = f'Opening port {port_path}...'
            connection = serial.Serial(port_path, 115200, timeout=1)
            
            # Read and send G-code file line by line
            self.status_label.text = 'Plotting in progress...'
            with open(self.selected_file_path, 'r') as f:
                for line in f:
                    line_stripped = line.strip()
                    # Skip empty lines or comments
                    if not line_stripped or line_stripped.startswith('(') or line_stripped.startswith(';'):
                        continue
                    
                    # Send command to plotter
                    connection.write((line_stripped + '\n').encode('utf-8'))
                    
                    # Read response from plotter board (optional, keeps sync)
                    response = connection.readline().decode('utf-8').strip()
            
            connection.close()
            self.status_label.text = 'Plotting Complete!'
            
        except Exception as e:
            self.status_label.text = f'Connection Error: Check USB OTG cable!'

if __name__ == '__main__':
    PlotterApp().run()
