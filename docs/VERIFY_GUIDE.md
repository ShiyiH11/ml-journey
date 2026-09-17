# 亲手验证手册

> 目标：在自己电脑上，从零走完一遍「确认仓库正常 → 提交新文件 → 推送上线」的完整流程。
>
> 这份文档本身就是一个练习材料 —— 它是**未提交状态**的，等你按本手册把它提交上去。

---

## 第 0 步：打开终端

三种方法，任选一种：

| 方法 | 操作 |
|---|---|
| **最简单** | 按 `Win + X`，在弹出菜单里点「**终端**」或「**Windows PowerShell**」 |
| 从文件夹进 | 打开文件资源管理器，进到 `ml-journey` 文件夹，在**地址栏**里输入 `powershell` 回车 |
| 搜索 | 按 `Win`，直接打字 `powershell`，回车 |

打开后你会看到一个**蓝色或黑色的窗口**，里面有一行文字，最后是个 `>` 符号，光标在闪。这就对了。

> **粘贴技巧**：在这个窗口里 `Ctrl + V` 可能不管用，**右键点一下就自动粘贴**了。
> 复制命令 → 右键 → 回车。

---

## 第 1 步：进入项目目录

复制这一行，右键粘贴，回车：

```powershell
cd C:\Users\ASUS\WorkBuddy\2026-09-17-08-30-13\ml-journey
```

**预期**：命令行开头的路径变了，变成 `...\ml-journey>`。

**如果报错说路径不存在**：用文件资源管理器打开 `ml-journey` 文件夹，在地址栏复制真实路径，替换上去。

---

## 第 2 步：确认这是独立仓库（排雷检查）

```powershell
git rev-parse --show-toplevel
```

**预期输出**：

```
C:/Users/ASUS/WorkBuddy/2026-09-17-08-30-13/ml-journey
```

⚠️ **如果输出的是 `C:/Users/ASUS`**，说明主目录那个雷又回来了，立刻停下来告诉我。

> 这条命令为什么重要：git 会**向上逐级查找** `.git` 目录。如果项目自己没初始化过仓库，
> 它会一路找到你主目录去 —— 那就等于把整个用户目录纳入了版本控制。先确认边界，再动手。

---

## 第 3 步：看提交历史

```powershell
git log --oneline
```

**预期输出**（4 行）：

```
183dddd docs: 填入远程仓库地址与提交身份说明
fb405d6 docs: 补充仓库地址与作者信息
a6ab9e6 docs: 添加 Git 与 GitHub 操作手册
6c31df1 init: 初始化机器学习学习仓库
```

`q` 键退出（如果内容太多分页了）。

---

## 第 4 步：确认工作区状态

```powershell
git status
```

**预期输出**：

```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        docs/VERIFY_GUIDE.md

nothing added to commit but untracked files present
```

**两个关键信息**：

1. `Your branch is up to date with 'origin/main'` —— 本地和远程同步了，没有落后也没有领先
2. `docs/VERIFY_GUIDE.md` 显示为 **Untracked**（未跟踪）—— 这是我要你提交的文件

---

## 第 5 步：直接问远程仓库（终极验证）

前面几步验证的都是**本地**信息。这一步真正去 GitHub 问一次：

```powershell
git fetch
git branch -vv
```

**预期输出**：

```
* main 183dddd [origin/main] docs: 填入远程仓库地址与提交身份说明
```

注意方括号里是干净的 `[origin/main]` —— **不带 `gone`**。如果你之前看到过 `gone`，跑完 `git fetch` 就正常了。

再跑一条更彻底的：

```powershell
git ls-remote --heads origin
```

**预期输出**：

```
183dddd82c65e80e48260a30185252bc1562178e        refs/heads/main
```

**这一行的哈希值必须和本地一致。** 对照方法：

```powershell
git rev-parse HEAD
```

两边的 40 位哈希完全相同 = 远程内容和你本地**一模一样**，推送确实成功了。

---

## 第 6 步：用浏览器确认

打开：

```
https://github.com/ShiyiH11/ml-journey
```

**应该看到**：

- 仓库名 `ShiyiH11/ml-journey`，旁边有 `Public` 标签
- README 渲染出来了，**6 张图表正常显示**（这是重点检查项）
- 文件列表里能看到 `01-basics/`、`docs/`、`outputs/` 等
- 右上角提交数显示 `5 Commits`（等你完成下面第 7 步后会变多）
- 点进 `01-basics/03_first_model.py`，代码有高亮

**如果 README 里的图片显示不出来**（出现破图图标）：告诉我，这通常是图片路径大小写问题。

---

---

# 接下来：走一遍完整的日常提交流程

前面都是**只读**操作，很安全。下面这几步会**真正修改远程仓库** —— 这就是最需要练熟的部分。

## 第 7 步：把这份文档提交上去

严格按顺序执行，**每一条都先看输出对不对再走下一步**。

### ① 先看状态（养成习惯）

```powershell
git status
```

确认只有 `docs/VERIFY_GUIDE.md` 一个未跟踪文件。

### ② 精确添加这一个文件

```powershell
git add docs/VERIFY_GUIDE.md
```

> ⚠️ **注意这里没用 `git add -A`**。
> `-A` 会把当前目录下**所有**改动一股脑加进去 —— 包括你不想提交的临时文件、密钥、大数据。
> 明确指定文件名，是更安全的习惯。

### ③ 再确认一次（关键！）

```powershell
git status
```

**预期输出**：

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   docs/VERIFY_GUIDE.md
```

看到 `Changes to be committed` 下面**只有这一个文件**，才能继续。

**这就是 `git add` 和 `git commit` 之间那道保险。** 多花 3 秒，能避免 90% 的误提交事故。

### ④ 提交

```powershell
git commit -m "docs: 添加推送验证与日常提交手册"
```

**预期输出**（数字可能不同）：

```
[main 8f3a1c2] docs: 添加推送验证与日常提交手册
 1 file changed, 180 insertions(+)
 create mode 100644 docs/VERIFY_GUIDE.md
```

方括号里的 `8f3a1c2` 是这次提交的新哈希。

### ⑤ 推送

```powershell
git push
```

> 注意：**这次不用带 `origin main`**。
> 因为第一次推送时用了 `git push -u origin main`，`-u` 已经建立了**跟踪关系**，
> 以后在这个分支上直接 `git push` 就够了。

**预期输出**：

```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (3/3), 1.02 KiB | 512.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), done.
To https://github.com/ShiyiH11/ml-journey.git
   183dddd..8f3a1c2  main -> main
```

**最后一行是判断成功的唯一标准**：

```
183dddd..8f3a1c2  main -> main
 ↑旧哈希   ↑新哈希
```

两个哈希之间用 `..` 连接、箭头是 `->`（不是 `<—` 强制推送），就说明干净地推进了一个提交。

### ⑥ 刷新 GitHub 页面

回到 https://github.com/ShiyiH11/ml-journey ，`Ctrl + F5` 强制刷新：

- 提交数 +1
- 文件树里出现 `docs/VERIFY_GUIDE.md`
- 点右上角你的头像 → **Your profile** → 看贡献图，今天的格子应该**变绿了**

> 第一次推送时 GitHub 可能有几分钟延迟才更新贡献图，属正常。

---

## 出错怎么办

| 报错信息 | 原因 | 解决 |
|---|---|---|
| `remote origin already exists` | 重复执行了 `git remote add` | 不用管，远程已经配好了 |
| `Your local changes would be overwritten` | 有未提交的改动挡住了 | 先 `git status` 看清楚，再决定 add 还是 stash |
| `fatal: not a git repository` | 当前目录不对 | 重新执行第 1 步的 `cd` |
| `Authentication failed` | 登录凭据过期 | 会弹浏览器，重新授权 GitHub 即可 |
| `rejected - non-fast-forward` | 远程有你本地没有的提交 | **不要用 `-f` 强推**，先 `git pull --rebase` 再推 |
| 中文显示成乱码 | 编码问题 | 在终端里执行 `chcp 65001` 切到 UTF-8 |

**遇到任何没见过的报错：整段复制给我，不要自己乱试 `-f` / `--hard` 这类强制命令。**

---

## 命令速查（贴墙版）

```powershell
# 每一次动手前
git status                    # 现在是什么状态？
git rev-parse --show-toplevel # 我在哪个仓库里？（排雷）

# 提交四步曲
git status                    # 1. 看
git add <具体文件名>           # 2. 加（不要用 -A）
git status                    # 3. 再确认一遍
git commit -m "类型: 说明"     # 4. 提交
git push                      # 5. 推送

# 查看
git log --oneline             # 提交历史
git diff                      # 还没 add 的改动内容
git diff --staged             # 已 add、待提交的改动内容

# 撤销（安全向）
git restore <文件>             # 丢弃工作区的修改（不可逆，慎用）
git restore --staged <文件>    # 只把它从暂存区拿出来，文件不动
```

---

## 提交信息怎么写

格式：`类型: 说明`

| 类型 | 用途 | 例子 |
|---|---|---|
| `feat` | 新增功能/代码 | `feat: 添加决策树调参实验` |
| `docs` | 文档 | `docs: 补充交叉验证说明` |
| `fix` | 修 bug | `fix: 修正箱线图参数名` |
| `refactor` | 重构（不改功能） | `refactor: 抽离绘图工具函数` |
| `chore` | 杂项（配置、依赖） | `chore: 升级 pandas 到 3.0.5` |

**说明部分用祈使句，别写「我改了…」**：

- ✅ `fix: 修正箱线图参数名`
- ❌ `我修改了一下箱线图的参数`

原因：`git log --oneline` 读起来就是一句话的列表，主语默认是「这次提交」。

---

*本手册由小淮编写 · 2026-09-17*
