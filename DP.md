# Documentation Process Guide

**Purpose**: Maintain clean, up-to-date documentation for the Cooin project.

---

## 🖥️ MULTI-MACHINE DOCUMENTATION (CRITICAL!)

**This project is developed on TWO computers simultaneously:**
- 💻 **Windows** - Primary development machine
- 🍎 **Mac** - Secondary development machine

### 🚨 Machine-Specific Files

#### Windows Files (Windows ✍️ WRITES, Mac 👀 READS)
- `HISTORY.md`, `TODO.md`, `README.md`, `HOW-TO-LAUNCH-WEB-APP.md`

#### Mac Files (Mac ✍️ WRITES, Windows 👀 READS)
- `HISTORY_MAC.md`, `TODO_MAC.md`, `README_MAC.md`, `HOW-TO-LAUNCH-WEB-APP_MAC.md`

#### Shared Files (Both machines can read/edit carefully)
- `DP.md` - This documentation process guide
- `TECH_STACK.md` - Technology stack documentation
- Code files in `cooin-backend/`, `cooin-frontend/`, `cooin-ios/`

### 📝 Claude's Workflow

**EVERY session, Claude MUST:**
1. **Ask the user**: "¿Estás en Mac o Windows?"
   - If Mac 🍎 → Document in `*_MAC.md` files
   - If Windows 💻 → Document in regular files
2. **Never edit the other machine's files**

### 🔄 Sync Strategy
```bash
# Before starting work
git pull origin main

# After finishing work (Mac)
git add HISTORY_MAC.md TODO_MAC.md README_MAC.md
git commit -m "docs: Session X on Mac 🍎"
git push origin main

# After finishing work (Windows)
git add HISTORY.md TODO.md README.md
git commit -m "docs: Session X on Windows 💻"
git push origin main
```

---

## 📋 Documentation Files Overview

| File | Purpose | When to Read |
|------|---------|--------------|
| **README** | Project setup & overview | First time, setup changes |
| **TODO** | Current tasks & status | START of every session |
| **HISTORY** | Session changelog | When debugging, reviewing changes |
| **HOW-TO-LAUNCH** | Launch instructions | First launch, troubleshooting |
| **DP** | Documentation process | When unsure how to document |
| **TECH_STACK** | Technology details | When stack changes |

---

## 🔄 Standard Documentation Flow

### At START of Each Session
1. **Review TODO.md** - Check pending tasks
2. **Note Session Number** - Increment from last session (check HISTORY.md)

### DURING the Session
- Track files modified
- Note bugs fixed and features added

### At END of Each Session

#### 1. Update HISTORY.md (5 minutes)
```markdown
## YYYY-MM-DD (Session X) - Brief Title

**Goal**: One-sentence objective.

**Changes/Fixes**:
1. **Feature/Fix**: Description
2. **Another Change**: Description

**Files Changed**:
- `filename:line` - What changed

**Status**: ✅ Working / ⚠️ Blocked / 🔄 In Progress

---
```

#### 2. Update TODO.md (3 minutes)
- Update session header
- Move completed items to "✅ Completed This Session"
- Update "In Progress" section
- Add new tasks if discovered
- Update timestamp

#### 3. Update README.md (Only if needed)
- ✅ New major feature, setup changes, stack changes
- ❌ Don't update for minor fixes/refactors

#### 4. Update HOW-TO-LAUNCH.md (Only if needed)
- Update if: Launch commands changed, new steps, URL changes

---

## 📝 Writing Style Guide

### General Rules
1. **Be Concise**: 1-2 sentences per point
2. **Use Active Voice**: "Fixed bug" not "Bug was fixed"
3. **Include Context**: Why it matters, not just what changed
4. **Add Links**: Reference `file:line` for specific changes

### Emoji Guide
| Emoji | Meaning | Usage |
|-------|---------|-------|
| ✅ | Completed | Finished tasks, working features |
| ❌ | Failed/Broken | Things that don't work |
| ⚠️ | Warning | Known issues, be careful |
| 🔄 | In Progress | Currently working on |
| 🐛 | Bug | Bug fixes, issues |
| ✨ | New Feature | New functionality added |
| 🔧 | Configuration | Config changes, setup updates |
| 📝 | Documentation | Doc updates |

---

## 🎯 Quick Reference: Which File When?

| Situation | File to Read | Section |
|-----------|-------------|---------|
| Starting work today | TODO.md | Current Session → In Progress |
| Need to launch app | HOW-TO-LAUNCH.md | Quick Launch |
| App won't start | HOW-TO-LAUNCH.md | Troubleshooting |
| What changed recently? | HISTORY.md | Top 3 sessions |
| What are known bugs? | TODO.md | Known Issues |
| Project overview? | README.md | Entire file |

---

## 🚫 Common Mistakes to Avoid

1. **Over-documenting**: Keep it scannable
2. **Under-documenting**: Even small changes matter
3. **Inconsistent Formats**: Use the templates
4. **Missing Context**: Explain WHY, not just WHAT
5. **Stale TODOs**: Remove or archive old items
6. **Wrong Dates**: Use YYYY-MM-DD format
7. **Missing File References**: Always cite which files changed

---

## 🎯 Quick Action Commands

**Start New Session:**
```bash
# Check current session number
grep "Session" HISTORY.md | head -1

# Review pending tasks
grep "\[ \]" TODO.md | head -10
```

**End Session:**
```bash
# Commit docs
git add HISTORY.md TODO.md README.md
git commit -m "docs: update session X documentation"
```

---

**Last Updated**: 2025-12-06 (Session 18 - Mac 🍎)
**Maintained By**: Development Team (Mac & Windows)

---

## 🎯 Quick Reference: Mac vs Windows

**If you're on Mac 🍎:**
- Edit: `HISTORY_MAC.md`, `TODO_MAC.md`, `README_MAC.md`, `HOW-TO-LAUNCH-WEB-APP_MAC.md`
- Read: All Windows files for context

**If you're on Windows 💻:**
- Edit: `HISTORY.md`, `TODO.md`, `README.md`, `HOW-TO-LAUNCH-WEB-APP.md`
- Read: All Mac files for context

**Claude MUST ask every session:** "¿Estás en Mac o Windows?"
