"""
简易计算器 (PySide6)
可被 briefcase 打包为 Android APK
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QSizePolicy   # 新增 QSizePolicy
)
from PySide6.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算器")
        self.setMinimumSize(320, 480)

        # 当前显示与表达式状态
        self.current_input = ""
        self.expression = ""  # 用于求值的完整表达式字符串
        self.last_was_operator = False
        self.last_was_equals = False

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # 显示屏
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet(
            "font-size: 28px; padding: 12px; background: #f0f0f0; border: 1px solid #ccc;"
        )
        self.display.setText("0")
        main_layout.addWidget(self.display)

        # 按钮网格
        grid = QGridLayout()
        grid.setSpacing(8)

        buttons = {
            (0, 0): "C",   (0, 1): "⌫",
            (1, 0): "7",   (1, 1): "8",   (1, 2): "9",   (1, 3): "/",
            (2, 0): "4",   (2, 1): "5",   (2, 2): "6",   (2, 3): "*",
            (3, 0): "1",   (3, 1): "2",   (3, 2): "3",   (3, 3): "-",
            (4, 0): "0",   (4, 1): ".",   (4, 2): "=",   (4, 3): "+",
        }

        for (row, col), label in buttons.items():
            btn = QPushButton(label)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,  # 水平策略
                QSizePolicy.Policy.Expanding  # 垂直策略
            )
            btn.setStyleSheet(
                "font-size: 20px; padding: 16px;"
            )
            btn.clicked.connect(self.on_button_clicked)
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)

    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text == "C":
            self.clear_all()
        elif text == "⌫":
            self.backspace()
        elif text in "+-*/":
            self.add_operator(text)
        elif text == "=":
            self.calculate()
        elif text == ".":
            self.add_decimal()
        else:  # 数字 0-9
            self.add_digit(text)

    def clear_all(self):
        self.current_input = ""
        self.expression = ""
        self.last_was_operator = False
        self.last_was_equals = False
        self.display.setText("0")

    def backspace(self):
        if self.last_was_equals:
            return
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.expression = self.expression[:-1]
        if not self.current_input:
            self.display.setText("0")
            self.last_was_operator = False
        else:
            self.display.setText(self.expression)
            # 检查最后一个字符是否为运算符
            self.last_was_operator = self.expression[-1] in "+-*/"

    def add_digit(self, digit):
        # 如果刚刚按了等号，重置
        if self.last_was_equals:
            self.clear_all()
        self.current_input += digit
        self.expression += digit
        self.display.setText(self.expression)
        self.last_was_operator = False
        self.last_was_equals = False

    def add_decimal(self):
        if self.last_was_equals:
            self.clear_all()
            self.current_input = "0."
            self.expression = "0."
            self.display.setText(self.expression)
            self.last_was_operator = False
            self.last_was_equals = False
            return

        # 当前输入部分已经包含小数点，不允许再添加
        if "." in self.current_input:
            return

        # 如果当前输入为空，则补0
        if not self.current_input:
            self.current_input = "0."
            self.expression += "0."
        else:
            self.current_input += "."
            self.expression += "."
        self.display.setText(self.expression)
        self.last_was_operator = False
        self.last_was_equals = False

    def add_operator(self, op):
        if self.last_was_equals:
            # 等号后继续运算：使用上一次结果作为起点
            # 保留上次计算结果，expression 设为该结果
            result = self.display.text()
            if result == "Error":
                self.clear_all()
                return
            self.expression = result + op
            self.current_input = ""
            self.display.setText(self.expression)
            self.last_was_operator = True
            self.last_was_equals = False
            return

        if not self.expression and op != "-":
            # 空表达式时只允许负号作为一元运算符
            return

        # 避免连续输入运算符：替换最后一个运算符
        if self.last_was_operator and self.expression:
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op

        self.current_input = ""
        self.display.setText(self.expression)
        self.last_was_operator = True
        self.last_was_equals = False

    def calculate(self):
        if not self.expression:
            return
        try:
            # 用 eval 计算，但只允许数字和运算符，提高安全性
            # 替换显示乘除号为 Python 运算符（都是 * 和 /，无需替换）
            # 检查表达式是否包含非法字符（仅限数字、小数点、运算符）
            allowed = set("0123456789.+-*/")
            if any(ch not in allowed for ch in self.expression):
                raise ValueError("非法字符")
            result = eval(self.expression)
            # 格式化结果，避免浮点数精度问题
            if isinstance(result, float):
                # 去掉多余的小数末尾0
                formatted = f"{result:.10f}".rstrip("0").rstrip(".")
                if formatted == "":
                    formatted = "0"
            else:
                formatted = str(result)
            self.display.setText(formatted)
            self.expression = formatted
            self.current_input = formatted
            self.last_was_equals = True
            self.last_was_operator = False
        except:
            self.display.setText("Error")
            self.expression = ""
            self.current_input = ""
            self.last_was_equals = False
            self.last_was_operator = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())