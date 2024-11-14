import sys
import json
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication as app, QMainWindow as mainW, QStackedWidget as stack, QMessageBox

class MyApp(mainW):  # Sử dụng alias QMainWindow là mainW
    def __init__(self):
        super().__init__()

        # Tải giao diện từ file .ui (register.ui và login.ui)
        self.ui_register = uic.loadUi('register.ui')  # File UI của form đăng ký
        self.ui_login = uic.loadUi('login.ui')        # File UI của form đăng nhập

        # Kết nối sự kiện khi nhấn nút Register
        self.ui_register.btnRegister.clicked.connect(self.register_user)
        
        # Kết nối sự kiện khi nhấn nút Login
        self.ui_login.btnLogin.clicked.connect(self.login_user)

        # Sử dụng QStackedWidget để chuyển đổi giữa các form
        self.stacked_widget = stack()  # Sử dụng alias QStackedWidget là stack
        self.stacked_widget.addWidget(self.ui_register)  # Thêm giao diện đăng ký
        self.stacked_widget.addWidget(self.ui_login)     # Thêm giao diện đăng nhập

        # Đặt QStackedWidget làm widget trung tâm
        self.setCentralWidget(self.stacked_widget)
        self.setWindowTitle("Application")

    def register_user(self):
        #""" Hàm lưu thông tin người dùng vào file JSON khi đăng ký """
        username = self.ui_register.register_ip_username.text()
        repass = self.ui_register.register_ip_repass.text()
        password = self.ui_register.register_ip_pass.text()

        # Kiểm tra xem người dùng đã nhập đầy đủ thông tin chưa
        if not username or not repass or not password:
            self.show_message("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if repass != password:
            self.show_message("Bạn cần nhập lại đúng mật khẩu!")

        # Đọc dữ liệu từ file users.json (nếu có)
        users_data = self.load_users_data()

        # Kiểm tra xem người dùng đã tồn tại chưa
        if username in users_data:
            self.show_message("Lỗi", "Người dùng đã tồn tại!")
            return

        # Thêm người dùng vào dữ liệu
        users_data[username] = {"email": username, "password": password}

        # Lưu lại dữ liệu vào file JSON
        self.save_users_data(users_data)
        
        self.show_message("Thành công", "Đăng ký thành công!")
        # Chuyển đến giao diện đăng nhập
        self.stacked_widget.setCurrentIndex(1)

    def login_user(self):
        """ Hàm kiểm tra thông tin đăng nhập từ file JSON """
        username = self.ui_login.login_ip_username.text()
        password = self.ui_login.login_ip_pass.text()

        # Đọc dữ liệu từ file users.json
        users_data = self.load_users_data()

        # Kiểm tra thông tin đăng nhập
        if username not in users_data or users_data[username]['password'] != password:
            self.show_message("Lỗi", "Thông tin đăng nhập không chính xác!")
            return
        
        self.show_message("Thành công", "Đăng nhập thành công!")
        # Sau khi đăng nhập thành công, có thể chuyển đến trang chính của ứng dụng

    def load_users_data(self):
        """ Hàm đọc dữ liệu người dùng từ file users.json """
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Trả về dictionary rỗng nếu không tìm thấy file hoặc dữ liệu không hợp lệ

    def save_users_data(self, data):
        """ Hàm lưu dữ liệu người dùng vào file users.json """
        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)

    def show_message(self, title, message):
        """ Hiển thị thông báo cho người dùng """
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

if __name__ == '__main__':
    # Khởi tạo ứng dụng với alias app
    application = app(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(application.exec())
