# 🐛 Known Issues & Bug Tracking

This document tracks known issues, bugs, and items that need to be addressed in the VPS Testing Environment project.

## 🔧 **Active Issues**

### Issue #1: Brace Expansion Bug in Dockerfile
**Status**: Open  
**Priority**: Medium  
**Discovered**: October 25, 2025  

**Description**: 
The Ubuntu Dockerfile contains a brace expansion command that doesn't execute properly, creating a single directory with a literal brace name instead of separate directories.

**Current Behavior**:
```bash
# In container: ls shows:
{projects,deployments,logs,backups}
```

**Expected Behavior**:
```bash
# Should show separate directories:
projects/
deployments/
logs/
backups/
```

**Root Cause**:
Line in `project/distros/ubuntu/Dockerfile`:
```dockerfile
RUN mkdir -p /home/vpsuser/{projects,deployments,logs,backups}
```

**Workaround**:
Users can manually fix this in the container:
```bash
rm -rf "{projects,deployments,logs,backups}"
mkdir -p projects deployments logs backups
```

**Proposed Fix**:
Replace the brace expansion with explicit directory creation:
```dockerfile
RUN mkdir -p /home/vpsuser/projects \
    && mkdir -p /home/vpsuser/deployments \
    && mkdir -p /home/vpsuser/logs \
    && mkdir -p /home/vpsuser/backups
```

**Files Affected**:
- `project/distros/ubuntu/Dockerfile`
- Potentially other distribution Dockerfiles with similar patterns

---

## 📋 **Issue Template**

When adding new issues, use this format:

### Issue #X: [Brief Description]
**Status**: Open/In Progress/Resolved  
**Priority**: Low/Medium/High/Critical  
**Discovered**: [Date]  

**Description**: 
[Detailed description of the issue]

**Current Behavior**:
[What currently happens]

**Expected Behavior**:
[What should happen]

**Root Cause**:
[Technical explanation if known]

**Workaround**:
[Temporary solution if available]

**Proposed Fix**:
[Suggested permanent solution]

**Files Affected**:
- [List of files that need changes]

---

## ✅ **Resolved Issues**

*No resolved issues yet*

---

## 📝 **Notes**

- Issues are numbered sequentially starting from #1
- High priority issues should be addressed before next release
- Include reproduction steps when possible
- Link to relevant GitHub issues if created