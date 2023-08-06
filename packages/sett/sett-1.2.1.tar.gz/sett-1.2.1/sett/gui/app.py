from functools import partial
from pathlib import Path
from datetime import datetime
import enum
import html
import operator
import time
import warnings

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QSysInfo
from PySide2.QtGui import QKeySequence

from .component import GuiProgress, FileSelectionWidget, PathInput, TabMixin
from .parallel import Worker
from .model import AppData, TableModel
from .. import __version__, APP_NAME_SHORT, APP_NAME_LONG, protocols
from ..core import crypt
from ..core.error import UserError
from ..core.versioncheck import check_version
from ..workflows import decrypt, encrypt, transfer
from ..utils.config import load_config
from ..__init__ import URL_READTHEDOCS, URL_GITLAB, URL_GITLAB_ISSUES

Key = crypt.gpg.Key

QtCore.QThreadPool.globalInstance().setExpiryTimeout(-1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = APP_NAME_LONG
        self.app_data = AppData(config=load_config())
        self.setWindowTitle(self.title)
        self.add_menu()
        self.add_tabs()
        self.add_status_bar()
        self.check_version()

    def add_tabs(self):
        tab_keys = KeysTab(self)  # FIXME created first to populate gpg keys
        tab_encrypt = EncryptTab(self)
        tab_decrypt = DecryptTab(self)
        tab_transfer = TransferTab(self)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(tab_encrypt, "&Encrypt")
        tabs.addTab(tab_transfer, "&Transfer")
        tabs.addTab(tab_decrypt, "&Decrypt")
        tabs.addTab(tab_keys, "&Keys")

        self.setCentralWidget(tabs)

    def add_status_bar(self):
        self.status = QtWidgets.QStatusBar()
        self.setStatusBar(self.status)

    def add_menu(self):
        action_exit = QtWidgets.QAction(QtGui.QIcon(), '&Exit', self)
        action_exit.setShortcut(QKeySequence('Ctrl+Q'))
        action_exit.setStatusTip('Exit application')
        action_exit.triggered.connect(self.close)

        menu = self.menuBar()
        menu.setNativeMenuBar(QSysInfo.productType() != 'osx')
        menu_file = menu.addMenu("&File")
        menu_file.addAction(action_exit)

        action_help = QtWidgets.QAction(QtGui.QIcon(), "&Documentation", self)
        action_help.setStatusTip('Open online documentation')
        action_help.setShortcut(QKeySequence(QKeySequence.HelpContents))
        action_help.triggered.connect(open_url(URL_READTHEDOCS))

        action_bug_report = QtWidgets.QAction(QtGui.QIcon(),
                                              "&Report an Issue", self)
        action_bug_report.setStatusTip('Open online bug report form')
        action_bug_report.triggered.connect(open_url(URL_GITLAB_ISSUES))

        action_about = QtWidgets.QAction(QtGui.QIcon(), "&About", self)
        action_about.setStatusTip("Show info about application")
        action_about.triggered.connect(self.show_about)

        menu_help = menu.addMenu("&Help")
        menu_help.addAction(action_help)
        menu_help.addAction(action_bug_report)
        menu_help.addAction(action_about)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self, "Quit", "Are you sure to quit?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def check_version(self):
        if self.app_data.config.offline or not self.app_data.config.check_version:
            return
        def get_warnings():
            with warnings.catch_warnings(record=True) as w:
                check_version(self.app_data.config.repo_url)
                return "\n".join(format(warning.message) for warning in w)
        def show_msg(text):
            msg = QtWidgets.QMessageBox(parent=self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle(f"{self.title}")
            msg.setText(text)
            msg.show()
        worker = Worker(get_warnings)
        worker.signals.result.connect(lambda x: x and show_msg(x))
        QtCore.QThreadPool.globalInstance().start(worker)

    def show_about(self):
        msg = QtWidgets.QMessageBox(parent=self)
        msg.setWindowTitle(f"About {APP_NAME_SHORT}")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setTextFormat(QtCore.Qt.RichText)
        msg.setText(
            f"{APP_NAME_LONG}<br>"
            f"Version {__version__}<br><br>"
            f"For documentation go to "
            f"<a href='{URL_READTHEDOCS}'>{URL_READTHEDOCS}</a><br>"
            f"To report an issue go to "
            f"<a href='{URL_GITLAB_ISSUES}'>{URL_GITLAB_ISSUES}</a><br>"
            f"Source code is available at "
            f"<a href='{URL_GITLAB}'>{URL_GITLAB}</a><br><br>"
            f"{APP_NAME_SHORT} is developed as part of the "
            f"<a href='https://sphn.ch'>Swiss Personalized Health Network "
            f"initiative</a>")
        msg.show()


class EncryptTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data

        files_panel = self.create_files_panel()
        user_panel = self.create_user_panel()
        output_panel = self.create_output_panel()
        self.create_run_panel("Package and Encrypt data", self.encrypt,
                              "Package && Encrypt")
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(files_panel)

        layout_split = QtWidgets.QHBoxLayout()
        layout_split.addWidget(user_panel)
        layout_split.addWidget(output_panel)
        layout.addLayout(layout_split)

        layout.addWidget(self.run_panel)
        layout.addWidget(self.console)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def create_files_panel(self):
        box = FileSelectionWidget(
            "Select files and/or directories to encrypt", self)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "encrypt_files", box.get_list()))
        return box

    def create_user_panel(self):
        box = QtWidgets.QGroupBox("Select data sender and recipients")
        sender_widget = QtWidgets.QComboBox()
        sender_widget.setModel(self.app_data.priv_keys_model)
        if self.app_data.default_key_index:
            sender_widget.setCurrentIndex(self.app_data.default_key_index)

        recipients_input_view = QtWidgets.QComboBox()
        recipients_input_view.setModel(self.app_data.pub_keys_model)

        recipients_output_view = QtWidgets.QTableView()
        recipients_output_model = TableModel(
            columns=("Name", "Email", "Fingerprint"))
        recipients_output_view.setModel(recipients_output_model)
        recipients_output_view.verticalHeader().hide()
        recipients_output_view.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        recipients_output_view.setSelectionMode(
            QtWidgets.QTableView.SelectionMode.SingleSelection)

        recipients_btn_add = QtWidgets.QPushButton("+")
        recipients_btn_remove = QtWidgets.QPushButton(
            "Remove selected recipients")

        def update_sender(index):
            self.app_data.encrypt_sender = "" if index == -1 else \
                self.app_data.priv_keys_model.get_value(index).fingerprint

        def update_recipients(index):
            self.app_data.encrypt_recipients = [x[2] for x in
                                                index.model().get_data()]

        def add_recipient():
            key = recipients_input_view.model().get_value(
                recipients_input_view.currentIndex())
            row = (key.uids[0].full_name, key.uids[0].email, key.fingerprint)
            recipients_output_model.set_data(
                set(recipients_output_model.get_data()) | set([row]))
            recipients_output_view.resizeColumnsToContents()

        def remove_recipient():
            recipients_output_model.removeRows(
                recipients_output_view.currentIndex().row(), 1)

        # Connect actions
        recipients_btn_add.clicked.connect(add_recipient)
        recipients_btn_remove.clicked.connect(remove_recipient)
        recipients_output_model.dataChanged.connect(update_recipients)
        sender_widget.currentIndexChanged.connect(update_sender)
        # Set the default value for the sender
        update_sender(sender_widget.currentIndex())

        layout = QtWidgets.QVBoxLayout()
        layout_form = QtWidgets.QFormLayout()
        layout_form.addRow("Sender", sender_widget)
        layout_recipients = QtWidgets.QHBoxLayout()
        layout_recipients.addWidget(recipients_input_view)
        layout_recipients.addWidget(recipients_btn_add)
        layout_form.addRow("Recipients", layout_recipients)
        layout.addLayout(layout_form)
        layout.addWidget(recipients_output_view)
        layout.addWidget(recipients_btn_remove)

        box.setLayout(layout)
        return box

    def create_output_panel(self):
        box = QtWidgets.QGroupBox("Select output name and location")
        # Create fields
        project = QtWidgets.QComboBox(box)
        project.setStatusTip(
            "Select project ID from the list or type a different one.")
        try:
            projects = sorted(self.app_data.config.projects_by_id.keys())
            if projects:
                project.addItems(projects)
                setattr(self.app_data, "encrypt_project_id", projects[0])
        except UserError:
            pass
        project.setEditable(True)
        project_validate = QtWidgets.QCheckBox("Validate Project ID")
        project_validate.setChecked(self.app_data.encrypt_project_id_validate)
        compress = QtWidgets.QCheckBox("Compress inner tarball")
        compress.setChecked(self.app_data.encrypt_compress)
        output_suffix = QtWidgets.QLineEdit(box)
        output_suffix.setStatusTip(
            "File name suffix in the format datetime_suffix.tar")
        output_suffix.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r"[\w-]*")))
        output_location = PathInput()
        # Add actions
        project.currentTextChanged.connect(lambda text:
            setattr(self.app_data, "encrypt_project_id", text))
        project_validate.stateChanged.connect(lambda state:
            setattr(self.app_data, "encrypt_project_id_validate",
                    state == QtCore.Qt.Checked))
        compress.stateChanged.connect(lambda state:
            setattr(self.app_data, "encrypt_compress",
                    state == QtCore.Qt.Checked))
        output_suffix.editingFinished.connect(
            lambda: setattr(self.app_data, "encrypt_output_suffix",
                            output_suffix.text()))
        output_location.on_path_change(
            partial(setattr, self.app_data, "encrypt_output_location"))

        layout = QtWidgets.QFormLayout()
        layout.addRow("Project ID", project)
        layout.addRow("", project_validate)
        layout.addRow("", compress)
        layout.addRow("Output suffix", output_suffix)
        layout.addRow("Output location", output_location.text)
        layout.addRow("", output_location.btn)
        box.setLayout(layout)
        return box

    def encrypt(self, dry_run=False):
        warning_msg = []
        if not self.app_data.encrypt_files:
            warning_msg.append("Select files for encryption.")
        if not self.app_data.encrypt_recipients:
            warning_msg.append("Select at least one recipient.")
        if warning_msg:
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText("\n".join(warning_msg))
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()
            return

        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)
        output_path = str(
            self.app_data.encrypt_output_location /
            "_".join(filter(None,
                            [datetime.now().astimezone().strftime(
                                encrypt.DATE_FMT_FILENAME),
                             self.app_data.encrypt_output_suffix])))
        if not dry_run and self.app_data.config.sign_encrypted_data:
            pw = run_dialog(self, "Enter password for your GPG key")
            if pw is None:
                return
        else:
            pw = None
        worker = Worker(
            encrypt.encrypt,
            self.app_data.encrypt_files,
            logger=(encrypt.logger,),
            sender=self.app_data.encrypt_sender,
            recipient=self.app_data.encrypt_recipients,
            project_id=self.app_data.encrypt_project_id,
            config=self.app_data.config,
            passphrase=pw,
            output_name=output_path,
            dry_run=dry_run,
            offline=not self.app_data.encrypt_project_id_validate,
            compress=self.app_data.encrypt_compress,
            progress=progress,
            on_error=lambda: None)
        self.add_worker_actions(worker)
        self.threadpool.start(worker)


class DecryptTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data

        files_panel = self.create_files_panel()
        decrypt_options_panel = self.create_decrypt_options_panel()
        self.create_run_panel("Decrypt data", self.decrypt,
                              "Decrypt selected files")
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(files_panel, 0, 0, 1, 2)
        layout.addWidget(decrypt_options_panel, 1, 0, 1, 2)
        layout.addWidget(self.run_panel, 2, 0, 1, 2)
        layout.addWidget(self.console, 3, 0, 1, 2)
        layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        self.setLayout(layout)

    def create_files_panel(self):
        box = FileSelectionWidget("Select files to decrypt",
                                  self, directory=False, archives_only=True)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "decrypt_files", box.get_list()))
        return box

    def create_decrypt_options_panel(self):
        box = QtWidgets.QGroupBox("Select data decryption options")

        group_extract = QtWidgets.QButtonGroup(box)
        btn_decrypt_and_extract = QtWidgets.QRadioButton(
            "Decrypt and unpack files")
        btn_decrypt_and_extract.setChecked(
            not self.app_data.decrypt_decrypt_only)
        btn_decrypt_only = QtWidgets.QRadioButton("Decrypt only")
        btn_decrypt_only.toggled.connect(
            lambda: setattr(self.app_data, "decrypt_decrypt_only",
                            btn_decrypt_only.isChecked()))
        group_extract.addButton(btn_decrypt_and_extract)
        group_extract.addButton(btn_decrypt_only)
        output_location = PathInput()
        output_location.on_path_change(
            partial(setattr, self.app_data, "decrypt_output_location"))

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(btn_decrypt_and_extract, 0, 0)
        layout.addWidget(btn_decrypt_only, 1, 0)
        layout.addWidget(QtWidgets.QLabel("Output location"), 2, 0)
        layout.addWidget(output_location.text, 2, 1)
        layout.addWidget(output_location.btn, 2, 2)
        box.setLayout(layout)
        return box

    def decrypt(self, dry_run=False):
        if not self.app_data.decrypt_files:
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText("Select files for decryption.")
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()
            return
        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)
        if not dry_run:
            pw = run_dialog(self, "Enter password for your GPG key")
            if pw is None:
                return
        else:
            pw = None
        worker = Worker(
            decrypt.decrypt,
            files=self.app_data.decrypt_files,
            logger=(decrypt.logger,),
            output_dir=str(self.app_data.decrypt_output_location),
            config=self.app_data.config,
            decrypt_only=self.app_data.decrypt_decrypt_only,
            passphrase=pw,
            dry_run=dry_run,
            progress=progress,
            on_error=lambda: None)
        self.add_worker_actions(worker)
        self.threadpool.start(worker)


class TransferTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data
        self.app_data.transfer_protocol_args = {"sftp": {},
                                                "liquid_files": {}}

        files_panel = self.create_files_panel()
        options_panel = self.create_options_panel()
        self.create_run_panel("Transfer data", self.transfer,
                              "Transfer selected files")
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(files_panel, 0, 0, 1, 2)
        layout.addWidget(options_panel, 1, 0, 1, 2)
        layout.addWidget(self.run_panel, 2, 0, 1, 2)
        layout.addWidget(self.console, 3, 0, 1, 2)
        layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        self.setLayout(layout)

    def create_files_panel(self):
        box = FileSelectionWidget("Select encrypted files to transfer",
                                  self, directory=False, archives_only=True)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "transfer_files", box.get_list()))
        return box

    def create_sftp_options_panel(self):
        field_mapping = FieldMapping()

        text_username = field_mapping.bind_text("username", QtWidgets.QLineEdit())
        text_destination_dir = field_mapping.bind_text("destination_dir", QtWidgets.QLineEdit())
        text_username.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "username", text_username.text()))
        text_host = field_mapping.bind_text("host", QtWidgets.QLineEdit())
        text_host.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                            "host", text_host.text()))
        text_jumphost = field_mapping.bind_text("jumphost", QtWidgets.QLineEdit())
        text_jumphost.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "jumphost", text_jumphost.text() or None))
        text_destination_dir.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                            "destination_dir", text_destination_dir.text()))
        pkey_location = field_mapping.bind_path("pkey", PathInput(directory=False, path=None))
        pkey_location.btn_label = "Select private key"
        pkey_location.on_path_change(lambda path:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "pkey", "" if path is None else str(path)))
        pkey_password = field_mapping.bind_text("pkey_password", QtWidgets.QLineEdit())
        pkey_password.setEchoMode(QtWidgets.QLineEdit.Password)
        pkey_password.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "pkey_password", pkey_password.text()))

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("User name"), 0, 0)
        layout.addWidget(text_username, 0, 1)
        layout.addWidget(QtWidgets.QLabel("Host URL"), 1, 0)
        layout.addWidget(text_host, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Jumphost URL (if needed)"), 2, 0)
        layout.addWidget(text_jumphost, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Destination directory"), 3, 0)
        layout.addWidget(text_destination_dir, 3, 1)
        layout.addWidget(QtWidgets.QLabel("SSH key location (optional)"), 4, 0)
        layout.addWidget(pkey_location.text, 4, 1)
        layout.addWidget(pkey_location.btn, 4, 2)
        layout.addWidget(pkey_location.btn_clear, 4, 3)
        layout.addWidget(QtWidgets.QLabel("SSH key password (optional)"), 5, 0)
        layout.addWidget(pkey_password, 5, 1)
        box = QtWidgets.QGroupBox("Parameters")
        box.setFlat(True)
        box.setLayout(layout)
        box.load_connection = field_mapping.load
        return box

    def create_liquidfiles_options_panel(self):
        field_mapping = FieldMapping()
        text_host = field_mapping.bind_text("host", QtWidgets.QLineEdit())
        text_api_key = field_mapping.bind_text("api_key", QtWidgets.QLineEdit())
        text_host.editingFinished.connect(lambda: operator.setitem(
            self.app_data.transfer_protocol_args["liquid_files"], "host",
            text_host.text()))
        text_api_key.editingFinished.connect(lambda: operator.setitem(
            self.app_data.transfer_protocol_args["liquid_files"],
            "api_key", text_api_key.text()))
        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Host URL"), 0, 0)
        layout.addWidget(text_host, 0, 1)
        layout.addWidget(QtWidgets.QLabel("API Key"), 1, 0)
        layout.addWidget(text_api_key, 1, 1)
        box = QtWidgets.QGroupBox("Parameters")
        box.setFlat(True)
        box.setLayout(layout)
        box.load_connection = field_mapping.load
        return box

    def create_options_panel(self):
        box = QtWidgets.QGroupBox("Select data transfer options")

        connections_selection = QtWidgets.QComboBox(box)
        connections_selection.addItems(list(self.app_data.config.connections))

        protocol_selection = QtWidgets.QComboBox(box)
        protocol_selection.addItems(["sftp", "liquid_files"])

        box_sftp = self.create_sftp_options_panel()
        box_liquidfiles = self.create_liquidfiles_options_panel()
        boxes = {"sftp": box_sftp, "liquid_files": box_liquidfiles}
        box_liquidfiles.hide()

        def load_connection():
            connection = self.app_data.config.connections.get(connections_selection.currentText())
            if not connection:
                return
            protocol_selection.setCurrentText(connection.protocol)
            box = boxes[connection.protocol]
            box.load_connection(connection.parameters)
            self.app_data.transfer_protocol_args[self.app_data.transfer_protocol_name].update(
                connection.parameters)
        connections_selection.currentIndexChanged.connect(load_connection)

        protocol_selection.currentTextChanged.connect(lambda text:
            (setattr(self.app_data, "transfer_protocol_name", text),
            box_sftp.setVisible(
                not box_sftp.isVisible()),
                box_liquidfiles.setVisible(not box_liquidfiles.isVisible())))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Predefined connections"))
        layout.addWidget(connections_selection)
        layout.addWidget(QtWidgets.QLabel("Protocol"))
        layout.addWidget(protocol_selection)
        layout.addWidget(box_sftp)
        layout.addWidget(box_liquidfiles)
        box.setLayout(layout)
        load_connection()
        return box

    def transfer(self, dry_run=False):
        if not self.app_data.transfer_files:
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText("Select files for transfer.")
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()
            return
        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)

        second_factor = None

        class Msg(enum.Enum):
            code = enum.auto()

        class MsgSignal(QtCore.QObject):
            msg = QtCore.Signal(object)

        msg_signal = MsgSignal()

        def second_factor_callback():
            msg_signal.msg.emit(Msg.code)
            time_start = time.time()
            timeout = 120
            while time.time() - time_start < timeout:
                time.sleep(1)
                if second_factor is not None:
                    break
            return second_factor

        def show_second_factor_dialog(msg: str):
            nonlocal second_factor
            second_factor = None
            if msg == Msg.code:
                output = run_dialog(self, "Verification code", password=False)
                second_factor = "" if output is None else output

        worker = Worker(
            transfer.transfer,
            files=self.app_data.transfer_files,
            logger=(transfer.logger, protocols.sftp.logger),
            protocol=protocols.protocols_by_name[
                self.app_data.transfer_protocol_name],
            protocol_args=self.app_data.transfer_protocol_args[
                self.app_data.transfer_protocol_name],
            config=self.app_data.config,
            dry_run=dry_run,
            progress=progress,
            on_error=lambda: None,
            two_factor_callback=second_factor_callback)
        self.add_worker_actions(worker)
        msg_signal.msg.connect(show_second_factor_dialog)
        self.threadpool.start(worker)


class KeyGenDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.setWindowTitle("Generate new key pair")
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.text_name_full = QtWidgets.QLineEdit()
        self.text_name_extra = QtWidgets.QLineEdit()
        self.text_email = QtWidgets.QLineEdit()
        self.text_pass = QtWidgets.QLineEdit()
        self.text_pass_repeat = QtWidgets.QLineEdit()
        self.toggle_password_visibility(False)

        re_email = QtCore.QRegExp(r"[^@]+@[^@]+\.[^@]+")
        self.text_email.setValidator(QtGui.QRegExpValidator(re_email))

        self.btn_run = QtWidgets.QPushButton("Generate key")
        self.btn_run.setDefault(True)
        self.btn_run.clicked.connect(self.create_private_key)
        btn_cancel = QtWidgets.QPushButton("Close")
        btn_cancel.clicked.connect(self.close)
        btn_show_pass = QtWidgets.QPushButton("Show")
        btn_show_pass.setCheckable(True)
        btn_show_pass.clicked[bool].connect(self.toggle_password_visibility)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Full name"), 0, 0)
        layout.addWidget(self.text_name_full, 0, 1)
        layout.addWidget(QtWidgets.QLabel("(optional) institution/project"), 1, 0)
        layout.addWidget(self.text_name_extra, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Institutional email"), 2, 0)
        layout.addWidget(self.text_email, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Password"), 3, 0)
        layout.addWidget(self.text_pass, 3, 1)
        layout.addWidget(QtWidgets.QLabel("Password (repeat)"), 4, 0)
        layout.addWidget(self.text_pass_repeat, 4, 1)
        layout.addWidget(btn_show_pass, 4, 2)
        layout.addWidget(btn_cancel, 5, 0)
        layout.addWidget(self.btn_run, 5, 1)
        layout.addWidget(
            QtWidgets.QLabel("Key generation can take a few minutes"),
            6, 0, 1, 3)
        self.setLayout(layout)

    def toggle_password_visibility(self, show: bool):
        mode = (QtWidgets.QLineEdit.Normal if show else
                QtWidgets.QLineEdit.Password)
        self.text_pass.setEchoMode(mode)
        self.text_pass_repeat.setEchoMode(mode)

    def clear_form(self):
        self.text_name_full.clear()
        self.text_name_extra.clear()
        self.text_email.clear()
        self.text_pass.clear()
        self.text_pass_repeat.clear()

    def post_key_creation(self, key: Key):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("GPG Key Generation")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        try:
            revocation_cert = crypt.create_revocation_certificate(
                key.fingerprint, self.text_pass.text(),
                self.parent().app_data.config.gpg_store)
            msg.setText(
                "Your new key has been successfully generated.\n\n"
                "Additionally, a revocation certificate was also created. "
                "It can be used to revoke your key in the eventuality that it "
                "gets compromised, lost, or that you forgot your password.\n"
                "Please store the revocation certificate below in a safe "
                "location, as anyone can use it to revoke your key.")
            msg.setDetailedText(revocation_cert.decode())
            # Programatically click the "Show Details..." button so that the
            # certificate is shown by default.
            click_show_details(msgbox=msg)

        except UserError:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(
                "Key has been successfully generated. "
                "However, it was not possible to create a revocation "
                "certificate. "
                "Execute the following command to create the certificate\n\n"
                f"gpg --gen-revoke {key.fingerprint}"
            )
        finally:
            msg.exec_()
            self.clear_form()
            self.parent().update_private_keys()
            self.parent().update_public_keys()
            self.close()

    def create_private_key(self):
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG Key Generation Error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        self.btn_run.setEnabled(False)
        full_name = (f"{self.text_name_full.text()} "
                     f"{self.text_name_extra.text()}")
        worker = Worker(crypt.create_key,
                        full_name,
                        self.text_email.text(),
                        self.text_pass.text(),
                        self.text_pass_repeat.text(),
                        self.parent().app_data.config.gpg_store)
        worker.signals.result.connect(self.post_key_creation)
        worker.signals.error.connect(lambda e: (
            msg_warn.setText(format(e[1])), msg_warn.exec_()))
        worker.signals.finished.connect(
            lambda: self.btn_run.setEnabled(True))
        self.threadpool.start(worker)


class KeyDownloadDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.setWindowTitle("Download public keys from the server")
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.search_string = QtWidgets.QLineEdit()
        self.btn_search = QtWidgets.QPushButton("Search")
        self.btn_search.clicked.connect(self.search_keys)

        self.key_list_view = QtWidgets.QListView()
        key_list_model = QtCore.QStringListModel()
        self.key_list_view.setModel(key_list_model)

        self.btn_download = QtWidgets.QPushButton("Download")
        self.btn_download.clicked.connect(self.download_selected)

        btn_cancel = QtWidgets.QPushButton("Close")
        btn_cancel.clicked.connect(self.close)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(
            QtWidgets.QLabel(
                "Enter a search term (e.g. user name, email, key "
                "fingerprint)"),
            0, 0)
        layout.addWidget(self.search_string, 1, 0)
        layout.addWidget(self.btn_search, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Select a key to download"), 2, 0)
        layout.addWidget(self.key_list_view, 3, 0)
        layout.addWidget(self.btn_download, 3, 1)
        layout.addWidget(btn_cancel, 4, 1)
        self.setLayout(layout)

    def search_keys(self):
        self.btn_search.setEnabled(False)
        self.key_list_view.model().setStringList([])
        worker = Worker(crypt.search_keyserver, self.search_string.text(),
                        self.parent().app_data.config.keyserver_url)
        worker.signals.result.connect(
            lambda keys: self.key_list_view.model().setStringList(
                [f"{k.uid} {k.fingerprint}" for k in keys]))
        worker.signals.finished.connect(
            lambda: self.btn_search.setEnabled(True))
        self.threadpool.start(worker)

    def download_selected(self):
        key_ids = []
        for index in self.key_list_view.selectedIndexes():
            key_ids.append(index.model().data(index).split()[-1])
        if key_ids:
            self.btn_download.setEnabled(False)
            worker = Worker(crypt.download_keys, key_ids,
                            self.parent().app_data.config.keyserver_url,
                            self.parent().app_data.config.gpg_store)
            worker.signals.result.connect(
                lambda x: self.parent().update_public_keys())
            worker.signals.finished.connect(
                lambda: self.btn_download.setEnabled(True))
            self.threadpool.start(worker)


class KeysTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data
        self.update_private_keys()
        self.update_public_keys()

        self.text_panel = QtWidgets.QTextEdit()
        self.text_panel.setReadOnly(True)

        self.priv_keys_view = QtWidgets.QListView()
        self.priv_keys_view.setModel(self.app_data.priv_keys_model)
        self.priv_keys_view.selectionModel().currentChanged.connect(
            self._update_display)

        self.pub_keys_view = QtWidgets.QListView()
        self.pub_keys_view.setModel(self.app_data.pub_keys_model)
        self.pub_keys_view.selectionModel().currentChanged.connect(
            self._update_display)
        self.pub_keys_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)

        # When item is selected clear selection in the other list
        self.priv_keys_view.selectionModel().currentChanged.connect(
            lambda: self.pub_keys_view.selectionModel().clear())
        self.pub_keys_view.selectionModel().currentChanged.connect(
            lambda: self.priv_keys_view.selectionModel().clear())

        btn_generate = QtWidgets.QPushButton("Generate new private/public key")
        btn_generate.clicked.connect(
            lambda: KeyGenDialog(parent=self).show())
        btn_group_public = self.create_public_keys_btn_group()
        btn_refresh = QtWidgets.QPushButton("Refresh keys")
        btn_refresh.setStatusTip("Refresh keys from the local keyring")
        btn_refresh.clicked.connect(
            lambda x: (self.update_private_keys(),
                       self.update_public_keys(),
                       self._update_display(
                           self.pub_keys_view.selectionModel().currentIndex()))
            )

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Private keys"), 0, 0)
        layout.addWidget(self.priv_keys_view, 1, 0)
        layout.addWidget(btn_generate, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Public keys"), 2, 0)
        layout.addWidget(self.pub_keys_view, 3, 0)
        layout.addLayout(btn_group_public, 3, 1)
        layout.addWidget(self.text_panel, 4, 0)
        layout.addWidget(btn_refresh, 4, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        self.setLayout(layout)

    def key_to_html(self, key: Key) -> str:
        content = []
        content.append("<table>")
        rows = [("User ID", html.escape(str(key.uids[0]))),
                ("Key ID", key.key_id),
                ("Key fingerprint", key.fingerprint),
                ("Key length", key.key_length)]
        for k, v in rows:
            content.append(f"<tr><th>{k}</th><td>{v}</td></tr>")

        content.append("<tr><th>Signatures</th><td>")
        content.append("<br>".join(
            [f"{html.escape(str(sig.issuer_uid))} {sig.issuer_key_id} {sig.signature_class}"
                for sig in key.valid_signatures]))
        content.append("</td></tr>")

        content.append("</table>")
        if key.key_type == crypt.gpg.KeyType.public:
            try:
                crypt.validate_pub_key(
                    key,
                    validation_keyid=self.app_data.config.key_validation_authority_keyid,
                    keyserver_url=self.app_data.config.keyserver_url)
                content.append(
                    "<p class=\"safe\">This key has been verified</p>")
            except UserError as e:
                content.append(
                    f"<p class=\"danger\">{e}</p>")
        else:
            content.append(
                "<p>This is a private key. "
                "Private keys can not be signed.</p>")
        return "".join(content)

    @staticmethod
    def key_to_text(key: Key) -> str:
        return(f"User ID: {key.uids[0]}\n"
               f"Fingerprint: {key.fingerprint}")

    def create_public_keys_btn_group(self):
        btn_download = QtWidgets.QPushButton("Download keys")
        btn_download.setStatusTip(
            "Search and download keys from the keyserver")
        btn_download.clicked.connect(
            lambda: KeyDownloadDialog(parent=self).show())
        btn_update = QtWidgets.QPushButton("Update keys")
        btn_update.setStatusTip("Update selected key from the keyserver")
        btn_update.clicked.connect(self.update_keys)
        btn_import = QtWidgets.QPushButton("Import key")
        btn_import.setStatusTip("Import key from file")
        btn_import.clicked.connect(self.import_key)
        btn_upload = QtWidgets.QPushButton("Upload keys")
        btn_upload.setStatusTip("Upload selected key to the keyserver")
        btn_upload.clicked.connect(self.upload_key)
        btn_sign = QtWidgets.QPushButton("Request signature")
        btn_sign.setStatusTip("Request signature for the selected keys")
        btn_sign.clicked.connect(self.request_signature)
        btn_delete = QtWidgets.QPushButton("Delete keys")
        btn_delete.setStatusTip("Delete selected keys from your computer")
        btn_delete.clicked.connect(self.delete_keys)

        btn_group_public = QtWidgets.QVBoxLayout()
        btn_group_public.addWidget(btn_download)
        btn_group_public.addWidget(btn_update)
        btn_group_public.addWidget(btn_import)
        btn_group_public.addWidget(btn_upload)
        btn_group_public.addWidget(btn_sign)
        btn_group_public.addWidget(btn_delete)
        return btn_group_public

    def update_private_keys(self):
        # Retrieve all private keys from local keyring.
        keys_private = self.app_data.config.gpg_store.list_sec_keys()
        try:
            default_key = (self.app_data.config.default_sender or
                           self.app_data.config.gpg_store.default_key())
            self.app_data.default_key_index = next(index for index, entry in enumerate(
                keys_private) if entry.fingerprint == default_key)
            self.app_data.encrypt_sender = default_key
        except StopIteration:
            pass
        self.app_data.priv_keys_model.set_data(
            {f"{key.uids[0]} {key.key_id}": key for key in keys_private})

    def update_public_keys(self):
        # Retrieve all public keys from local keyring.
        keys_public = self.app_data.config.gpg_store.list_pub_keys(sigs=True)
        self.app_data.pub_keys_model.set_data(
            {f"{key.uids[0]} {key.key_id}": key for key in keys_public})

    def update_keys(self):
        """Updated selected keys from the keyserver."""
        msg_ok = QtWidgets.QMessageBox()
        msg_ok.setIcon(QtWidgets.QMessageBox.Information)
        msg_ok.setWindowTitle("Updated keys")
        msg_ok.setText("Keys have been successfully updated.")
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key update error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        keys = [index.model().get_value(index).fingerprint for index in
                self.pub_keys_view.selectedIndexes()]
        if keys:
            worker = Worker(crypt.download_keys, keys,
                            self.app_data.config.keyserver_url,
                            self.app_data.config.gpg_store)
            worker.signals.result.connect(
                lambda x: (self.update_public_keys(),
                           self._update_display(
                               self.pub_keys_view.selectionModel().currentIndex()),
                           msg_ok.exec_()))
            worker.signals.error.connect(
                lambda x: (msg_warn.setText(format(x[1])),
                            msg_warn.exec_()))
            self.threadpool.start(worker)

    def import_key(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                     "Select GPG key file",
                                                     str(Path.home()))[0]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("GPG public key import")
        try:
            if path:
                with open(path) as fin:
                    key_data = fin.read()
                crypt.import_keys(key_data, self.app_data.config.gpg_store)
                self.update_public_keys()
                self._update_display(
                    self.pub_keys_view.selectionModel().currentIndex())
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Key has been imported.")
                msg.exec_()
        except (UnicodeDecodeError, UserError) as e:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(format(e))
            msg.exec_()

    def delete_keys(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle("Delete public key")
        msg.setText("Do you really want to delete the following public key?")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key deletion error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        priv_keys = self.app_data.config.gpg_store.list_sec_keys()
        for index in self.pub_keys_view.selectedIndexes():
            key = index.model().get_value(index)
            if any(k for k in priv_keys if key.fingerprint == k.fingerprint):
                msg_warn.setText(
                    f"{key.uids[0]}\n\n"
                    "Deleting private keys (and by extension public keys "
                    "with an associated private key) is not supported by "
                    "this application. Please use an external software such "
                    "as GnuPG (Linux, MacOS) or Kleopatra (Windows).")
                msg_warn.exec_()
                continue
            msg.setDetailedText(self.key_to_text(key))
            click_show_details(msgbox=msg)
            status = msg.exec_()
            if status == QtWidgets.QMessageBox.Ok:
                try:
                    crypt.delete_keys([key.fingerprint],
                                    self.app_data.config.gpg_store)
                except UserError as e:
                    msg_warn.setText(format(e))
                    msg_warn.exec_()
                self.text_panel.clear()
        self.update_public_keys()

    def upload_key(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Send public key")
        msg.setText(
            "Do you want to upload the selected key to the key server?")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_ok = QtWidgets.QMessageBox()
        msg_ok.setIcon(QtWidgets.QMessageBox.Information)
        msg_ok.setWindowTitle("Send public key")
        msg_ok.setText("Key has been successfully uploaded to the keyserver.")
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key upload error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        for index in self.pub_keys_view.selectedIndexes():
            key = index.model().get_value(index)
            msg.setDetailedText(self.key_to_text(key))
            click_show_details(msgbox=msg)
            status = msg.exec_()
            if status == QtWidgets.QMessageBox.Ok:
                worker = Worker(crypt.upload_keys, [key.fingerprint],
                                self.app_data.config.keyserver_url,
                                self.app_data.config.gpg_store)
                worker.signals.result.connect(lambda x: msg_ok.exec_())
                worker.signals.error.connect(
                    lambda x: (msg_warn.setText(format(x[1])),
                               msg_warn.exec_()))
                self.threadpool.start(worker)

    def request_signature(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Key signing request")
        msg.setText("Do you want to request signature for the selected key?")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_ok = QtWidgets.QMessageBox()
        msg_ok.setIcon(QtWidgets.QMessageBox.Information)
        msg_ok.setWindowTitle("Key signing request")
        msg_ok.setText("Key signing request has been sent.")
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("Key signing request")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        for index in self.pub_keys_view.selectedIndexes():
            key = index.model().get_value(index)
            msg.setDetailedText(self.key_to_text(key))
            click_show_details(msgbox=msg)
            status = msg.exec_()
            if status == QtWidgets.QMessageBox.Ok:
                worker = Worker(
                    crypt.request_key_signature, key.key_id,
                    self.app_data.config.dcc_portal_pgpkey_endpoint_url)
                worker.signals.result.connect(lambda x: msg_ok.exec_())
                worker.signals.error.connect(
                    lambda x: (msg_warn.setText(format(x[1])),
                               msg_warn.exec_()))
                self.threadpool.start(worker)

    def _update_display(self, index: QtCore.QModelIndex):
        style = (
            "<style>"
            "th {text-align: left; padding: 0 20px 5px 0;}"
            ".danger { color: red;}"
            ".safe { color: green;}"
            "</style>"
        )
        if index.isValid():
            try:
                self.text_panel.setHtml(
                    style + self.key_to_html(index.model().get_value(index)))
            except IndexError:
                self.text_panel.setHtml("")

def run_dialog(parent, msg: str, password: bool = True):
    dialog_pwd = QtWidgets.QInputDialog(parent)
    dialog_pwd.setLabelText(msg)
    dialog_pwd.setWindowTitle("SETT")
    if password:
        dialog_pwd.setTextEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    if dialog_pwd.exec_() != QtWidgets.QDialog.Accepted or not dialog_pwd.textValue():
        return None
    return dialog_pwd.textValue()

class FieldMapping:
    def __init__(self):
        self._mapping = {}

    def bind_text(self, field_name, w):
        self._mapping[field_name] = w.setText
        return w

    def bind_path(self, field_name, w):
        self._mapping[field_name] = lambda p: w.update_path(Path(p))
        return w

    def load(self, parameters):
        for key, val in parameters.items():
            try:
                self._mapping[key](val)
            except KeyError:
                raise ValueError(f"Invalid field `{key}` found in your config file")

def click_show_details(msgbox: QtWidgets.QMessageBox):
    for button in msgbox.buttons():
        if msgbox.buttonRole(button) is \
        QtWidgets.QMessageBox.ButtonRole.ActionRole:
            button.click()

def open_url(url: str):
    """Retruns a function that will opens the specified URL in the user's
    default browser when called. The function that is returned has no
    arguments.
    :param url: URL to open.
    :returns: function that opens specifed URL.
    """
    def open_url_template():
        if not QtGui.QDesktopServices.openUrl(QtCore.QUrl(url)):
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText(f"Unable to open URL at \n{url}.")
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()
    return open_url_template
