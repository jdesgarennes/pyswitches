import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QComboBox

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

        passphrase_label = QLabel("Passphrase:")
        layout.addWidget(passphrase_label)
        self.passphrase_entry = QLineEdit()
        layout.addWidget(self.passphrase_entry)

        tacsecrete_label = QLabel("Tacsecrete:")
        layout.addWidget(tacsecrete_label)
        self.tacsecrete_entry = QLineEdit()
        layout.addWidget(self.tacsecrete_entry)

        template_label = QLabel("Template:")
        layout.addWidget(template_label)
        self.template_combo = QComboBox()
        self.template_combo.addItem("template1")
        self.template_combo.addItem("template2")
        layout.addWidget(self.template_combo)

        button_generate = QPushButton("Generate")
        button_generate.clicked.connect(self.generate_config)
        layout.addWidget(button_generate)

        button_save = QPushButton("Save to File")
        button_save.clicked.connect(self.save_to_file)
        layout.addWidget(button_save)

        self.setLayout(layout)

    def generate_config(self):
        hostname = self.hostname_entry.text()
        mgmt_ip = self.mgmt_ip_entry.text()
        passphrase = self.passphrase_entry.text()
        tacsecrete = self.tacsecrete_entry.text()

        template = self.template_combo.currentText()

        # Load the template file
        with open("./templates/template.txt", "r") as file:
            template_content = file.read()

        # Replace the variables in the template
        template_content = template_content.replace("{{hostname}}", hostname)
        template_content = template_content.replace("{{mgmt_ip}}", mgmt_ip)
        template_content = template_content.replace("{{passphrase}}", passphrase)
        template_content = template_content.replace("{{tacsecrete}}", tacsecrete)

        # Print or save the generated configuration
        print("Generated switch configuration:")
        print(template_content)

        self.generated_config = template_content

    def save_to_file(self):
        if hasattr(self, 'generated_config'):
            # Open a file dialog to select the save location
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)')

            if file_path:
                # Write the generated configuration to the selected file
                with open(file_path, 'w') as file:
                    file.write(self.generated_config)

                print(f'File saved to: {file_path}')
        else:
            print("No configuration generated yet.")

if __name__ == '__main__':
    app = QApplication([])
    window = SwitchConfig()
    window.show()
    app.exec_()
