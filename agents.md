# Agent 简单协作流程

## 使用场景

两个 Agent 在同一个仓库、同一个 `main` 分支上协作修改文档。

---

## 核心原则

1. 所有修改先在本地完成
2. 修改前先同步 GitHub 最新内容
3. 修改后及时提交并推送
4. 推送前再同步一次，避免覆盖另一个 Agent 的修改
5. 不使用 `git push --force`

---

## 每次工作流程

### 1. 查看本地状态

```bash
git status
```

如果有未提交内容，先处理完再开始新任务。

---

### 2. 拉取 GitHub 最新内容

```bash
git pull --rebase origin main
```

作用：确保本地是最新版本。

---

### 3. 本地修改文件

在本地完成文档修改。

如果需要，更新 `README.md`。

---

### 4. 查看修改内容

```bash
git status
git diff
```

确认这次只改了该改的内容。

---

### 5. 提交修改

```bash
git add .
git commit -m "描述本次修改"
```

---

### 6. 推送前再次同步

```bash
git pull --rebase origin main
```

作用：防止另一个 Agent 在你工作期间已经推送了新内容。

---

### 7. 推送到 GitHub

```bash
git push origin main
```

---

## 冲突处理

如果 `git pull --rebase origin main` 出现冲突：

1. 不要强制推送
2. 执行：

```bash
git status
```

3. 打开冲突文件，手动保留正确内容
4. 然后执行：

```bash
git add .
git rebase --continue
git push origin main
```

---

## 禁止行为

```bash
git push --force
```

两个 Agent 协作时，禁止强制推送。
