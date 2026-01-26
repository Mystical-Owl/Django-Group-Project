# Git Operations Guide: Adding, Committing, and Pushing Files

## Scenario
You have a file `questionnaire_scoring.py` that you want to:
1. Add to git tracking
2. Pull latest changes from remote
3. Commit with a specific message
4. Push to remote repository

## Prerequisites
- Git installed on your system
- Repository already cloned locally
- You're in the correct branch

## Step-by-Step Instructions

### 1. Check Current Git Status
Always start by checking the current status to see what files are modified, staged, or untracked.

```bash
git status
```

**Expected output example:**
```
On branch franco
Your branch is ahead of 'origin/franco' by 8 commits.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    questionnaire_scoring.py
    other_file.py

nothing added to commit but untracked files present (use "git add" to track)
```

### 2. Add Specific File to Git Staging
Add the file you want to commit to the staging area.

```bash
git add questionnaire_scoring.py
```

To add all untracked/modified files:
```bash
git add .
```

**Verification:** Run `git status` again to see the file is now staged:
```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    new file:   questionnaire_scoring.py
```

### 3. Pull Latest Changes from Remote
Before committing, always pull the latest changes from the remote repository to avoid conflicts.

```bash
git pull origin franco
```

**Note:** Replace `franco` with your branch name.

**Expected output if up to date:**
```
Already up to date.
```

**If there are updates:** Git will merge them automatically if there are no conflicts.

### 4. Commit with Descriptive Message
Commit the staged changes with a meaningful commit message.

```bash
git commit -m "scoring_from_questionnaire 23/2/2026"
```

**Expected output:**
```
[franco a4ef983] scoring_from_questionnaire 23/2/2026
1 file changed, 411 insertions(+)
 create mode 100644 questionnaire_scoring.py
```

**Commit message best practices:**
- Use present tense ("Add feature" not "Added feature")
- Keep it concise but descriptive
- Include reference numbers if applicable (e.g., "Fix #123")

### 5. Push Changes to Remote Repository
Push your committed changes to the remote repository.

```bash
git push origin franco
```

**Expected output:**
```
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
...
To github.com:Mystical-Owl/Django-Group-Project.git
   5f59fb6..a4ef983  franco -> franco
```

### 6. Verify Everything is Up to Date
Final verification step:

```bash
git status
```

**Expected output:**
```
On branch franco
Your branch is up to date with 'origin/franco'.

nothing to commit, working tree clean
```

## Common Variations

### Committing Multiple Files
```bash
git add file1.py file2.py
git commit -m "Add multiple files"
```

### Amending the Last Commit
If you need to add more changes to the last commit:
```bash
git add additional_file.py
git commit --amend -m "Updated commit message"
```

### Viewing Commit History
```bash
git log --oneline -n 5
```

### Undoing Changes
- Unstage a file: `git restore --staged questionnaire_scoring.py`
- Discard local changes: `git checkout -- questionnaire_scoring.py`

## Troubleshooting

### Merge Conflicts
If `git pull` results in conflicts:
1. Resolve conflicts in the affected files
2. Mark as resolved: `git add conflicted_file.py`
3. Continue merge: `git commit`

### Permission Issues
Ensure you have write access to the repository and are authenticated.

### Wrong Branch
Check current branch: `git branch`
Switch branches: `git checkout branch_name`

## Summary Workflow
1. `git status` - Check current state
2. `git add <file>` - Stage changes
3. `git pull origin <branch>` - Get latest changes
4. `git commit -m "message"` - Commit with message
5. `git push origin <branch>` - Push to remote
6. `git status` - Verify completion

This workflow ensures your changes are properly tracked, synchronized with the team, and safely stored in the remote repository.
