import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox

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

        button = QPushButton("Generate Single Config")
        button.clicked.connect(self.generate_config)
        layout.addWidget(button)

        batch_button = QPushButton("Batch Mode")
        batch_button.clicked.connect(self.batch_mode)
        layout.addWidget(batch_button)

        self.setLayout(layout)

        self.show()  # Show the window

    def generate_config(self):
        hostname = self.hostname_entry.text()
        mgmt_ip = self.mgmt_ip_entry.text()
        passphrase = self.passphrase_entry.text()
        tacsecrete = self.tacsecrete_entry.text()

        # Read the template file
        with open('./templates/template.txt', 'r') as template_file:
            template = template_file.read()

        # Replace the variables in the template with the provided values
        config = template.replace('{{hostname}}', hostname)
        config = config.replace('{{mgmt_ip}}', mgmt_ip)
        config = config.replace('{{passphrase}}', passphrase)
        config = config.replace('{{tacsecrete}}', tacsecrete)

        # Save the configuration to a file
        self.save_to_file(config, hostname)

    def batch_mode(self):
        # Open a file dialog to select the CSV file
        file_dialog = QFileDialog()
        csv_path, _ = file_dialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')

        if csv_path:
            # Read the CSV file and generate configurations
            with open(csv_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    hostname = row['Hostname']
                    mgmt_ip = row['Management IP']
                    passphrase = row['Passphrase']
                    tacsecrete = row['Tacsecrete']

                    # Read the template file
                    with open('./templates/template.txt', 'r') as template_file:
                        template = template_file.read()

                    # Replace the variables in the template with the provided values
                    config = template.replace('{{hostname}}', hostname)
                    config = config.replace('{{mgmt_ip}}', mgmt_ip)
                    config = config.replace('{{passphrase}}', passphrase)
                    config = config.replace('{{tacsecrete}}', tacsecrete)

                    # Save the configuration to a file
                    self.save_to_file(config, hostname)

            QMessageBox.information(self, "Batch Mode", "Batch configuration generation completed.")

    def save_to_file(self, config, hostname):
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, f"{hostname}.txt")

        with open(file_path, 'w') as file:
            file.write(config)

        print(f'Configuration saved to: {file_path}')

if __name__ == '__main__':
    app = QApplication([])
    window = SwitchConfig()
    app.exec_()
