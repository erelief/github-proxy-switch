# 主题测试脚本说明

## 用途

用于在不修改main.py的情况下，强制使用指定主题进行测试。

---

## 可用脚本

| 脚本 | 主题 | 命令 |
|------|------|------|
| `run_light_mode.py` | 浅色 | `python run_light_mode.py` |
| `run_dark_mode.py` | 深色 | `python run_dark_mode.py` |
| `main.py` | 系统默认 | `python main.py` |

---

## 使用方法

### 测试浅色主题

```bash
python run_light_mode.py
```

### 测试深色主题

```bash
python run_dark_mode.py
```

### 测试系统默认主题（跟随系统）

```bash
python main.py
```

---

## 工作原理

这些脚本在导入`ProxySwitchApp`之前调用`ctk.set_appearance_mode()`，因此会覆盖main.py中的`"System"`设置。

**不修改main.py，实现临时主题控制。**

---

## 清理说明

测试完成后，可以直接删除这两个脚本：

```bash
rm run_light_mode.py run_dark_mode.py
```

---

## 注意事项

- 这些脚本仅用于测试，不会修改main.py
- 打包后的exe不会使用这些脚本的主题设置
- 如需打包固定主题，需要修改main.py或添加命令行参数
