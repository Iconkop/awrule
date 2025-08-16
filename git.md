# Git 使用方法完全指南 (Markdown 版)

Git 是一个免费、开源的分布式版本控制系统，旨在快速高效地处理从小型到大型的各种项目。无论你是个人开发者还是团队成员，Git 都是代码管理和协作的必备工具。

---

## 一、核心概念

在开始使用指令前，理解 Git 的几个核心概念至关重要：

1.  **工作区 (Working Directory)**：你在电脑上能看到的项目目录，是你直接编辑文件的地方。
2.  **暂存区 (Staging Area / Index)**：一个临时的存储区域，用于存放你想要在下一次提交中包含的更改。使用 `git add` 命令将工作区的更改添加到暂存区。
3.  **本地仓库 (Local Repository)**：存储了项目所有版本历史记录的地方（`.git` 文件夹）。使用 `git commit` 命令将暂存区的更改永久保存到本地仓库。
4.  **远程仓库 (Remote Repository)**：托管在网络服务器上的项目仓库（例如 GitHub, GitLab），用于团队协作和数据备份。
5.  **分支 (Branch)**：独立的开发线。创建分支可以让你在不影响主线（通常是 `main` 或 `master`）的情况下开发新功能或修复问题。
6.  **HEAD**：一个指向你当前所在分支最新提交的指针。

**基本工作流程**：
在**工作区**修改文件 -> 使用 `git add` 将更改添加到**暂存区** -> 使用 `git commit` 将暂存区的更改提交到**本地仓库** -> （可选）使用 `git push` 将本地仓库的提交推送到**远程仓库**。

![Git Workflow Diagram](https://i.imgur.com/t3oYGDL.png)

---

## 二、初次配置

在你开始使用 Git 之前，需要配置你的用户信息（用户名和邮箱），这些信息会出现在你的每一次提交记录中。

* 配置你的用户名：
    ```bash
    git config --global user.name "Your Name"
    ```

* 配置你的邮箱地址：
    ```bash
    git config --global user.email "your.email@example.com"
    ```

* （可选）查看你的配置信息：
    ```bash
    git config --list
    ```

`--global` 标志表示这个配置适用于你系统上的所有 Git 仓库。如果想为特定项目设置不同的信息，可以去掉 `--global` 并在该项目目录中运行命令。

---

## 三、创建与克隆仓库

#### 1. 初始化新仓库

如果你有一个尚未进行版本控制的项目目录，可以将其初始化为 Git 仓库。

* 进入你的项目目录：
    ```bash
    cd my-project
    ```
* 初始化一个新的 Git 仓库：
    ```bash
    git init
    ```
    这会在当前目录下创建一个 `.git` 子目录，其中包含仓库所需的所有文件。

#### 2. 克隆现有仓库

从远程服务器（如 GitHub）上克隆一个已存在的项目。

* 克隆一个远程仓库到本地（请将 `<repository_url>` 替换为实际地址）：
    ```bash
    git clone <repository_url>
    ```

---

## 四、日常基本操作（核心工作流程）

这是你每天都会用到的指令。

#### 1. 检查状态

查看工作区和暂存区的状态，了解哪些文件被修改、添加或删除了。

```bash
git status
```

#### 2. 添加到暂存区

跟踪新文件或将已修改的文件放入暂存区，准备下一次提交。

* 添加指定文件：
    ```bash
    git add <file_name>
    ```
* 添加当前目录下所有更改（新增、修改、删除）：
    ```bash
    git add .
    ```

#### 3. 提交更改

将暂存区的所有内容提交到本地仓库，并附上一条描述性的提交信息。

* 提交并直接在命令行中添加简短信息（常用）：
    ```bash
    git commit -m "Your descriptive commit message"
    ```
* 将 `git add` 和 `git commit` 合并为一步（只对已跟踪过的文件有效）：
    ```bash
    git commit -am "A shortcut for adding and committing"
    ```

#### 4. 查看历史

查看项目的提交历史记录。

* 显示完整的提交历史：
    ```bash
    git log
    ```
* 以更简洁的单行格式显示历史：
    ```bash
    git log --oneline
    ```
* 以图形化的方式显示分支和合并历史：
    ```bash
    git log --graph --oneline --decorate --all
    ```

#### 5. 查看差异

比较文件在不同状态下的差异。

* 查看工作区与暂存区的差异：
    ```bash
    git diff
    ```
* 查看暂存区与最新提交（HEAD）的差异：
    ```bash
    git diff --staged
    ```
* 查看工作区与最新提交的差异：
    ```bash
    git diff HEAD
    ```

---

## 五、分支管理

分支是 Git 的核心功能，它允许你并行开发多个功能。

#### 1. 查看与创建分支

* 列出所有本地分支（当前分支前会有一个 `*`）：
    ```bash
    git branch
    ```
* 列出所有本地和远程分支：
    ```bash
    git branch -a
    ```
* 创建一个新分支：
    ```bash
    git branch <branch-name>
    ```
* 删除一个已经合并的分支：
    ```bash
    git branch -d <branch-name>
    ```
* 强制删除一个未合并的分支（慎用）：
    ```bash
    git branch -D <branch-name>
    ```
* 全局默认分支 :
    ```bash
    git config --global init.defaultBranch main
    ```

#### 2. 切换分支

* 切换到一个已存在的分支：
    ```bash
    git switch <branch-name>
    ```
* 创建并立即切换到新分支：
    ```bash
    git switch -c <new-branch-name>
    ```
    （`git checkout` 也能完成同样功能，但 `git switch` 语义更清晰，是推荐的新命令）

#### 3. 合并分支

将一个分支的更改合并到当前所在的分支。

* 首先，切换到你想要并入的目标分支（例如 `main`）：
    ```bash
    git switch main
    ```
* 然后，运行 `merge` 命令将 `feature-branch` 合并进来：
    ```bash
    git merge <feature-branch-name>
    ```

**解决合并冲突**：如果两个分支都修改了同一个文件的同一部分，Git 无法自动合并，就会产生冲突。此时你需要：
1.  手动打开冲突的文件，编辑内容，解决冲突。
2.  使用 `git add` 将解决后的文件标记为已解决：
    ```bash
    git add <conflicted-file-name>
    ```
3.  运行 `git commit` 完成合并：
    ```bash
    git commit
    ```

---

## 六、与远程仓库协作

这部分指令用于多人协作和同步代码。

#### 1. 管理远程仓库

* 查看当前配置的远程仓库：
    ```bash
    git remote -v
    ```
* 添加一个新的远程仓库（通常，默认的远程仓库名为 `origin`）：
    ```bash
    git remote add <remote-name> <repository_url>
    ```
* 删除一个远程仓库：
    ```bash
    git remote remove <remote-name>
    ```

#### 2. 推送更改

将本地仓库的提交推送到远程仓库。

* 将当前分支的提交推送到名为 `origin` 的远程仓库：
    ```bash
    git push origin <branch-name>
    ```
* 第一次推送一个新创建的本地分支时，需要设置上游（upstream）跟踪关系：
    ```bash
    git push -u origin <branch-name>
    ```

#### 3. 拉取和获取更改

从远程仓库更新你的本地仓库。

* 从远程仓库获取（fetch）最新数据，但不自动合并（merge）：
    ```bash
    git fetch <remote-name>
    ```
* 从远程仓库拉取（pull）最新数据，它会自动 fetch 并 merge：
    ```bash
    git pull origin <branch-name>
    ```

---

## 七、撤销操作

当犯了错误时，这些指令可以帮你“回到过去”。

#### 1. 修改最后一次提交

如果你刚刚提交完，但发现提交信息写错了，或者漏掉了一个文件。

* 使用 `--amend` 选项来重新提交（这会打开编辑器让你修改提交信息）：
    ```bash
    git commit --amend
    ```
    **注意**：不要对已经推送到远程仓库的提交使用 `--amend`。

#### 2. 撤销工作区的修改

如果你想丢弃工作区对某个文件的修改。

* 使用 `restore` 恢复文件：
    ```bash
    git restore <file_name>
    ```
* 丢弃所有工作区的修改：
    ```bash
    git restore .
    ```

#### 3. 取消暂存

如果你用 `git add` 把文件添加到了暂存区，但想把它撤销回来。

```bash
git restore --staged <file_name>
```

#### 4. 重置提交历史（危险操作）

`git reset` 可以将 `HEAD` 指针移动到指定的提交。

* `--soft`: 仅移动 `HEAD` 指针，保留暂存区和工作区的更改。
    ```bash
    git reset --soft <commit_id>
    ```
* `--mixed` (默认): 移动 `HEAD`，并重置暂存区，但保留工作区的更改。
    ```bash
    git reset --mixed <commit_id>
    ```
* `--hard`: 彻底重置！移动 `HEAD`，重置暂存区和工作区，所有后续更改都会丢失（慎用！）。
    ```bash
    git reset --hard <commit_id>
    ```

#### 5. 创建一个反向提交

`git revert` 会创建一个新的提交，其内容正好与你想要撤销的某个提交相反。这是一种安全地“撤销”公开历史的方式。

* 创建一个新的提交来撤销指定 `commit_id` 的更改：
    ```bash
    git revert <commit_id>
    ```
