# Git 与 GitHub 操作手册

写给刚开始用 Git 的自己。每次忘了就来这里查。

---

## 一、首次推送到 GitHub

### 第 1 步：在 GitHub 上建一个空仓库

1. 打开 https://github.com/new
2. **Repository name** 填 `ml-journey`
3. **Description** 可以填：`从零开始的机器学习实践记录`
4. 选择 **Public**（公开，这样别人能看到，对找工作/找导师有用）
5. ⚠️ **不要勾选** "Add a README file"、".gitignore"、license
   —— 因为你本地已经有了，勾了会造成冲突
6. 点 **Create repository**

### 第 2 步：关联远程仓库

创建后 GitHub 会显示一段命令。你只需要执行这两条（把 `你的用户名` 换成实际的）：

```bash
cd C:\Users\ASUS\WorkBuddy\2026-09-17-08-30-13\ml-journey

git remote add origin https://github.com/你的用户名/ml-journey.git
git push -u origin main
```

### 第 3 步：登录

第一次推送会弹出浏览器要求登录 GitHub，授权即可。
如果用的是 HTTPS，可能会让你输入用户名和密码 —— 密码要填 **Personal Access Token**，不是账号密码。

> 获取 Token：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → 勾选 `repo` 权限

---

## 二、日常提交流程（最常用）

每次做完一点东西，就提交一次：

```bash
cd C:\Users\ASUS\WorkBuddy\2026-09-17-08-30-13\ml-journey

git status              # 1. 看看改了哪些文件
git add -A              # 2. 全部加入暂存区
git commit -m "说明"    # 3. 提交
git push                # 4. 推到 GitHub
```

**四步走，记住就行。**

---

## 三、提交信息怎么写

写清楚「做了什么」，不要写「更新」「修改」这种废话。

**糟糕的例子：**
```
更新
改了一下
提交
```

**好的例子：**
```
feat: 完成第 4 课特征工程与 GridSearchCV 调参
fix: 修正 boxplot 的 labels 参数（matplotlib 3.11 已改名）
docs: 补充 README 中的交叉验证结果表
```

推荐用前缀（叫 Conventional Commits，很常见）：

| 前缀 | 用途 |
|---|---|
| `feat:` | 新增功能 / 新课程 |
| `fix:` | 修复错误 |
| `docs:` | 只改了文档 |
| `refactor:` | 重构代码，功能不变 |
| `chore:` | 杂项（依赖升级、配置调整） |

---

## 四、常用命令速查

```bash
# 看状态
git status                  # 哪些文件改了
git log --oneline -10       # 最近 10 次提交
git diff                    # 具体改了什么内容

# 撤销操作
git restore <文件>          # 撤销单个文件的修改（未暂存）
git restore --staged <文件> # 从暂存区拿出（已 add 但后悔）
git reset --soft HEAD~1     # 撤销上一次提交，保留改动

# 分支
git branch                  # 查看分支
git checkout -b 新分支名     # 创建并切换分支
git checkout main           # 切回 main
git merge 分支名             # 把分支合并到当前分支

# 远程
git remote -v               # 查看远程地址
git pull                    # 拉取远程更新
git push                    # 推送本地提交
```

---

## 五、常见错误与解决

### 1. `fatal: not a git repository`

当前目录不是仓库，或者进了子目录。用 `git status` 确认，或 `cd` 到仓库根目录。

### 2. 推送被拒绝 `rejected - non-fast-forward`

远程有你本地没有的提交（通常是你在网页上改过文件）。

```bash
git pull --rebase
git push
```

### 3. 不小心提交了不该提交的文件

```bash
git rm --cached 文件名      # 从版本控制移除，但保留本地文件
# 然后把这个文件加进 .gitignore
git commit -m "chore: 移除误提交的文件"
```

### 4. 想改最后一次提交的说明

```bash
git commit --amend -m "新的说明"
```

### 5. 提交作者写错了

```bash
git commit --amend --author="名字 <邮箱>" --no-edit
```

---

## 六、⚠️ 最重要的一条安全规则

**永远不要在「文件夹套文件夹」的层级不确定的情况下执行 `git add -A`。**

`git add -A` 会暂存**当前仓库根目录下的所有变化**。
如果你不小心在错误的目录（比如用户主目录、桌面）初始化了仓库，
一条 `git add -A` + `git push` 就可能把你的私人文件全部上传到公开的 GitHub 上。

**每次提交前先跑 `git status`，确认列表里的文件都是你想提交的。**

---

*最后更新：2026-09-17*
