import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import urllib3
from pyinfoblox import InfobloxWAPI

class SwitchConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.network_function = None  

        self.setWindowTitle("Switch Config Generator")
        self.setGeometry(100, 100, 800, 600)  # Set window size and position

        layout = QVBoxLayout()
        # This is just adding the window dressing for logo and stuff
        title_bar = QLabel(self)
        title_bar.setPixmap(QPixmap("./images/pech-logo-red.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        title_bar.setAlignment(Qt.AlignCenter)
        title_bar.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #cccccc; padding: 10px;")
        layout.addWidget(title_bar)

        label = QLabel("Switch Config Generator")
        label.setStyleSheet("font-size: 18px; color: #f45f0b ")  # Increase the font size to 18 pixels
        layout.addWidget(label)

        # switch templates  C9300-48U  C3850-12X4 C9300-48T
        template_label = QLabel("Select Template:")
        layout.addWidget(template_label)
        self.template_combo = QComboBox()
        self.template_combo.addItem("C9300-48U-PRC") 
        self.template_combo.addItem("C3850-12X4-PRC")
        self.template_combo.addItem("C9300_PGC")
        layout.addWidget(self.template_combo)

        hostname_label = QLabel("Hostname:")
        hostname_label.setStyleSheet("font-size: 18px; color: #f45f0b;")  # Increase the font size to 18 pixels
        layout.addWidget(hostname_label)
        self.hostname_entry = QLineEdit()
        layout.addWidget(self.hostname_entry)

        mgmt_ip_label = QLabel("Management IP:")
        mgmt_ip_label.setStyleSheet("font-size: 18px; color: #f45f0b;")  # Increase the font size to 18 pixels
        layout.addWidget(mgmt_ip_label)
        self.mgmt_ip_entry = QLineEdit()
        layout.addWidget(self.mgmt_ip_entry)

        passphrase_label = QLabel("Local-Passphrase:")
        passphrase_label.setStyleSheet("font-size: 18px; color: #f45f0b;")  # Increase the font size to 18 pixels
        layout.addWidget(passphrase_label)
        self.passphrase_entry = QLineEdit()
        layout.addWidget(self.passphrase_entry)

        tacsecrete_label = QLabel("Tac-secret:")
        tacsecrete_label.setStyleSheet("font-size: 18px; color: #f45f0b;")  # Increase the font size to 18 pixels
        layout.addWidget(tacsecrete_label)
        self.tacsecrete_entry = QLineEdit()
        layout.addWidget(self.tacsecrete_entry)

        radius_password_label = QLabel("Radius Password:")
        radius_password_label.setStyleSheet("font-size: 18px; color: #f45f0b;")  # Increase the font size to 18 pixels
        layout.addWidget(radius_password_label)
        self.radius_password_entry = QLineEdit()
        layout.addWidget(self.radius_password_entry)

        next_ip_button = QPushButton("Get Next Available IP")
        next_ip_button.clicked.connect(self.get_next_available_ip)
        layout.addWidget(next_ip_button)

        button = QPushButton("Generate Single Config")
        button.clicked.connect(self.generate_config)
        layout.addWidget(button)

        batch_button = QPushButton("Generate Batch Config")
        batch_button.clicked.connect(self.generate_batch_config)
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

    def get_next_available_ip(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        infoblox = InfobloxWAPI(
            username='XXXXXXXXXXX',
            password='XXXXXXXXXXX',
            wapi='https://10.0.20.13/wapi/v1.1/'
        )

        network_function = infoblox.network.function(
            objref='network/ZG5zLm5ldHdvcmskMTAuMTAuMC4wLzE2LzA:10.10.0.0/16/default',
            _function='next_available_ip',
            num=1
        )

        print(network_function)  # For debugging
       

        next_ip = network_function['ips'][0]  # Modification here

        self.mgmt_ip_entry.setText(next_ip)

        # Display the next available IP in a popup
        QMessageBox.information(self, "Next Available IP", f"The next available IP is: {next_ip}", buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)

    def generate_batch_config(self):
        # Get the selected template for batch generation
        template = self.template_combo.currentText()

        # Prompt user to select the CSV file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_path, _ = file_dialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")

        if file_path:
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row

                for row in csv_reader:
                    hostname, mgmt_ip = row[0], row[1]

                    config = self.generate_template(template, hostname, mgmt_ip, "", "", "")

                    file_name = f"{hostname}.txt"
                    file_path = os.path.join(output_dir, file_name)
                    with open(file_path, 'w') as output_file:
                        output_file.write(config)

            QMessageBox.information(
                self, "Batch Config Generation Complete", "Batch configurations generated successfully.", buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok
            )
        else:
            QMessageBox.warning(
                self, "Error", "No CSV file selected.", buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok
            )

    def generate_template(self, template, hostname, mgmt_ip, passphrase, tacsecrete, radius_password):
        # Read the template file and replace placeholders with provided parameters
        template_dir = "templates"
        template_file = f"{template_dir}/{template}.txt"
        with open(template_file, 'r') as file:
            template_content = file.read()
            template_content = template_content.replace("{{hostname}}", hostname)
            template_content = template_content.replace("{{mgmt_ip}}", mgmt_ip)
            template_content = template_content.replace("{{passphrase}}", passphrase)
            template_content = template_content.replace("{{tacsecrete}}", tacsecrete)
            template_content = template_content.replace("{{radius_password}}", radius_password)
        return template_content

    def save_to_file(self, config, hostname):
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_name = f"{hostname}.txt"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as file:
            file.write(config)
        return file_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SwitchConfig()
    window.show()
    sys.exit(app.exec_())
