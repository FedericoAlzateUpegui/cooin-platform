# Documentation Process Guide

**Purpose**: Maintain clean, up-to-date documentation for the Cooin project.

---

## 📋 Documentation Files Overview

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| **HISTORY.md** | Session-by-session changelog | After each session |
| **TODO.md** | Current tasks and roadmap | Daily/per session |
| **README.md** | Project overview and setup | As features change |
| **HOW-TO-LAUNCH-WEB-APP.md** | Launch instructions | When setup changes |
| **TECH_STACK.md** | Technology documentation | When stack changes |

---

## 📖 How to Read and Use Each Documentation File

### 🗂️ README.md - Your Starting Point

**When to Read:**
- First time seeing the project
- Need quick project overview
- Setting up development environment
- Looking for documentation links

**How to Read:**
```markdown
1. Read top section → Get project name, description, features
2. Check "Quick Start" → Commands to launch the app
3. Review "Tech Stack" → Understand technologies used
4. Scan "Common Issues" → Known problems and fixes
5. Follow "Documentation" links → Deep dive into specific areas
```

**What to Look For:**
- Prerequisites (Python, Node.js versions)
- Installation commands
- Environment variables needed
- Links to detailed guides

**Example Questions README Answers:**
- "How do I start the backend?"
- "What technologies does this use?"
- "Where's the API documentation?"
- "What are the known issues?"

---

### 📝 TODO.md - Your Daily Task List

**When to Read:**
- **START of every session** (most important!)
- Need to know what's pending
- Checking current session tasks
- Planning next work

**How to Read:**
```markdown
# Read in this order:

1. "Current Session" section (top)
   ↓ What are we working on NOW?

2. "In Progress" tasks
   ↓ What's actively being worked on?

3. "Completed This Session"
   ↓ What did we just finish?

4. "Known Issues" section
   ↓ What problems exist?

5. "Key Commands Reference"
   ↓ Copy-paste commands to run
```

**Structure Explained:**
```markdown
## 🚀 Current Session (Session X)
   ↑ Always at top, increments each session

### 🔨 In Progress
   ↑ Active work (1-3 items max)

### ✅ Completed This Session
   ↑ Just finished (cleared next session)

### 🌐 Local Development
   ↑ Commands to run app locally

### 🌍 Public Sharing Setup
   ↑ Commands for Cloudflare tunnels

## 🐛 Known Issues
   ↑ Current bugs and problems

## 🔧 Future Enhancements
   ↑ Nice-to-have features (longer term)
```

**What to Look For:**
- [ ] Unchecked boxes = Pending work
- [x] Checked boxes = Completed work
- ⚠️ Warnings = Be careful!
- ✅ Check marks = Fixed/working

**Example Questions TODO Answers:**
- "What should I work on next?"
- "What commands do I run to start development?"
- "What issues are blocking progress?"
- "What's the current session number?"

**Pro Tip:**
```bash
# Quick view of pending tasks
cat TODO.md | grep "\[ \]" | head -10
```

---

### 📚 HISTORY.md - Your Project Timeline

**When to Read:**
- Need to know what changed
- Debugging - "When did this break?"
- Understanding past decisions
- Onboarding new developers

**How to Read:**
```markdown
# Sessions are listed NEWEST FIRST (top to bottom)

## 2025-11-05 (Session 8) ← Most recent
   ↓
## 2025-11-03 (Session 7) ← One session ago
   ↓
## 2025-10-25 (Session 6) ← Two sessions ago
   ↓
...older sessions...
```

**Each Session Entry Contains:**
```markdown
## Date (Session X) - Title
**Goal**: What we tried to accomplish
**Changes**: What actually changed
**Files Changed**: Which files were modified
**Status**: Did it work?
```

**What to Look For:**
- **Recent sessions** (top 5-10) = Recent changes
- **Files Changed** = What to review if bug appeared
- **Status** = Was the goal achieved?
- **Key Learning** = Important insights

**How to Find Specific Information:**

**Q: "When was the config.ts file last changed?"**
```bash
grep -n "config.ts" HISTORY.md
# Shows all lines mentioning config.ts with line numbers
```

**Q: "What changed in Session 6?"**
```bash
# Read HISTORY.md, search for "Session 6"
# Or use Ctrl+F in your editor
```

**Q: "When did we fix the Python path issue?"**
```bash
grep -n "Python" HISTORY.md | head -5
```

**Example Questions HISTORY Answers:**
- "When did we add form validation?"
- "What was broken in Session 7?"
- "Who made changes to the auth system?"
- "When did we switch from ngrok to Cloudflare?"

**Pro Tip:**
```bash
# See last 3 sessions
head -100 HISTORY.md

# Search for specific file changes
grep "filename" HISTORY.md
```

---

### 🚀 HOW-TO-LAUNCH-WEB-APP.md - Your Launch Guide

**When to Read:**
- **First time launching** the app
- Forgot how to start backend/frontend
- Sharing app with partners (public access)
- Troubleshooting launch issues

**How to Navigate:**
```markdown
# The file has clear sections:

1. Prerequisites
   ↑ What you need installed first

2. Quick Launch (Local Development Only)
   ↑ For working on your own computer

3. Launch with Public Access (Share with Partners)
   ↑ For showing app to others via internet

4. Troubleshooting
   ↑ Common errors and fixes

5. Quick Commands Reference
   ↑ Copy-paste command cheat sheet
```

**Two Main Workflows:**

**Workflow 1: Local Development** (most common)
```markdown
1. Read "Prerequisites" (one time only)
2. Jump to "Quick Launch"
3. Copy Terminal 1 commands → Start backend
4. Copy Terminal 2 commands → Start frontend
5. Open http://localhost:8083
```

**Workflow 2: Share with Partners**
```markdown
1. Follow "Launch with Public Access" section
2. Start 4 terminals (backend, frontend, 2 tunnels)
3. Update config files with new URLs
4. Restart services
5. Share frontend URL with partners
```

**What to Look For:**
- Step-by-step numbered instructions
- Code blocks with `cmd` → Copy these!
- "Wait for:" sections → Know when ready
- "Access at:" → URLs to open in browser

**Common Use Cases:**

**"I need to start working"**
→ Go to "Quick Launch" section
→ Copy commands from Step 1 & 2

**"I need to show this to my partner"**
→ Go to "Launch with Public Access"
→ Follow Steps 1-7 in order

**"Error: Cannot connect to server"**
→ Go to "Troubleshooting" section
→ Find your error message
→ Follow solution steps

**Pro Tip:**
Keep this file open in a browser tab while developing!

---

### 🔗 How the Files Work Together

**Scenario: Starting a New Session**

```markdown
1. Read TODO.md (What needs to be done?)
   ↓
2. Check HISTORY.md (What was last session number?)
   ↓
3. Open HOW-TO-LAUNCH-WEB-APP.md (Start the app)
   ↓
4. Work on task from TODO.md
   ↓
5. Update HISTORY.md (Document what changed)
   ↓
6. Update TODO.md (Mark completed, add new tasks)
```

**Scenario: Debugging an Issue**

```markdown
1. Check TODO.md "Known Issues" (Is this a known bug?)
   ↓
2. Read HISTORY.md (When did this last work?)
   ↓
3. Find session where it broke
   ↓
4. Check "Files Changed" in that session
   ↓
5. Review those files for the bug
```

**Scenario: Onboarding New Developer**

```markdown
1. Start with README.md (Project overview)
   ↓
2. Follow HOW-TO-LAUNCH-WEB-APP.md (Get it running)
   ↓
3. Skim HISTORY.md (Recent 5 sessions - what's been happening?)
   ↓
4. Read TODO.md (What to work on)
   ↓
5. Use DOCUMENTATION_PROCESS.md (How to contribute)
```

---

## 🎯 Quick Reference: Which File When?

| Situation | File to Read | Section |
|-----------|-------------|---------|
| Starting work today | TODO.md | Current Session → In Progress |
| Need to launch app | HOW-TO-LAUNCH-WEB-APP.md | Quick Launch |
| App won't start | HOW-TO-LAUNCH-WEB-APP.md | Troubleshooting |
| What changed recently? | HISTORY.md | Top 3-5 sessions |
| When was X fixed? | HISTORY.md | Search for X |
| What's the tech stack? | README.md | Tech Stack section |
| What are known bugs? | TODO.md | Known Issues |
| How to share with partners? | HOW-TO-LAUNCH-WEB-APP.md | Launch with Public Access |
| What are the commands? | TODO.md or HOW-TO-LAUNCH | Key Commands Reference |
| Project overview? | README.md | Entire file (top to bottom) |
| How to document? | DOCUMENTATION_PROCESS.md | This file! |

---

## 🔄 Standard Documentation Flow

### At START of Each Session

1. **Review TODO.md**
   - Check pending tasks
   - Identify what needs to be done
   - Mark current task as "In Progress"

2. **Note Session Number**
   - Increment from last session (check HISTORY.md)
   - Use consistent date format: `YYYY-MM-DD`

---

### DURING the Session

1. **Track Changes**
   - Keep mental note of files modified
   - Note any bugs fixed
   - Record new features added
   - Document any breaking changes

2. **Save Important Commands**
   - Commands that worked
   - Commands that failed (and why)
   - New workflow discoveries

---

### At END of Each Session

#### Step 1: Update HISTORY.md (5 minutes)

**Template:**
```markdown
## YYYY-MM-DD (Session X) - Brief Session Title

**Goal**: One-sentence description of session objective.

**Changes/Fixes**:
1. **Feature/Fix Name**: Description
2. **Another Change**: Description

**Educational Sessions** (if applicable):
- **Topic**: What was taught/explained

**Files Changed**:
- `filename` - What changed
- `another-file` - What changed

**Pending Work**:
- [ ] Incomplete task
- [ ] Follow-up needed

**Key Learning**: Important insight or gotcha discovered

**Status**: Current state (e.g., "Working ✅", "Blocked ⚠️", "In Progress 🔄")

---
```

**Guidelines:**
- Keep descriptions concise (1-2 lines max)
- Focus on WHAT changed, not HOW (code details)
- Include file:line references for specific changes
- Mark status clearly with emojis

---

#### Step 2: Update TODO.md (3 minutes)

**Actions:**
1. **Update Session Header**
   ```markdown
   ## 🚀 Current Session (Session X) - Brief Title
   ```

2. **Move Completed Items**
   ```markdown
   ### ✅ Completed This Session
   - [x] **Task Name** - Brief result
   ```

3. **Update In Progress**
   ```markdown
   ### 🔨 In Progress
   - [ ] **Active Task** - Current status
   ```

4. **Add New Tasks** (if discovered)
   - Add to appropriate section (Technical Improvements, Technical Debt, Future Enhancements)

5. **Update Timestamp**
   ```markdown
   **Last Updated**: YYYY-MM-DD (Session X)
   ```

**Keep It Light:**
- Remove stale/obsolete tasks
- Merge similar tasks
- Archive completed tasks to HISTORY.md
- Maximum 3-5 current session tasks

---

#### Step 3: Update README.md (Only if needed)

**When to Update:**
- ✅ New major feature completed
- ✅ Setup instructions changed
- ✅ Technology stack changed
- ✅ Dependencies updated
- ❌ Don't update for minor fixes
- ❌ Don't update for internal refactors

**What to Update:**
- Status badges (if applicable)
- Feature list
- Prerequisites
- Quick start commands
- Known issues section

---

#### Step 4: Update Other Docs (Only if needed)

**HOW-TO-LAUNCH-WEB-APP.md**
- Update if: Launch commands changed, new steps added, URL changes
- Don't update for: Minor config tweaks

**TECH_STACK.md**
- Update if: New library added, version upgrades, architecture changes

---

### ⚡ Auto-Documentation on Commit (Quick Flow)

**When User Requests a Commit** - Follow this streamlined process:

1. **HISTORY.md** (30 seconds)
   - Add brief session entry at top with date, changes, files modified
   - Keep it concise - 2-4 bullet points max

2. **TODO.md** (30 seconds)
   - Mark completed items with [x]
   - Move to "Completed This Session" section
   - Update "In Progress" if needed

3. **README.md** (Only if major feature added)
   - Update feature list or setup instructions
   - Skip for minor fixes/refactors

4. **Commit to Dev Branch**
   - Stage all modified files
   - Commit with descriptive message
   - NEVER commit to main branch

**Example Quick Update:**
```markdown
# HISTORY.md (add at top)
## 2025-11-06 (Session 9) - [Brief description]
**Changes**: [What changed]
**Files**: [List of files]
**Status**: Working ✅

# TODO.md
Move completed task to ✅ Completed This Session
```

**Pro Tip**: Keep it light - full documentation can be done at end of session, commit docs should be quick and minimal.

---

## 📝 Writing Style Guide

### General Rules

1. **Be Concise**: Aim for 1-2 sentences per point
2. **Use Active Voice**: "Fixed bug" not "Bug was fixed"
3. **Include Context**: Why it matters, not just what changed
4. **Add Links**: Reference file:line for specific changes
5. **Use Emojis Consistently**: See emoji guide below

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
| 🎓 | Learning | Educational content, tutorials |
| 🚀 | Deployment | Launch, production, release |

---

## 🎯 Documentation Checklist

Use this at the end of each session:

```markdown
### Documentation Checklist
- [ ] HISTORY.md updated with Session X entry
- [ ] TODO.md session number incremented
- [ ] TODO.md completed tasks moved to "Completed This Session"
- [ ] TODO.md new tasks added (if any)
- [ ] TODO.md timestamp updated
- [ ] README.md updated (if major changes)
- [ ] All file paths use correct format (filename:line or filename)
- [ ] All commands tested and verified
- [ ] Emojis used consistently
- [ ] Session marked with clear status (✅ ⚠️ 🔄)
```

---

## 🚫 Common Mistakes to Avoid

1. **Over-documenting**: Don't write essays. Keep it scannable.
2. **Under-documenting**: Don't skip sessions. Even small changes matter.
3. **Inconsistent Formats**: Use the templates provided.
4. **Missing Context**: Explain WHY, not just WHAT.
5. **Stale TODOs**: Remove or archive old completed items.
6. **Wrong Dates**: Use YYYY-MM-DD format consistently.
7. **Missing File References**: Always cite which files changed.

---

## 📊 Quick Reference: Session Types

### Bug Fix Session
```markdown
**Goal**: Fix [specific bug]
**Changes**:
1. **Bug Fix**: [file:line] - Description
**Status**: Bug fixed ✅
```

### Feature Development Session
```markdown
**Goal**: Implement [feature name]
**Changes**:
1. **Feature**: Added [functionality]
2. **Files**: Created/modified [files]
**Status**: Feature complete ✅ / In progress 🔄
```

### Configuration/Setup Session
```markdown
**Goal**: Update [config/setup aspect]
**Changes**:
1. **Config**: Updated [what]
2. **Dependencies**: Added/updated [packages]
**Status**: Working ✅
```

### Learning/Educational Session
```markdown
**Goal**: Learn/teach [concept]
**Educational Sessions**:
- **Topic**: What was learned
**Pending Work**:
- [ ] Apply learnings to codebase
**Status**: Knowledge transferred 🎓
```

---

## 🔍 Review Process

### Weekly Review (Optional but Recommended)

Every 5-7 sessions, review:

1. **HISTORY.md**: Are sessions well documented?
2. **TODO.md**: Remove completed/stale items
3. **README.md**: Does it reflect current state?
4. **Archive**: Consider moving old HISTORY entries to ARCHIVE.md

### Monthly Archive (For Long Projects)

When HISTORY.md gets too long (>20 sessions):

1. Create `HISTORY_ARCHIVE_YYYY.md`
2. Move old sessions (keep last 10-15)
3. Link archive in main HISTORY.md

---

## 💡 Pro Tips

1. **Use Git Commits**: Match doc updates with code commits
2. **Screenshot Important Changes**: Store in `/docs/screenshots/`
3. **Version Documentation**: Tag docs with version numbers
4. **Link Between Docs**: Use relative links `[README](./README.md)`
5. **Keep Templates Handy**: Save session template for quick copy-paste
6. **Document Decisions**: Explain WHY you chose approach X over Y
7. **Future Self**: Write for someone reading this in 6 months

---

## 📚 Additional Resources

- **Markdown Guide**: https://www.markdownguide.org/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Keep a Changelog**: https://keepachangelog.com/

---

## 🎯 Quick Action Commands

**Start New Session:**
```bash
# 1. Check current session number
grep "Session" HISTORY.md | head -1

# 2. Review pending tasks
cat TODO.md | grep "\[ \]" | head -10

# 3. Note what you're working on
```

**End Session:**
```bash
# 1. Add to HISTORY.md (top of file, after header)
# 2. Update TODO.md (mark completed, add new)
# 3. Commit docs
git add HISTORY.md TODO.md README.md
git commit -m "docs: update session X documentation"
```

---

**Last Updated**: 2025-11-05 (Session 8)
**Maintained By**: Development Team
**Review Cycle**: Per session + weekly review
