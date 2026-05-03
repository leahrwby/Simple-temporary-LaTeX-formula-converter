# -*- coding: utf-8 -*-
import os
import platform
import re
import subprocess
import tkinter as tk
from tkinter import messagebox

import pypandoc


class LatexToWordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX 转 Word 公式神器 V4.0")
        self.root.geometry("580x560")
        self.root.eval("tk::PlaceWindow . center")

        self.last_generated_mathml = ""

        top_frame = tk.Frame(root)
        top_frame.pack(fill="x", pady=(10, 5), padx=20)
        tk.Label(top_frame, text="在此粘贴您的科研内容:", font=("微软雅黑", 12, "bold")).pack(side="left")

        self.topmost_var = tk.BooleanVar(value=False)
        self.topmost_cb = tk.Checkbutton(
            top_frame,
            text="📌 窗口置顶",
            variable=self.topmost_var,
            command=self.toggle_topmost,
            font=("微软雅黑", 10),
        )
        self.topmost_cb.pack(side="right")

        self.text_input = tk.Text(root, height=9, width=55, font=("Consolas", 12), bg="#f4f4f4")
        self.text_input.pack(pady=5)
        default_text = "\\rho = \\frac{m}{V}"
        self.text_input.insert("1.0", default_text)

        tk.Label(root, text="🚀 主功能：纯公式代码转换", font=("微软雅黑", 12, "bold"), fg="#e65100").pack(
            pady=(15, 0)
        )
        tk.Label(root, text="无需 $ 包裹，直接转为剪贴板对象", font=("微软雅黑", 9), fg="#666666").pack()

        self.copy_btn = tk.Button(
            root,
            text="仅转换纯公式 -> 复制到剪贴板",
            font=("微软雅黑", 13, "bold"),
            bg="#FFB300",
            fg="black",
            command=self.process_pure_formula,
            width=35,
            height=2,
        )
        self.copy_btn.pack(pady=5)

        tk.Frame(root, height=2, bd=1, relief="sunken", width=520).pack(pady=10)

        tk.Label(
            root,
            text="📝 次功能：包含汉字与公式的整段文本",
            font=("微软雅黑", 10, "bold"),
            fg="#1565C0",
        ).pack(pady=(5, 0))
        tk.Label(root, text="注意：此模式下公式需用 $ 或 $$ 包裹", font=("微软雅黑", 9), fg="#666666").pack()

        self.mixed_btn = tk.Button(
            root,
            text="智能排版并自动打开 Word",
            font=("微软雅黑", 10),
            bg="#2196F3",
            fg="white",
            command=self.process_mixed_text,
            width=30,
            height=1,
        )
        self.mixed_btn.pack(pady=5)

        self.status_label = tk.Label(root, text="", font=("微软雅黑", 10, "bold"))
        self.status_label.pack(pady=5)

        self.root.bind("<FocusIn>", self.on_window_focus)
        self.check_pandoc_engine()

    def toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    def on_window_focus(self, event):
        try:
            clipboard_content = self.root.clipboard_get().strip()
            current_text = self.text_input.get("1.0", tk.END).strip()
            if not current_text and clipboard_content and "<math" not in clipboard_content:
                self.text_input.insert("1.0", clipboard_content)
                self.show_status("💡 已自动识别剪贴板，请选择转换模式", "#00838F")
        except tk.TclError:
            pass

    def show_status(self, message, color):
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def check_pandoc_engine(self):
        try:
            pypandoc.get_pandoc_version()
        except OSError:
            messagebox.showinfo("初始化", "未检测到 Pandoc，后台下载中...")
            self.root.update()
            try:
                pypandoc.download_pandoc()
                messagebox.showinfo("成功", "Pandoc 下载完成！")
            except Exception as e:
                messagebox.showerror("失败", f"下载失败: {e}")

    def open_file_cross_platform(self, filepath):
        """跨平台自动打开文件。"""
        if platform.system() == "Darwin":
            subprocess.call(("open", filepath))
        elif platform.system() == "Windows":
            os.startfile(filepath)
        else:
            subprocess.call(("xdg-open", filepath))

    def process_mixed_text(self):
        """处理整段混合文本并自动拉起 Word。"""
        content = self.text_input.get("1.0", tk.END).strip()
        if not content:
            self.show_status("⚠️ 内容不能为空！", "#D32F2F")
            return

        temp_file = "Temp_Rendered_Paragraph.docx"
        try:
            self.mixed_btn.config(state="disabled", text="正在排版生成...")
            self.show_status("正在进行引擎排版...", "#1565C0")

            pypandoc.convert_text(content, to="docx", format="markdown", outputfile=temp_file)

            self.text_input.delete("1.0", tk.END)
            self.show_status("✅ 排版成功！已为您打开文档，请直接全选复制", "#388E3C")

            self.open_file_cross_platform(os.path.abspath(temp_file))

        except Exception as e:
            messagebox.showerror("排版失败", f"请检查格式:\n{e}")
            self.show_status("❌ 排版失败", "#D32F2F")
        finally:
            self.mixed_btn.config(state="normal", text="智能排版并自动打开 Word")

    def process_pure_formula(self):
        """纯公式剪贴板功能。"""
        latex_formula = self.text_input.get("1.0", tk.END).strip()
        if not latex_formula:
            self.show_status("⚠️ 公式不能为空！", "#D32F2F")
            return

        try:
            self.copy_btn.config(state="disabled", text="转换中...")
            safe_latex = f"$${latex_formula.strip(' $')}$$"
            html_out = pypandoc.convert_text(safe_latex, to="html", format="markdown", extra_args=["--mathml"])

            match = re.search(r"(<math.*?</math>)", html_out, re.DOTALL | re.IGNORECASE)
            mathml_content = match.group(1) if match else html_out

            self.root.clipboard_clear()
            self.root.clipboard_append(mathml_content)
            self.last_generated_mathml = mathml_content
            self.root.update()

            self.text_input.delete("1.0", tk.END)
            self.show_status("✅ 已复制到剪切板", "#388E3C")

        except Exception as e:
            messagebox.showerror("转换失败", f"语法错误:\n{e}")
            self.show_status("❌ 转换失败", "#D32F2F")
        finally:
            self.copy_btn.config(state="normal", text="仅转换纯公式 -> 复制到剪贴板")


if __name__ == "__main__":
    root = tk.Tk()
    app = LatexToWordApp(root)
    root.mainloop()
