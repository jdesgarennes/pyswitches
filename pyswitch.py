import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, QComboBox

class SwitchConfig(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Switch Config Generator")

        layout = QVBoxLayout()

        label = QLabel("Switch Config Generator")
        layout.addWidget(label)

        # switch templates  C9300-48U  C3850-12X4 C9300-48T
        template_label = QLabel("Select Template:")
        layout.addWidget(template_label)
        self.template_combo = QComboBox()
        self.template_combo.addItem("C9300-48U") 
        self.template_combo.addItem("C3850-12X4")
        layout.addWidget(self.template_combo)

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

        radius_password_label = QLabel("Radius Password:")
        layout.addWidget(radius_password_label)
        self.radius_password_entry = QLineEdit()
        layout.addWidget(self.radius_password_entry)

        button = QPushButton("Generate Single Config")
        button.clicked.connect(self.generate_config)
        layout.addWidget(button)

        batch_button = QPushButton("Batch Mode")
        batch_button.clicked.connect(self.batch_mode)
        layout.addWidget(batch_button)

        self.setLayout(layout)

    def generate_config(self):
        template = self.template_combo.currentText()
        hostname = self.hostname_entry.text()
        mgmt_ip = self.mgmt_ip_entry.text()
        passphrase = self.passphrase_entry.text()
        tacsecrete = self.tacsecrete_entry.text()
        radius_password = self.radius_password_entry.text()

        # Generate configuration using the selected template and provided parameters
        config = self.generate_template(template, hostname, mgmt_ip, passphrase, tacsecrete, radius_password)

        # Save the configuration to a file
        file_path = self.save_to_file(config, hostname)

        # Display completion message and file path in a popup window
        QMessageBox.information(self, "Single Config Generation Complete", f"Configuration saved to: {file_path}")

    def batch_mode(self):
        # Open a file dialog to select the CSV file
        file_dialog = QFileDialog()
        csv_path, _ = file_dialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')

        if csv_path:
            # Read the CSV file and generate configurations
            with open(csv_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    template = self.template_combo.currentText()
                    hostname = row['Hostname']
                    mgmt_ip = row['Management IP']
                    passphrase = row['Passphrase']
                    tacsecrete = row['Tacsecrete']
                    radius_password = row['Radius Password']

                    # Generate configuration using the selected template and provided parameters
                    config = self.generate_template(template, hostname, mgmt_ip, passphrase, tacsecrete, radius_password)

                    # Save the configuration to a file
                    self.save_to_file(config, hostname)

            QMessageBox.information(self, "Batch Mode", "Batch configuration generation completed.")

    def generate_template(self, template, hostname, mgmt_ip, passphrase, tacsecrete, radius_password):
        # Read the template file and replace placeholders with provided parameters
        template_dir = "templates"
        template_file = f"{template.lower().replace(' ', '_')}.txt"
        template_path = os.path.join(template_dir, template_file)

        with open(template_path, 'r') as file:
            template_content = file.read()

        config = template_content.replace("{{hostname}}", hostname)
        config = config.replace("{{mgmt_ip}}", mgmt_ip)
        config = config.replace("{{passphrase}}", passphrase)
        config = config.replace("{{tacsecrete}}", tacsecrete)
        config = config.replace("{{radius_password}}", radius_password)

        return config

    def save_to_file(self, config, hostname):
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, f"{hostname}.txt")

        with open(file_path, 'w') as file:
            file.write(config)

        return file_path

if __name__ == '__main__':
    app = QApplication([])
    window = SwitchConfig()
    window.show()
    app.exec_()
