# 文件操作小工具项目｜个人学习笔记
> 项目路径：C:\python实践\ClaudeCodeTest
> 用途：Python os/shutil/zipfile 文件操作实战项目
> 笔记作者：自己
> 版本说明：原始代码手写练习 → Claude模块化重构优化

## 📌 一、项目整体架构
### 目录分层设计
> 分层思想：职责分离、代码解耦，同类代码集中存放，便于维护与扩展

### 1. main.py 【程序入口层】
- **职责**：主菜单循环、接收用户输入、调度 core 中的各个功能函数
- **设计原则**：只负责功能调度，不编写复杂业务实现代码

### 2. config.py 【全局配置层】
- **职责**：集中存放项目固定常量、全局参数
- **内容**：日志文件路径、压缩默认等级等配置；修改参数仅改动此文件，无需全局搜索替换

---

### 3. core/ 【业务功能层】
> 核心作用：存放全部业务功能实现代码，按照功能类别拆分文件

- **(1) `__init__.py`**
  Python包标识文件。
  作用：将普通文件夹标记为Python可识别的「包」，支持 `from core.xxx import xxx` 导入；空文件即可生效，是模块化项目标准配置。

- **(2) `file_operations.py`｜基础文件操作模块**
  存放文件/文件夹基础增删改查功能
  - `func1_show_files`：查看指定文件夹内所有文件
  - `func2_get_suffix`：按后缀名对文件夹内文件分类统计
  - `func3_make_folder`：创建新文件夹
  - `func5_copy_file`：复制单个文件至目标目录
  - `func6_delete_file`：删除指定文件
  - `func7_delete_folder`：删除整个文件夹
  - `func8_rename_file`：文件重命名
  - `func9_log_output`：写入操作日志到本地文件

- **(3) `advanced_operations.py`｜高级文件移动模块**
  - `func4_move_file`：整合三类移动场景
    - 单个文件移动
    - 完整文件夹移动
    - 按文件后缀批量移动（支持递归、保留目录结构）

- **(4) `search.py`｜文件检索模块**
  - `func10_file_search`：根据关键字搜索本地文件，支持递归遍历、大小写匹配切换、结果导出、路径复制

- **(5) `compression.py`｜压缩解压模块**
  - `func11_compress_file`：文件/文件夹打包为zip压缩包
  - `func12_extract_file`：解压zip压缩包，支持选择性解压、预览压缩包内容

---

### 4. utils/ 【通用工具层】
> 项目公共工具箱，存放多处复用的通用函数；业务代码直接调用，消除重复代码

- **(1) `clipboard.py`｜剪贴板工具**
  - `copy_to_clipboard`：将文本复制到Windows系统剪贴板

- **(2) `helpers.py`｜综合通用工具集**
  - `safe_input`：封装原生`input()`，提供统一退出机制（输入 q/Q/0 返回主菜单）
  - `handle_duplicate_file`：自动处理重名文件，避免直接覆盖
  - `format_file_size`：字节数值转为 KB/MB/GB 人类可读格式
  - `get_folder_size`：递归计算文件夹总占用大小
  - `merge_folders`：递归合并两个文件夹内容
  - `export_search_result_to_log`：搜索结果格式化并写入日志

- **(3) `logger.py`｜统一日志模块**
  - `write_log`：自动追加时间戳，标准化写入日志文件

- **(4) `path_utils.py`｜路径清洗工具**
  - `normalize_path`：清理路径多余空格、引号，统一路径格式
  - `input_path`：整合路径输入、标准化清洗、退出能力一体封装



## 📌 二、项目使用的Python标准库
> 全部为Python内置标准库，无需额外安装第三方包，结合本项目实战场景整理

### 1. os
**作用**：操作系统底层交互，负责路径处理、目录遍历、基础文件管理
常用API：
- `os.path.join()`：跨平台安全拼接路径
- `os.path.isfile() / isdir() / exists()`：区分文件/文件夹、校验路径是否存在
- `os.listdir()`：单层读取文件夹内容
- `os.walk()`：递归多层遍历文件夹
- `os.path.splitext()`：分割文件名与后缀名
- `os.path.normpath()`：标准化路径格式，清理多余斜杠、小数点
- `os.mkdir() / os.remove() / os.rename()`：创建文件夹、删除文件、文件重命名

### 2. shutil
**作用**：高层文件操作工具，弥补os短板，实现文件夹级别的批量操作
常用API：
- `shutil.move()`：文件/文件夹移动
- `shutil.copy()`：复制文件
- `shutil.rmtree()`：递归删除**非空文件夹**

### 3. zipfile
**作用**：专门处理ZIP格式压缩包的创建、读取、解压
核心类与方法：
- `ZipFile`：压缩包读写对象（配合`with`上下文管理器）
- `ZIP_DEFLATED`：启用压缩算法，支持自定义压缩等级
- `.write()`：将文件写入压缩包
- `.extract() / .extractall()`：解压单个文件 / 全部文件

### 4. datetime
**作用**：日期时间处理，生成格式化时间戳
常用API：
- `datetime.datetime.now().strftime()`：自定义格式化时间，用于日志记录

### 5. subprocess
**作用**：Python调用系统终端命令，和操作系统指令交互
项目场景：`clipboard.py` 实现Windows文本复制到剪贴板
常用API：
- `subprocess.run()`：执行系统`clip`命令，配置GBK编码解决中文乱码



## 📌 三、踩坑记录 & 个人理解
> 这里自由填写看不懂、反复卡住的知识点