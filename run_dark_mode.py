import customtkinter as ctk
from main import ProxySwitchApp

# 强制设置深色主题
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# 创建并运行应用
root = ctk.CTk()
app = ProxySwitchApp(root)
root.mainloop()
