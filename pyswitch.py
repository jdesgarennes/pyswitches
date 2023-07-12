import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog

class SwitchConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Switch Config Generator")

        layout = QVBoxLayout()

        label = QLabel("Switch Config Generator")
        layout.addWidget(label)

        hostname_label = QLabel("Hostname:")
        layout.addWidget(hostname_label)
        self.hostname_entry = QLineEdit()
        layout.addWidget(self.hostname_entry)

        mgmt_ip_label = QLabel("Management IP:")
        layout.addWidget(mgmt_ip_label)
        self.mgmt_ip_entry = QLineEdit()
        layout.addWidget(self.mgmt_ip_entry)

        body_text = QLabel("Switch Body Config:")
        layout.addWidget(body_text)
        self.body_text_entry = QLineEdit()
        layout.addWidget(self.body_text_entry)

        button = QPushButton("Generate")
        button.clicked.connect(self.generate_and_save)
        layout.addWidget(button)

        self.setLayout(layout)
        self.show()

    def generate_and_save(self):
        hostname = self.hostname_entry.text()
        mgmt_ip = self.mgmt_ip_entry.text()
        body_text = self.body_text_entry.text()

        # Generate switch configuration
        config = f"Hostname: {hostname}\nManagement IP: {mgmt_ip}\nBody Text: {body_text}"

        # Open a file dialog to select the save location
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')

        if file_path:
            # Write the configuration to the selected file
            with open(file_path, 'w') as file:
                file.write(config)

            print(f'Configuration saved to: {file_path}')


if __name__ == '__main__':
    app = QApplication([])
    window = SwitchConfig()
    app.exec_()
