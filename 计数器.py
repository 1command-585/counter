import tkinter as tk
from tkinter import messagebox
import os

class DraggableButton(tk.Button):
    """平滑拖拽的可移动按钮"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self._drag_start_x = 0
        self._drag_start_y = 0

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        new_x = self.winfo_x() + (event.x - self._drag_start_x)
        new_y = self.winfo_y() + (event.y - self._drag_start_y)
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        btn_width = self.winfo_width()
        btn_height = self.winfo_height()
        new_x = max(0, min(new_x, parent_width - btn_width))
        new_y = max(0, min(new_y, parent_height - btn_height))
        self.place(x=new_x, y=new_y)
        self.update_idletasks()


class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("计数器")
        # 初始窗口大小（宽 x 高），后续可能自动变大
        self.root.geometry("1000x700")
        # 允许用户手动调整大小（自动调整时也会生效）
        self.root.resizable(True, True)

        # 保存分数的文件名
        self.score_file = "score.txt"
        self.score = self.load_score()

        # ---------- 显示分数 ----------
        self.label = tk.Label(root, text=str(self.score), font=("Arial", 80))
        self.label.pack(pady=50, expand=True)

        # ---------- 可拖拽按钮 ----------
        self.inc_btn = DraggableButton(root, text="+", command=self.increment,
                                       width=6, font=("Arial", 40))
        self.inc_btn.place(x=200, y=500)

        self.reset_btn = DraggableButton(root, text="归零", command=self.confirm_reset,
                                         width=6, font=("Arial", 40))
        self.reset_btn.place(x=500, y=500)

        # 绑定窗口大小改变事件（可选，用于实时限制按钮边界）
        self.root.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        """当窗口大小改变时，确保按钮不超出边界"""
        if event.widget == self.root:
            # 检查两个按钮是否超出新窗口边界，若超出则移入
            for btn in (self.inc_btn, self.reset_btn):
                x = btn.winfo_x()
                y = btn.winfo_y()
                w = btn.winfo_width()
                h = btn.winfo_height()
                max_x = self.root.winfo_width() - w
                max_y = self.root.winfo_height() - h
                if x > max_x or y > max_y:
                    btn.place(x=min(x, max_x), y=min(y, max_y))

    def load_score(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        return int(content)
            except (ValueError, IOError):
                pass
        return 0

    def save_score(self):
        with open(self.score_file, "w") as f:
            f.write(str(self.score))

    def update_display(self):
        """更新分数显示，并检查是否需要自动放大窗口"""
        self.label.config(text=str(self.score))
        # 强制刷新以获取标签的真实渲染宽度
        self.root.update_idletasks()
        self.adjust_window_size()

    def adjust_window_size(self):
        """根据分数标签的宽度自动调整窗口大小（仅宽度）"""
        # 获取标签的实际渲染宽度（像素）
        label_width = self.label.winfo_width()
        if label_width <= 0:
            return
        # 左右各预留 100 像素的边距
        margin = 100
        required_width = label_width + margin

        current_width = self.root.winfo_width()
        if required_width > current_width:
            # 只增加宽度，保持高度不变
            new_width = required_width
            new_height = self.root.winfo_height()
            self.root.geometry(f"{new_width}x{new_height}")
            # 可选：如果需要同时调整高度，可以按比例或固定增加

    def increment(self):
        self.score += 1
        self.update_display()
        self.save_score()

    def confirm_reset(self):
        if messagebox.askyesno("确认归零", "确定要将计数器归零吗？"):
            self.score = 0
            self.update_display()
            self.save_score()


if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()