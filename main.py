import customtkinter as ctk
import subprocess
import re
import json
import os
import sys
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

HISTORY_FILE = "history.json"
MAX_HISTORY = 10

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def get_git_proxy():
    try:
        result = subprocess.run(
            ["git", "config", "--global", "--get", "http.https://github.com.proxy"],
            capture_output=True, text=True, encoding="utf-8",
            startupinfo=startupinfo
        )
        output = result.stdout.strip()
        return output if output else ""
    except (OSError, subprocess.SubprocessError, Exception):
        return ""


def get_system_proxy():
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_READ
        )
        enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
        if not enabled:
            return ""

        server, _ = winreg.QueryValueEx(key, "ProxyServer")
        if not server:
            return ""

        if "=" in server:
            parts = dict(p.split("=", 1) for p in server.split(";"))
            socks5_addr = parts.get("socks5", "")
            http_addr = parts.get("http", "")
            if socks5_addr:
                return f"socks5://{socks5_addr}"
            if http_addr:
                return f"http://{http_addr}"
        else:
            return f"http://{server}"

        return ""
    except Exception:
        return ""


def set_git_proxy(proxy_url):
    try:
        subprocess.run(
            ["git", "config", "--global", "http.https://github.com.proxy", proxy_url],
            check=True,
            startupinfo=startupinfo
        )
        return True, proxy_url
    except subprocess.CalledProcessError as e:
        return False, str(e)


def unset_git_proxy():
    try:
        subprocess.run(
            ["git", "config", "--global", "--unset", "http.https://github.com.proxy"],
            check=True,
            startupinfo=startupinfo
        )
        return True
    except subprocess.CalledProcessError:
        return False


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and isinstance(data[0], dict):
                    return [
                        f"{item.get('protocol', 'http')}://{item.get('addr', '')}"
                        for item in data
                    ]
                return data
        except Exception:
            return []
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_history(proxy_url):
    history = load_history()
    if proxy_url in history:
        history.remove(proxy_url)
    history.insert(0, proxy_url)
    history = history[:MAX_HISTORY]
    save_history(history)
    return history


def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


def load_button_image(name, size=(16, 16)):
    path = get_resource_path(f"images/{name}.png")
    image = ctk.CTkImage(Image.open(path), size=size)
    return image


class ProxySwitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub 代理开关工具")
        self.root.iconbitmap(get_resource_path("icon.ico"))
        self.root.geometry("360x145")
        self.root.resizable(False, False)

        self.run_img = load_button_image("run")
        self.stop_img = load_button_image("stop")
        self.test_img = load_button_image("test")

        self.history = load_history()
        self._action_type = "enable"

        self._setup_ui()
        self._refresh_status()

    def _setup_ui(self):
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=12)

        self.status_label = ctk.CTkLabel(frame, text="当前状态: 未启用")
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(0, 12))

        ctk.CTkLabel(frame, text="代理：").grid(row=1, column=0, sticky="e", pady=5)

        proxy_frame = ctk.CTkFrame(frame, fg_color="transparent")
        proxy_frame.grid(row=1, column=1, sticky="w", pady=5, padx=(5, 0))

        self.addr_var = ctk.StringVar()
        self.history_combo = ctk.CTkComboBox(proxy_frame, variable=self.addr_var, width=260)
        self.history_combo.pack(side="left")
        self.history_combo.bind("<<ComboboxSelected>>", self._on_history_selected)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent", width=260)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=15)

        self.action_btn = ctk.CTkButton(btn_frame, width=90, image=self.run_img, compound="left", command=self._toggle)
        self.action_btn.pack(side="right")

        self.change_btn = ctk.CTkButton(btn_frame, text="更改代理", width=90, image=self.run_img, compound="left", command=self._enable)
        self.change_btn.pack(side="right", padx=(0, 5))

        self.test_btn = ctk.CTkButton(btn_frame, text="测试", width=60, image=self.test_img, compound="left", command=self._test_proxy)
        self.test_btn.pack(side="right")

        self._update_combo_list()
        self._update_action_button()
        self._load_system_proxy()

    def _on_history_selected(self, event):
        selected = self.history_combo.get()
        if selected == "🗑️清空历史":
            self._clear_history()
            self.addr_var.set("")
            return
        if selected:
            self.addr_var.set(selected)

    def _load_system_proxy(self):
        proxy_url = get_git_proxy()
        if not proxy_url:
            sys_proxy = get_system_proxy()
            if sys_proxy:
                self.addr_var.set(sys_proxy)

    def _update_combo_list(self):
        display_list = self.history.copy()
        if self.history:
            display_list.append("🗑️清空历史")
        self.history_combo.configure(values=display_list)

    def _update_action_button(self, proxy_url=None):
        if proxy_url is None:
            proxy_url = get_git_proxy()
        if proxy_url:
            self.action_btn.configure(text="禁用代理", image=self.stop_img, compound="left")
            self._action_type = "disable"
            self.change_btn.pack(side="right", padx=(0, 5))
            self.test_btn.pack(side="right", padx=(0, 5))
        else:
            self.action_btn.configure(text="启用代理", image=self.run_img, compound="left")
            self._action_type = "enable"
            self.change_btn.pack_forget()
            self.test_btn.pack_forget()

    def _toggle(self):
        if self._action_type == "enable":
            self._enable()
        else:
            self._disable()

    def _refresh_status(self):
        proxy_url = get_git_proxy()
        if proxy_url:
            self.addr_var.set(proxy_url)
            self.status_label.configure(text=f"当前状态: 已启用  {proxy_url}")
        else:
            sys_proxy = get_system_proxy()
            if sys_proxy:
                self.status_label.configure(text=f"当前状态: 未启用，系统代理为：{sys_proxy}")
            else:
                self.status_label.configure(text="当前状态: 未启用，未检测到系统代理")
        self._update_action_button(proxy_url)

    def _enable(self):
        proxy_url = self.addr_var.get().strip()

        proxy_url = proxy_url.replace("：", ":")

        if not proxy_url or "://" not in proxy_url:
            CTkMessagebox(title="输入错误", message="请填写完整的代理地址（格式：协议://地址:端口）", icon="warning")
            return

        success, result = set_git_proxy(proxy_url)
        if success:
            self.history = add_history(proxy_url)
            self._update_combo_list()
            self.status_label.configure(text=f"当前状态: 已启用  {proxy_url}")
            self._update_action_button(proxy_url)
            CTkMessagebox(title="成功", message=f"代理已启用\n{result}", icon="check")
        else:
            CTkMessagebox(title="错误", message=f"设置代理失败\n{result}", icon="cancel")

    def _disable(self):
        success = unset_git_proxy()
        if success:
            CTkMessagebox(title="成功", message="代理已禁用", icon="check")
            self._refresh_status()
            self._load_system_proxy()
        else:
            CTkMessagebox(title="错误", message="禁用代理失败", icon="cancel")

    def _test_proxy(self):
        proxy_url = get_git_proxy()
        if not proxy_url:
            CTkMessagebox(title="提示", message="当前未设置代理", icon="info")
            return

        original_status = self.status_label.cget("text")
        self.status_label.configure(text="正在测试代理连接...")
        self.root.update()

        def close_test_window():
            pass

        def test_thread():
            try:
                result = subprocess.run(
                    ["git", "ls-remote", "https://github.com/github/gitignore", "HEAD"],
                    capture_output=True,
                    env={**os.environ, "HTTP_PROXY": proxy_url, "HTTPS_PROXY": proxy_url},
                    timeout=3,
                    text=True,
                    startupinfo=startupinfo
                )

                self.status_label.configure(text=original_status)

                if result.returncode == 0:
                    CTkMessagebox(title="测试成功", message=f"代理可以正常连接 GitHub！\n{proxy_url}", icon="check")
                else:
                    CTkMessagebox(title="测试失败", message=f"代理无法连接 GitHub\n{result.stderr}", icon="cancel")
            except subprocess.TimeoutExpired:
                self.status_label.configure(text=original_status)
                CTkMessagebox(title="测试失败", message="连接超时（3秒），请检查代理配置", icon="cancel")
            except Exception as e:
                self.status_label.configure(text=original_status)
                CTkMessagebox(title="测试失败", message=f"测试出错: {str(e)}", icon="cancel")

        self.root.after(100, test_thread)

    def _clear_history(self):
        if CTkMessagebox(title="确认", message="确定要清除所有历史记录吗？", icon="question", option_1="Yes", option_2="No").get() == "Yes":
            clear_history()
            self.history = []
            self._update_combo_list()
            CTkMessagebox(title="成功", message="历史记录已清除", icon="check")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = ProxySwitchApp(root)
    root.mainloop()
