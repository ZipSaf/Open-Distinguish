from PySide6.QtCore import Qt, QSettings, QUrl
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QPushButton,
    QVBoxLayout, QWidget, QStatusBar, QStackedWidget, QLabel,
    QTabWidget, QFormLayout, QComboBox, QFontComboBox, QCheckBox,
    QSlider, QHBoxLayout, QPlainTextEdit
)
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys

class OpenDistinguish(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Open-Distinguish")
        self.setGeometry(100, 100, 900, 600)
        self.setMinimumSize(800, 600)

        # Initialize settings persistence
        self.settings = QSettings("OpenDistinguish", "Distinguish")

        # Browser view and stacked widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Main pages
        self.browser_page = self.setup_browser_page()
        self.settings_page = self.setup_settings_page()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.browser_page)
        self.stacked_widget.addWidget(self.settings_page)

        # Navigation toolbar
        self.nav_bar = self.setup_navbar()
        self.addToolBar(self.nav_bar)

        # Apply saved appearance settings
        self.apply_settings()

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.browser.loadStarted.connect(lambda: self.status.showMessage("Loading..."))
        self.browser.loadFinished.connect(lambda: self.status.clearMessage())
        self.browser.urlChanged.connect(self.update_url_bar)

    def show_browser(self):
        """ Switch to the browser page """
        self.stacked_widget.setCurrentWidget(self.browser_page)

    def setup_browser_page(self):
        browser_page = QWidget()
        browser_layout = QVBoxLayout()
        browser_layout.addWidget(self.browser)
        browser_page.setLayout(browser_layout)
        return browser_page

    def setup_navbar(self):
        nav_bar = QToolBar("Navigation")

        # Back button
        back_button = QPushButton("⬅️")
        back_button.clicked.connect(self.browser.back)
        nav_bar.addWidget(back_button)

        # Forward button
        forward_button = QPushButton("➡️")
        forward_button.clicked.connect(self.browser.forward)
        nav_bar.addWidget(forward_button)

        # Reload button
        reload_button = QPushButton("🔄")
        reload_button.clicked.connect(self.browser.reload)
        nav_bar.addWidget(reload_button)

        # Home button
        home_button = QPushButton("🏠")
        home_button.clicked.connect(lambda: self.browser.setUrl(QUrl(self.settings.value("default_url", "https://www.google.com"))))
        nav_bar.addWidget(home_button)

        # Settings button
        settings_button = QPushButton("⚙️")
        settings_button.clicked.connect(self.show_settings)
        nav_bar.addWidget(settings_button)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        return nav_bar

    def setup_settings_page(self):
        settings_page = QWidget()
        settings_layout = QVBoxLayout()

        # Tabs for different settings sections
        tabs = QTabWidget()

        # Appearance Settings
        appearance_tab = QWidget()
        appearance_layout = QFormLayout()
        
        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Default", "Light", "Ocean Blue", "Forest Green", "Solarized Dark"])
        self.theme_combo.setCurrentText(self.settings.value("theme", "Default"))
        appearance_layout.addRow("Theme", self.theme_combo)

        # Font selector
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.settings.value("font", "Arial")))
        appearance_layout.addRow("Font", self.font_combo)

        # Font Size
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setRange(8, 30)
        self.font_size_slider.setValue(int(self.settings.value("font_size", 14)))
        appearance_layout.addRow("Font Size", self.font_size_slider)

        appearance_tab.setLayout(appearance_layout)
        tabs.addTab(appearance_tab, "Appearance")

        # Customization Tab
        customization_tab = QWidget()
        customization_layout = QFormLayout()

        # Show home button checkbox
        self.show_home_checkbox = QCheckBox("Show Home Button")
        self.show_home_checkbox.setChecked(self.settings.value("show_home", True, type=bool))
        customization_layout.addRow(self.show_home_checkbox)

        # Set Default URL
        self.default_url_input = QLineEdit()
        self.default_url_input.setText(self.settings.value("default_url", "https://www.google.com"))
        customization_layout.addRow("Default Home URL", self.default_url_input)

        customization_tab.setLayout(customization_layout)
        tabs.addTab(customization_tab, "Customization")

        # Privacy Tab
        privacy_tab = QWidget()
        privacy_layout = QFormLayout()

        # JavaScript toggle
        self.javascript_checkbox = QCheckBox("Enable JavaScript")
        self.javascript_checkbox.setChecked(self.settings.value("javascript", True, type=bool))
        privacy_layout.addRow(self.javascript_checkbox)

        # Cookies toggle
        self.cookies_checkbox = QCheckBox("Enable Cookies")
        self.cookies_checkbox.setChecked(self.settings.value("cookies", True, type=bool))
        privacy_layout.addRow(self.cookies_checkbox)

        # Do Not Track toggle
        self.dnt_checkbox = QCheckBox("Enable Do Not Track")
        self.dnt_checkbox.setChecked(self.settings.value("do_not_track", False, type=bool))
        privacy_layout.addRow(self.dnt_checkbox)

        privacy_tab.setLayout(privacy_layout)
        tabs.addTab(privacy_tab, "Privacy")

        # About Tab
        about_tab = QWidget()
        about_layout = QVBoxLayout()
        about_text = QPlainTextEdit()
        about_text.setPlainText("Open-Distinguish\nVersion 1.0.0\n\nCreated by: ZipSaf\n2024")
        about_text.setReadOnly(True)
        about_layout.addWidget(about_text)
        about_tab.setLayout(about_layout)
        tabs.addTab(about_tab, "About")

        # Add save and back buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        exit_button = QPushButton("Back to Browser")
        exit_button.clicked.connect(self.show_browser)
        button_layout.addWidget(save_button)
        button_layout.addWidget(exit_button)

        settings_layout.addWidget(tabs)
        settings_layout.addLayout(button_layout)
        settings_page.setLayout(settings_layout)

        return settings_page

    def apply_settings(self):
        """ Apply appearance settings with high readability """
        self.setStyleSheet("background-color: white; color: black;")  # White background, black text for contrast
        font_size = self.font_size_slider.value()
        font = self.font_combo.currentFont()
        self.setFont(font)
        self.setStyleSheet(f"""
            background-color: white;
            color: black;
            font-size: {font_size}px;
        """)

    def save_settings(self):
        """ Save settings and apply changes """
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("font", self.font_combo.currentFont().family())
        self.settings.setValue("font_size", self.font_size_slider.value())
        self.settings.setValue("default_url", self.default_url_input.text())
        self.apply_settings()
        self.show_browser()

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

app = QApplication(sys.argv)
window = OpenDistinguish()
window.show()
sys.exit(app.exec())
