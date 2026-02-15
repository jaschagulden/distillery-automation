# Git Setup and Usage Guide

## First Time Setup

### 1. Install Git (if not already installed)

**On Raspberry Pi / Linux:**
```bash
sudo apt-get update
sudo apt-get install git -y
```

**On macOS:**
```bash
# Using Homebrew
brew install git

# Or download from https://git-scm.com/
```

**On Windows:**
Download from https://git-scm.com/

### 2. Configure Git
```bash
# Set your name and email (used in commits)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Optional: Set default branch name to 'main'
git config --global init.defaultBranch main
```

### 3. Create GitHub Account
If you don't have one: https://github.com/join

### 4. Create a New Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `distillery-automation`
3. Description: "Automated distillery control system using Raspberry Pi"
4. Privacy: Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 5. Get Your Repository URL
After creating, GitHub will show you a URL like:
- HTTPS: `https://github.com/yourusername/distillery-automation.git`
- SSH: `git@github.com:yourusername/distillery-automation.git`

Copy this URL - you'll need it in the next step.

---

## Initial Push to GitHub

### 1. Navigate to your project directory
```bash
cd /path/to/distillery-automation
```

### 2. Initialize Git repository
```bash
git init
```

### 3. Add all files
```bash
git add .
```

### 4. Create first commit
```bash
git commit -m "Initial commit: Project structure and documentation"
```

### 5. Add GitHub as remote
```bash
# Replace YOUR_REPO_URL with the URL you copied from GitHub
git remote add origin YOUR_REPO_URL

# Example:
# git remote add origin https://github.com/yourusername/distillery-automation.git
```

### 6. Push to GitHub
```bash
git push -u origin main
```

**Note:** You may be prompted for your GitHub username and password/token.

---

## Daily Workflow

### After Each Work Session

1. **Check what changed:**
```bash
git status
```

2. **Add new or modified files:**
```bash
# Add all changes
git add .

# Or add specific files
git add src/hardware/load_cell.py
git add config/hardware_config.yaml
```

3. **Commit with descriptive message:**
```bash
git commit -m "Add load cell interface module and calibration"
```

4. **Push to GitHub:**
```bash
git push
```

### Good Commit Message Examples
- `"Add load cell interface module"`
- `"Implement PID controller with anti-windup"`
- `"Fix thermocouple reading error handling"`
- `"Update hardware specifications with final part numbers"`
- `"Add fill sequence automation"`

### Poor Commit Message Examples
- `"Updates"`
- `"Fixed stuff"`
- `"asdf"`
- `"Changes from today"`

---

## Working with a Collaborator

### When Collaborator Joins

1. **Add them as a collaborator on GitHub:**
   - Go to your repository settings
   - Click "Collaborators"
   - Add their GitHub username

2. **They clone the repository:**
```bash
git clone https://github.com/yourusername/distillery-automation.git
cd distillery-automation
```

### Daily Workflow with Team

**Before starting work each day:**
```bash
# Pull latest changes from GitHub
git pull
```

**After making changes:**
```bash
git add .
git commit -m "Descriptive message"
git push
```

**If you get a conflict:**
```bash
# Pull latest changes
git pull

# Git will tell you which files have conflicts
# Open those files and resolve conflicts manually
# Look for markers like:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> 

# After resolving, add and commit
git add .
git commit -m "Resolve merge conflict in [filename]"
git push
```

---

## Useful Commands

### View History
```bash
# See recent commits
git log --oneline

# See changes in last commit
git show
```

### Undo Changes

```bash
# Discard changes to a file (before committing)
git checkout -- filename.py

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Undo last commit (discards changes) - CAREFUL!
git reset --hard HEAD~1
```

### Branching (Advanced)

```bash
# Create a new branch for a feature
git checkout -b feature/new-gui

# Work on your feature, commit changes
git add .
git commit -m "Add new GUI feature"

# Push branch to GitHub
git push -u origin feature/new-gui

# Switch back to main
git checkout main

# Merge feature when ready
git merge feature/new-gui

# Delete branch
git branch -d feature/new-gui
```

---

## Best Practices

1. **Commit often** - Small, focused commits are easier to understand
2. **Pull before you push** - Avoid conflicts by staying up to date
3. **Write clear messages** - Future you will thank you
4. **Don't commit secrets** - API keys, passwords, etc. (use .gitignore)
5. **Test before committing** - Make sure code works
6. **Use branches for big features** - Keep main branch stable

---

## GitHub Features to Use

### Issues
Track tasks, bugs, and feature requests:
- Go to "Issues" tab
- Create new issue
- Assign to team member
- Reference in commits: `"Fix temperature reading bug (closes #5)"`

### Projects
Organize work with kanban boards:
- Create project board
- Add columns: To Do, In Progress, Done
- Move issues across columns

### Wiki
Document your project:
- Hardware assembly instructions
- Operating procedures
- Troubleshooting guide

---

## Help

If you get stuck:
```bash
# Get help for any git command
git help <command>

# Example:
git help commit
git help push
```

Or ask your collaborator or check:
- https://git-scm.com/doc
- https://docs.github.com/en

---

## Quick Reference Card

```bash
# Setup
git init                          # Initialize repository
git clone <url>                   # Clone existing repository

# Daily workflow  
git status                        # Check what changed
git add .                         # Stage all changes
git add <file>                    # Stage specific file
git commit -m "message"           # Commit changes
git push                          # Push to GitHub
git pull                          # Pull from GitHub

# Information
git log                           # View history
git diff                          # See unstaged changes
git diff --staged                 # See staged changes

# Undo
git checkout -- <file>            # Discard changes to file
git reset HEAD <file>             # Unstage file
```
