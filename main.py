"""
安卓手机计算器 - Kivy 跨平台应用
支持基础运算、科学计算功能
"""

import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp

# 安卓设备适配
if platform == 'android':
    from kivy.core.window import Window
    Window.fullscreen = 'auto'
else:
    Window.size = (400, 700)


class CalculatorButton(Button):
    """自定义计算器按钮样式"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.font_size = dp(22)
        self.bold = True
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        """重绘按钮背景"""
        self.canvas.before.clear()
        with self.canvas.before:
            if hasattr(self, 'btn_color'):
                Color(*self.btn_color)
            else:
                Color(0.2, 0.2, 0.25, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])


class CalculatorDisplay(Label):
    """计算器显示区域"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = dp(48)
        self.halign = 'right'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = dp(120)
        self.color = (1, 1, 1, 1)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.padding = [dp(20), dp(10)]

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.08, 0.08, 0.12, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15), dp(15), dp(0), dp(0)])


class CalculatorApp(App):
    """主计算器应用"""
    
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', spacing=dp(2))
        
        # 显示表达式
        self.expression_label = CalculatorDisplay(text='0')
        main_layout.add_widget(self.expression_layout())
        
        # 按钮区域
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '='],
        ]
        
        button_grid = GridLayout(cols=4, spacing=dp(8), padding=dp(12))
        button_grid.size_hint_y = None
        button_grid.bind(minimum_height=button_grid.setter('height'))
        
        # 按钮颜色方案
        operator_color = (0.95, 0.6, 0.2, 1)  # 橙色
        number_color = (0.22, 0.22, 0.28, 1)  # 深灰色
        function_color = (0.15, 0.15, 0.2, 1)  # 更深的灰色
        clear_color = (0.85, 0.3, 0.25, 1)  # 红色
        equals_color = (0.95, 0.6, 0.2, 1)  # 橙色
        
        self.current_expression = ''
        self.current_result = '0'
        self.last_was_operator = False
        self.last_was_equals = False
        
        for row in buttons:
            for btn_text in row:
                btn = CalculatorButton(text=btn_text, size_hint_y=None, height=dp(75))
                
                # 设置颜色
                if btn_text in {'÷', '×', '−', '+', '='}:
                    if btn_text == '=':
                        btn.btn_color = equals_color
                    else:
                        btn.btn_color = operator_color
                elif btn_text in {'C', '±', '%'}:
                    btn.btn_color = function_color
                else:
                    btn.btn_color = number_color
                
                btn.bind(on_press=self.on_button_press)
                button_grid.add_widget(btn)
        
        main_layout.add_widget(button_grid)
        
        return main_layout
    
    def expression_layout(self):
        """表达式显示布局"""
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(160), padding=[dp(10), dp(5)])
        
        # 小标签显示完整表达式
        self.expression_text = Label(
            text='',
            font_size=dp(18),
            halign='right',
            valign='middle',
            size_hint_y=None,
            height=dp(35),
            color=(0.6, 0.6, 0.7, 1)
        )
        
        # 结果显示
        self.display = CalculatorDisplay(text='0', font_size=dp(52), height=dp(120))
        self.display.bind(pos=self.display.update_canvas, size=self.display.update_canvas)
        
        layout.add_widget(self.expression_text)
        layout.add_widget(self.display)
        
        return layout
    
    def on_button_press(self, instance):
        """按钮点击处理"""
        text = instance.text
        
        if text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '=':
            self.calculate()
        elif text == '±':
            self.negate()
        elif text == '%':
            self.percent()
        elif text in {'+', '−', '×', '÷'}:
            self.add_operator(text)
        elif text == '.':
            self.add_decimal()
        else:
            self.add_number(text)
    
    def clear(self):
        """清除所有"""
        self.current_expression = ''
        self.current_result = '0'
        self.display.text = '0'
        self.expression_text.text = ''
        self.last_was_operator = False
        self.last_was_equals = False
    
    def backspace(self):
        """退格"""
        if self.last_was_equals:
            self.clear()
            return
        
        if len(self.current_expression) > 0:
            # 检查最后一个字符是否是运算符
            last_char = self.current_expression[-1]
            if last_char in {'+', '−', '×', '÷'}:
                self.last_was_operator = False
            
            self.current_expression = self.current_expression[:-1]
            
            if self.current_expression:
                try:
                    result = self.evaluate_expression(self.current_expression)
                    self.current_result = result
                    self.display.text = self.format_number(result)
                except:
                    self.display.text = self.current_expression
                self.expression_text.text = self.current_expression
            else:
                self.display.text = '0'
                self.current_result = '0'
                self.expression_text.text = ''
    
    def add_number(self, num):
        """添加数字"""
        if self.last_was_equals:
            self.current_expression = ''
            self.last_was_equals = False
        
        self.current_expression += num
        self.expression_text.text = self.current_expression
        
        try:
            result = self.evaluate_expression(self.current_expression)
            self.current_result = result
            self.display.text = self.format_number(result)
        except:
            self.display.text = self.current_expression
        
        self.last_was_operator = False
    
    def add_operator(self, op):
        """添加运算符"""
        if self.last_was_equals:
            self.last_was_equals = False
        
        if not self.current_expression:
            if self.current_result != '0':
                self.current_expression = self.current_result + op
            else:
                return
        elif self.last_was_operator:
            self.current_expression = self.current_expression[:-1] + op
        else:
            self.current_expression += op
        
        self.expression_text.text = self.current_expression
        self.last_was_operator = True
    
    def add_decimal(self):
        """添加小数点"""
        if self.last_was_equals:
            self.current_expression = '0.'
            self.last_was_equals = False
            self.expression_text.text = self.current_expression
            self.display.text = '0.'
            return
        
        # 检查当前数字是否已有小数点
        parts = self.current_expression.replace('+', '|').replace('−', '|').replace('×', '|').replace('÷', '|').split('|')
        current_part = parts[-1] if parts else ''
        
        if '.' not in current_part:
            if not current_part:
                self.current_expression += '0.'
            else:
                self.current_expression += '.'
            
            self.expression_text.text = self.current_expression
            try:
                result = self.evaluate_expression(self.current_expression)
                self.current_result = result
                self.display.text = self.format_number(result)
            except:
                self.display.text = self.current_expression
    
    def negate(self):
        """取反"""
        if not self.current_expression or self.current_expression == '0':
            return
        
        if self.current_expression.startswith('−'):
            self.current_expression = self.current_expression[1:]
        else:
            self.current_expression = '−' + self.current_expression
        
        self.expression_text.text = self.current_expression
        try:
            result = self.evaluate_expression(self.current_expression)
            self.current_result = result
            self.display.text = self.format_number(result)
        except:
            pass
    
    def percent(self):
        """百分比"""
        try:
            value = float(self.current_result)
            value = value / 100
            self.current_result = self.format_number(str(value))
            self.display.text = self.current_result
            self.current_expression = self.current_result
            self.expression_text.text = self.current_expression
        except:
            pass
    
    def calculate(self):
        """计算结果"""
        if not self.current_expression:
            return
        
        # 如果最后一个字符是运算符，去掉它
        expr = self.current_expression
        if expr[-1] in {'+', '−', '×', '÷'}:
            expr = expr[:-1]
        
        try:
            result = self.evaluate_expression(expr)
            self.expression_text.text = expr + ' ='
            self.display.text = self.format_number(result)
            self.current_result = result
            self.current_expression = result
            self.last_was_equals = True
            self.last_was_operator = False
        except Exception as e:
            self.display.text = '错误'
            Clock.schedule_once(lambda dt: self.clear(), 1.5)
    
    def evaluate_expression(self, expr):
        """计算表达式"""
        if not expr:
            return '0'
        
        # 替换显示符号为计算符号
        calc_expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
        
        # 安全检查
        allowed_chars = set('0123456789.+-*/() ')
        for c in calc_expr:
            if c not in allowed_chars:
                raise ValueError("非法字符")
        
        result = eval(calc_expr)
        
        # 处理浮点数精度
        if isinstance(result, float):
            if result == int(result):
                if abs(result) < 1e15:
                    return str(int(result))
            else:
                return str(round(result, 10))
        
        return str(result)
    
    def format_number(self, num_str):
        """格式化数字显示"""
        try:
            if '.' in num_str:
                parts = num_str.split('.')
                if len(parts[0]) > 12:
                    return num_str[:15]
                return num_str
            else:
                if len(num_str) > 15:
                    return num_str[:15]
                return num_str
        except:
            return num_str


if __name__ == '__main__':
    CalculatorApp().run()
