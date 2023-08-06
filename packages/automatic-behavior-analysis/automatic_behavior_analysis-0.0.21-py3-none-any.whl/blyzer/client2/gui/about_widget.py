import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class AboutWidget(QWidget):
    AUTHORS = [
        ["Aleksandr Sinitca", "Saint Petersburg Electrotechnical University \"LETI\"", "amsinitca@etu.ru"],
        ["Michael Plazner", "University of Haifa", "mplazner@campus.haifa.ac.il"],
        ["Gabriel Malin", "University of Haifa", "gabi939@gmail.com"],
        ["Liel Moalem", "University of Haifa", "lielmoalem12@gmail.com"],
        ["Vladimir Kovrigin","Saint Petersburg Electrotechnical University \"LETI\"","kovrigin.v.k@gmail.com"]
        #["Name","affiliation","e-mail"]
    ]
    def __init__(self, parent=None):
        super().__init__(parent)

        self._res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("About")
        self.main_layout = QVBoxLayout()
        self.images_layout = QGridLayout()

        logo_haifa = QImage()
        logo_haifa.load(os.path.join(self._res_path, "unihaifa-300x160.jpg"))
        logo_haifa = logo_haifa.scaledToWidth(200)
        logo_haifa_widget = QLabel()
        logo_haifa_widget.setPixmap(QPixmap.fromImage(logo_haifa))
        self.images_layout.addWidget(logo_haifa_widget, 1, 2)

        logo_leti = QImage()
        logo_leti.load(os.path.join(self._res_path, "leti_logo_eng_2019.png"))
        logo_leti = logo_leti.scaledToWidth(200)
        logo_leti_widget = QLabel()
        logo_leti_widget.setPixmap(QPixmap.fromImage(logo_leti))
        self.images_layout.addWidget(logo_leti_widget, 1, 1)

        logo_digiratory = QImage()
        logo_digiratory.load(os.path.join(self._res_path,"digiratory_logo.png"))
        logo_digiratory = logo_digiratory.scaledToWidth(200)
        logo_digiratory_widget = QLabel()
        logo_digiratory_widget.setPixmap(QPixmap.fromImage(logo_digiratory))
        self.images_layout.addWidget(logo_digiratory_widget, 2, 1)

        logo_tech4animals = QImage()
        logo_tech4animals.load(os.path.join(self._res_path,"tech4animals_logo.jpg"))
        logo_tech4animals = logo_tech4animals.scaledToWidth(200)
        logo_tech4animals_widget = QLabel()
        logo_tech4animals_widget.setPixmap(QPixmap.fromImage(logo_tech4animals))
        self.images_layout.addWidget(logo_tech4animals_widget, 2, 2)


        self.main_layout.addLayout(self.images_layout)

        self.affiliation_widget = QTextEdit()
        self.affiliation_widget.setReadOnly(True)
        self.affiliation_widget.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        organisation = []
        for author in self.AUTHORS:
            if author[1] not in organisation:
                organisation.append(author[1])
        for author in self.AUTHORS:
            org_ind = organisation.index(author[1]) + 1
            s = "{name}<sup>{org_ind}</sup>, <a href=\"mailto:{mail}\">{mail}</a> <br> \n".format(name=author[0], org_ind=org_ind, mail=author[2])
            self.affiliation_widget.insertHtml(s)
        self.affiliation_widget.insertHtml("<br>")
        for ind, org in enumerate(organisation):
            ind += 1
            s = "{ind}) {org} <br>".format(ind=ind, org=org)
            self.affiliation_widget.insertHtml(s)
        self.affiliation_widget.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.affiliation_widget)
        self.setLayout(self.main_layout)
        self.setWindowFlag(Qt.Dialog and Qt.MSWindowsFixedSizeDialogHint)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    app = AboutWidget()
    app.show()
    qapp.exec_()
