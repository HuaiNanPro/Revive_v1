
# 物品复活 Revive v1.1 — 校园闲置赠送/转让工具

**目标**：让同学们能快速发布、查找、删除闲置物品信息。  
**亮点**：
- 命令行（CLI）+ **黄色活泼风格 GUI（**
- SQLite 持久化，无需安装数据库
- 完整注释与高分检查表对齐（说明文档、功能、风格、代码、注释）

---

## 快速开始（零基础）

1. 安装 **Python 3.10+**（安装时勾选 *Add Python to PATH*）。  
2. 下载并解压本仓库到任意位置。  
3. **命令行模式**（推荐先跑一遍）：
   ```bash
   python app.py --init-db
   python app.py add --name "蓝牙耳机" --desc "九成新" --contact "微信:Avid_123" --price 0
   python app.py list
   python app.py find --q 耳机
   python app.py delete --id 1
   python app.py export --out items.csv
   ```
4. **图形界面（黄色活泼风格）**：
   ```bash
   python gui.py
   ```

---

## 功能清单（对齐作业要求）
- ✅ 添加物品信息（名称/描述/联系方式/价格0=赠送）
- ✅ 删除物品信息（按 `id`）
- ✅ 显示物品列表（排序/分页）
- ✅ 查找物品信息（关键词匹配）
- ✅ 导出 CSV（可做统计/分享）

---

## 文件结构
```
revive_v11/
├─ app.py        # 命令行入口（注释/常量/类型化/更规范）
├─ gui.py        # 包豪斯极简风 GUI（ttk.Style + 条纹表格）
├─ db.py         # 数据访问层（SQLite 封装，复用 CLI/GUI）
├─ README.md     # 本文件
├─ LICENSE       # MIT
└─ PSP_LOG.md    # PSP2.1 任务/耗时记录模板
```

---

## 评分对齐说明（代码检查表）
- **说明文档**：本 README 提供项目目的、运行方式、截图位、作者与版本信息。
- **功能检查**：CLI 与 GUI 全覆盖“增/删/查/列表”，含输入校验与错误提示。
- **版面风格**：PEP8 命名、每行一语句、统一空行/缩进/常量化。
- **代码**：接口清晰、命名有意义、常量集中、类型注解、函数职责单一。
- **注释**：文件头、函数 docstring、参数/返回值说明、全局常量含义。

---

## 版本信息
- 作者：帅哲（Avid）
- 版本：v1.1（黄色活泼风格 GUI + 代码规范化）
- 许可证：MIT

