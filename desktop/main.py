import sys
import os
import webbrowser
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
    QFrame, QMessageBox, QStackedWidget, QDialog, QLineEdit, QHeaderView
)
from PyQt5.QtCore import Qt

from api_client import login, upload_csv, get_history, download_report
from charts import MplCanvas


# ---------------- UTIL ----------------
def safe(x):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.2f}"
    return str(x)


def format_datetime(ts):
    try:
        dt = datetime.fromisoformat(ts.replace("Z", ""))
        return dt.strftime("%d %b %Y  %I:%M %p")
    except Exception:
        return ts


def qss():
    return """
    QWidget{
      background:#0f1220;
      color:#ffffff;
      font-family:Segoe UI;
      font-size:15px;
    }

    QLabel#Title{
      font-size:30px;
      font-weight:800;
      color:#8b5cf6;
    }
    QLabel#Muted{ color:#9aa3b2; }

    QPushButton{
      background:#3b82f6;
      border:none;
      padding:12px 18px;
      border-radius:12px;
      font-weight:700;
    }
    QPushButton:hover{ background:#2563eb; }

    QPushButton#Nav{
      background:transparent;
      color:#9aa3b2;
      text-align:left;
      padding:14px 18px;
    }
    QPushButton#Nav:hover{
      background:rgba(59,130,246,0.15);
      color:#ffffff;
    }

    QPushButton#Danger{
      background:transparent;
      border:1px solid #ef4444;
      color:#ef4444;
    }
    QPushButton#Danger:hover{
      background:#ef4444;
      color:#ffffff;
    }

    QFrame#Card{
      background:#171a2b;
      border:1px solid #262a40;
      border-radius:18px;
    }

    QTableWidget{
      background:#111426;
      border:1px solid #262a40;
      border-radius:12px;
    }

    QHeaderView::section{
      background:#171a2b;
      color:#9aa3b2;
      font-weight:800;
      padding:10px;
      border:none;
    }
    """


# ---------------- BASIC CARD ----------------
class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")


# ---------------- LOGIN ----------------
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 28, 26, 28)
        layout.setSpacing(16)

        title = QLabel("Login")
        title.setStyleSheet("font-size:26px;font-weight:800;color:#6366f1;")
        layout.addWidget(title)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")
        self.user.setMinimumHeight(46)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setMinimumHeight(46)

        layout.addWidget(self.user)
        layout.addWidget(self.pwd)

        self.status = QLabel("")
        self.status.setStyleSheet("color:#fb7185;font-size:13px;")
        layout.addWidget(self.status)

        layout.addSpacing(6)

        btn = QPushButton("Login")
        btn.setMinimumHeight(50)
        btn.clicked.connect(self.do_login)
        layout.addWidget(btn)

        layout.addStretch()

    def do_login(self):
        if not self.user.text().strip() or not self.pwd.text().strip():
            self.status.setText("Enter username and password")
            return
        try:
            login(self.user.text(), self.pwd.text())
            self.accept()
        except Exception as e:
            self.status.setText(str(e))


# ---------------- DASHBOARD ----------------
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemInSight")
        self.resize(1440, 880)
        self.file_path = None

        root = QHBoxLayout(self)
        root.setSpacing(18)

        # -------- LEFT SIDEBAR --------
        side = QVBoxLayout()
        side.setSpacing(8)

        logo = QLabel("ChemInSight")
        logo.setObjectName("Title")
        side.addWidget(logo)

        sub = QLabel("Desktop Analytics")
        sub.setObjectName("Muted")
        side.addWidget(sub)

        side.addSpacing(20)

        self.btn_overview = QPushButton("📊  Overview")
        self.btn_history = QPushButton("📁  History")
        self.btn_graphs = QPushButton("📈  Graphs")

        for b in (self.btn_overview, self.btn_history, self.btn_graphs):
            b.setObjectName("Nav")
            side.addWidget(b)

        side.addStretch()

        logout = QPushButton("Logout")
        logout.setObjectName("Danger")
        logout.clicked.connect(QApplication.quit)
        side.addWidget(logout)

        side_frame = QWidget()
        side_frame.setLayout(side)
        side_frame.setFixedWidth(220)
        root.addWidget(side_frame)

        # -------- MAIN --------
        main = QVBoxLayout()
        root.addLayout(main, 1)

        header = QHBoxLayout()
        header.addStretch()

        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("Muted")

        self.choose_btn = QPushButton("Choose CSV")
        self.choose_btn.clicked.connect(self.pick_file)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.do_upload)

        header.addWidget(self.file_label)
        header.addWidget(self.choose_btn)
        header.addWidget(self.upload_btn)
        main.addLayout(header)

        self.status = QLabel("")
        self.status.setObjectName("Muted")
        main.addWidget(self.status)

        self.stack = QStackedWidget()
        main.addWidget(self.stack, 1)

        self.stack.addWidget(self.build_overview())
        self.stack.addWidget(self.build_history())
        self.stack.addWidget(self.build_graphs())

        self.btn_overview.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_history.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_graphs.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        self.load_data()

    # -------- OVERVIEW --------
    def build_overview(self):
        w = QWidget()
        g = QGridLayout(w)
        g.setSpacing(18)

        self.kpi_card = Card()
        k = QGridLayout(self.kpi_card)

        self.kpi_total = self.make_kpi("TOTAL", "-")
        self.kpi_flow = self.make_kpi("FLOW", "-")
        self.kpi_pressure = self.make_kpi("PRESSURE", "-")
        self.kpi_temp = self.make_kpi("TEMP", "-")

        k.addWidget(self.kpi_total, 0, 0)
        k.addWidget(self.kpi_flow, 0, 1)
        k.addWidget(self.kpi_pressure, 1, 0)
        k.addWidget(self.kpi_temp, 1, 1)

        self.report_btn = QPushButton("Download Report")
        self.report_btn.setMinimumHeight(50)
        self.report_btn.clicked.connect(self.download_report_file)
        k.addWidget(self.report_btn, 2, 0, 1, 2)

        self.bar_card = Card()
        b = QVBoxLayout(self.bar_card)
        b.addWidget(QLabel("Equipment Distribution"))
        self.bar_canvas = MplCanvas()
        b.addWidget(self.bar_canvas, 1)

        g.addWidget(self.kpi_card, 0, 0)
        g.addWidget(self.bar_card, 0, 1)
        return w

    # -------- HISTORY --------
    def build_history(self):
        w = QWidget()
        l = QVBoxLayout(w)

        card = Card()
        c = QVBoxLayout(card)
        c.addWidget(QLabel("Upload History (Last 5)"))

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Filename", "Uploaded At", "Total", "Avg Flow"]
        )
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        c.addWidget(self.table)
        l.addWidget(card)
        return w

    # -------- GRAPHS --------
    def build_graphs(self):
        w = QWidget()
        l = QVBoxLayout(w)

        self.pie_card = Card()
        p = QVBoxLayout(self.pie_card)
        p.addWidget(QLabel("Equipment Distribution"))
        self.pie_canvas = MplCanvas()
        p.addWidget(self.pie_canvas, 1)

        self.line_card = Card()
        ln = QVBoxLayout(self.line_card)
        ln.addWidget(QLabel("Trends"))
        self.line_canvas = MplCanvas()
        ln.addWidget(self.line_canvas, 1)

        l.addWidget(self.pie_card, 1)
        l.addWidget(self.line_card, 1)
        return w

    # -------- HELPERS --------
    def make_kpi(self, label, value):
        box = QFrame()
        box.setStyleSheet(
            "background:#111426;border:1px solid #262a40;border-radius:14px;"
        )
        lay = QVBoxLayout(box)
        lay.setAlignment(Qt.AlignCenter)
        t = QLabel(label)
        t.setStyleSheet("color:#9aa3b2;font-weight:700;")
        v = QLabel(value)
        v.setStyleSheet("font-size:26px;font-weight:900;")
        lay.addWidget(t)
        lay.addWidget(v)
        box._value = v
        return box

    # -------- FILE --------
    def pick_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if path:
            self.file_path = path
            self.file_label.setText(os.path.basename(path))

    def do_upload(self):
        if not self.file_path:
            self.status.setText("Please select a CSV file first")
            return

        try:
            self.status.setText("Uploading...")
            upload_csv(self.file_path)
            self.status.setText("Uploaded successfully ✓")
            self.file_label.setText("No file selected")
            self.file_path = None
            self.load_data()
        except Exception as e:
            self.status.setText(str(e))

    # -------- DATA --------
    def load_data(self):
        data = get_history()
        if not data:
            return

        latest = data[0]["summary"]

        self.kpi_total._value.setText(safe(latest["total_equipment"]))
        self.kpi_flow._value.setText(safe(latest["avg_flowrate"]))
        self.kpi_pressure._value.setText(safe(latest["avg_pressure"]))
        self.kpi_temp._value.setText(safe(latest["avg_temperature"]))

        self.table.setRowCount(min(5, len(data)))
        for r, item in enumerate(data[:5]):
            s = item["summary"]
            self.table.setItem(r, 0, QTableWidgetItem(item["filename"]))
            self.table.setItem(r, 1, QTableWidgetItem(format_datetime(item["uploaded_at"])))
            self.table.setItem(r, 2, QTableWidgetItem(str(s["total_equipment"])))
            self.table.setItem(r, 3, QTableWidgetItem(str(s["avg_flowrate"])))

        dist = latest.get("type_distribution", {})
        self.bar_canvas.bar(list(dist.keys()), list(dist.values()), "Equipment Distribution")
        self.pie_canvas.bar(list(dist.keys()), list(dist.values()), "Equipment Distribution")

        ordered = list(reversed(data[:5]))
        self.line_canvas.lines(
            [f"#{i+1}" for i in range(len(ordered))],
            {
                "Flow": [d["summary"]["avg_flowrate"] for d in ordered],
                "Pressure": [d["summary"]["avg_pressure"] for d in ordered],
                "Temp": [d["summary"]["avg_temperature"] for d in ordered],
            },
            "Trends",
        )

    # -------- DOWNLOAD --------
    def download_report_file(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "report.pdf", "PDF Files (*.pdf)"
        )
        if not save_path:
            return
        download_report(save_path)
        QMessageBox.information(self, "Success", "Report downloaded successfully")
        webbrowser.open(save_path)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qss())

    dlg = LoginDialog()
    if dlg.exec_() != QDialog.Accepted:
        sys.exit(0)

    w = Dashboard()
    w.show()
    sys.exit(app.exec_())
