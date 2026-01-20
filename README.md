# GitHub Proxy Switch

![img](images/Gemini_Generated_Image_ec5mltec5mltec5m.png)

一个简单的 Windows GUI 工具，用于快速开关 GitHub CLI 的代理设置。

![img](images/screenshot-light.png)

## 注意事项
- 本软件**不提供**代理服务本身，仅提供“开关”作用
- 本软件通过 [OpenCode](https://opencode.ai/) 使用 [GLM-4.7](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.7) Vibe Coding 而成，作者本人不会编程

## 功能

- 快速启用/禁用 Git 代理（仅针对 GitHub.com）
- 显示当前代理状态
- 代理历史记录管理

## 特点

- **自动发现系统代理**：检测现在系统的代理（HTTP），自动填入
- **仅针对 GitHub**：只对 `github.com` 域名设置代理，不影响其他 Git 操作
- **简洁高效**：无需手动编辑配置文件
- **自适应主题**：根据系统主题自动切换

## 使用方法


### 操作说明

1. 在输入框中填写完整的代理地址
   - HTTP代理：`http://127.0.0.1:7890`
   - SOCKS5代理：`socks5://127.0.0.1:7890`
2. 点击`启用代理`开启 GitHub 代理
3. 点击`禁用代理`关闭代理
4. 状态栏会显示当前代理状态
5. 可点击`测试`检测代理是否成功

### 配置说明

启用代理后，Git 配置文件会添加：

```ini
[http "https://github.com"]
    proxy = socks5://127.0.0.1:7890
```

这种配置方式只会对 GitHub 相关的 HTTP 请求应用代理，不影响其他域名的 Git 操作。


## 依赖

- customtkinter（基于 Tkinter 的现代化 UI 库）
- tkinter（Python 标准库，customtkinter 依赖）
- CTkMessagebox（现代化的消息框组件）
- Pillow（图像处理库）

## 待办事项
- 增加 SSH 代理的支持