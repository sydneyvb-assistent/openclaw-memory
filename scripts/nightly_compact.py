#!/usr/bin/env python3
"""
Nightly Memory Compaction Script
Promotes items from SESSIONS and WORKING to CANON/PROJECTS, deduplicates, commits to git.
Run via: openclaw cron or manually
"""

import os
import sys
import re
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Configuration
WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', '~/.openclaw/workspace')).expanduser()
MEMORY_DIR = WORKSPACE / 'memory'
CANON_DIR = MEMORY_DIR / '10_CANON'
PROJECTS_DIR = MEMORY_DIR / '20_PROJECTS'
SESSIONS_DIR = MEMORY_DIR / '30_SESSIONS'
WORKING_DIR = MEMORY_DIR / '40_WORKING'
ARCHIVE_DIR = MEMORY_DIR / 'archive'

# Memory item types
VALID_TYPES = ['Constraint:', 'Decision:', 'Preference:', 'Task:', 'OpenQuestion:']
REQUIRED_FIELDS_PATTERN = re.compile(
    r'^- (Constraint|Decision|Preference|Task|OpenQuestion): (.+) \[(\d{4}-\d{2}-\d{2})\] \[(global|project:[\w-]+|system:[\w-]+)\]'
)


def log(msg: str):
    """Print with timestamp"""
    print(f"[{datetime.now().isoformat()}] {msg}")


def run_git(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run git command in workspace"""
    return subprocess.run(
        ['git'] + args,
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        check=check
    )


def content_hash(content: str) -> str:
    """Generate normalized hash for deduplication"""
    normalized = ' '.join(content.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def parse_typed_items(file_path: Path) -> List[Dict]:
    """Extract typed memory items from markdown file"""
    items = []
    if not file_path.exists():
        return items
    
    content = file_path.read_text()
    for line in content.split('\n'):
        line = line.strip()
        match = REQUIRED_FIELDS_PATTERN.match(line)
        if match:
            item_type = match.group(1)
            description = match.group(2)
            date = match.group(3)
            scope = match.group(4)
            
            items.append({
                'type': item_type,
                'description': description,
                'date': date,
                'scope': scope,
                'source': str(file_path),
                'hash': content_hash(f"{item_type}:{description}")
            })
    return items


def get_existing_hashes(canon_file: Path) -> set:
    """Get hashes of existing items in canon file"""
    hashes = set()
    if not canon_file.exists():
        return hashes
    
    content = canon_file.read_text()
    for line in content.split('\n'):
        match = REQUIRED_FIELDS_PATTERN.match(line.strip())
        if match:
            item_type = match.group(1)
            description = match.group(2)
            hashes.add(content_hash(f"{item_type}:{description}"))
    return hashes


def append_to_canon(item: Dict) -> bool:
    """Append item to appropriate canon file. Returns True if added, False if duplicate."""
    
    # Determine target file
    if item['type'] == 'Constraint':
        target_file = CANON_DIR / 'constraints.md'
    elif item['type'] == 'Preference':
        target_file = CANON_DIR / 'preferences.md'
    elif item['type'] == 'Decision':
        # Check scope for project-specific decisions
        if item['scope'].startswith('project:'):
            project_name = item['scope'].split(':', 1)[1]
            target_file = PROJECTS_DIR / project_name / 'decision-log.md'
        else:
            target_file = CANON_DIR / 'decisions.md'
    elif item['type'] == 'Task':
        # Tasks go to project backlog or global task file
        if item['scope'].startswith('project:'):
            project_name = item['scope'].split(':', 1)[1]
            target_file = PROJECTS_DIR / project_name / 'task-backlog.md'
        else:
            # Global tasks - for now, skip or add to a global tasks file
            log(f"Skipping global Task (not implemented): {item['description'][:50]}...")
            return False
    elif item['type'] == 'OpenQuestion':
        if item['scope'].startswith('project:'):
            project_name = item['scope'].split(':', 1)[1]
            target_file = PROJECTS_DIR / project_name / 'open-questions.md'
        else:
            # Global open questions - for now, skip
            log(f"Skipping global OpenQuestion (not implemented): {item['description'][:50]}...")
            return False
    else:
        log(f"Unknown item type: {item['type']}")
        return False
    
    # Create parent dirs if needed
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Check for duplicates
    existing_hashes = get_existing_hashes(target_file)
    if item['hash'] in existing_hashes:
        log(f"Duplicate skipped: {item['type']} {item['description'][:50]}...")
        return False
    
    # Check for conflicts (simple: same type, similar description)
    if target_file.exists():
        content = target_file.read_text()
        # If there's a very similar item, mark conflict
        similar_threshold = 0.8  # 80% similarity would need fuzzy matching
    
    # Append item
    line = f"- {item['type']}: {item['description']} [{item['date']}] [{item['scope']}]\n"
    with open(target_file, 'a') as f:
        f.write(line)
    
    log(f"Promoted to {target_file.name}: {item['description'][:60]}...")
    return True


def archive_working_files():
    """Archive or clear WORKING directory files"""
    today = datetime.now().strftime('%Y-%m-%d')
    archive_subdir = ARCHIVE_DIR / 'working' / today
    archive_subdir.mkdir(parents=True, exist_ok=True)
    
    for file_path in WORKING_DIR.glob('*.md'):
        if file_path.name == 'README.md':
            continue
        
        # Check if file has content beyond template
        content = file_path.read_text()
        non_empty = any(
            line.strip() and not line.startswith('#') and not line.startswith('*')
            for line in content.split('\n')
        )
        
        if non_empty:
            # Archive with timestamp
            archive_path = archive_subdir / f"{file_path.stem}-{today}.md"
            archive_path.write_text(content)
            log(f"Archived: {file_path.name} -> {archive_path}")
        
        # Reset to template (preserve structure)
        reset_working_file(file_path)


def reset_working_file(file_path: Path):
    """Reset a working file to empty template"""
    if file_path.name == 'inbox.md':
        content = """# Inbox

Unprocessed inputs, ideas, and raw notes. **Must be emptied by nightly compaction.**

## Rules

1. Dump raw notes here during the day
2. Nightly compaction promotes or archives
3. Never let this file exceed 100 lines
4. Clear after each compaction run

## Current Inbox

*Empty — ready for input*
"""
    elif file_path.name == 'scratch.md':
        content = """# Scratch

Ephemeral notes, temporary working memory. **Must be emptied by nightly compaction.**

## Rules

1. Use for temporary calculations, drafts, working thoughts
2. Do not store durable facts here
3. Cleared after each compaction run

## Current Scratch

*Empty — ready for work*
"""
    else:
        content = f"# {file_path.stem.replace('-', ' ').title()}\n\n*Reset by nightly compaction*\n"
    
    file_path.write_text(content)


def git_commit_changes():
    """Commit changes to git"""
    # Check if there are changes
    status_result = run_git(['status', '--porcelain'], check=False)
    if not status_result.stdout.strip():
        log("No changes to commit")
        return
    
    # Add all memory changes
    run_git(['add', 'memory/'], check=False)
    run_git(['add', 'MEMORY.md'], check=False)
    
    # Commit with timestamp
    today = datetime.now().strftime('%Y-%m-%d')
    commit_msg = f"nightly: compact memory {today}"
    run_git(['commit', '-m', commit_msg], check=False)
    log(f"Committed: {commit_msg}")
    
    # Push if remote configured
    remote_result = run_git(['remote'], check=False)
    if remote_result.stdout.strip():
        push_result = run_git(['push'], check=False)
        if push_result.returncode == 0:
            log("Pushed to remote")
        else:
            log(f"Push failed: {push_result.stderr}")


def reindex_qmd():
    """Reindex QMD if available"""
    qmd_path = subprocess.run(['which', 'qmd'], capture_output=True, text=True)
    if qmd_path.returncode != 0:
        log("QMD not installed, skipping reindex")
        return
    
    log("Reindexing QMD...")
    try:
        # Run qmd update and embed
        subprocess.run(['qmd', 'update'], cwd=WORKSPACE, check=False)
        subprocess.run(['qmd', 'embed'], cwd=WORKSPACE, check=False)
        log("QMD reindex complete")
    except Exception as e:
        log(f"QMD reindex failed: {e}")


def main():
    """Main compaction routine"""
    log("=== Nightly Memory Compaction Started ===")
    
    # 1. Verify workspace
    if not WORKSPACE.exists():
        log(f"ERROR: Workspace not found: {WORKSPACE}")
        sys.exit(1)
    
    # 2. Parse all session files (last 7 days)
    log("Parsing session files...")
    all_items = []
    cutoff_date = datetime.now().timestamp() - (7 * 24 * 60 * 60)
    
    for session_file in sorted(SESSIONS_DIR.glob('*.md')):
        # Check file mtime
        try:
            mtime = session_file.stat().st_mtime
            if mtime < cutoff_date:
                continue
        except:
            pass
        
        items = parse_typed_items(session_file)
        all_items.extend(items)
        log(f"  {session_file.name}: {len(items)} items")
    
    log(f"Total items to process: {len(all_items)}")
    
    # 3. Promote items to canon
    log("Promoting items to canon...")
    promoted = 0
    duplicates = 0
    
    for item in all_items:
        if append_to_canon(item):
            promoted += 1
        else:
            duplicates += 1
    
    log(f"Promoted: {promoted}, Duplicates: {duplicates}")
    
    # 4. Archive/clear WORKING
    log("Archiving WORKING files...")
    archive_working_files()
    
    # 5. Git commit
    log("Committing changes...")
    git_commit_changes()
    
    # 6. QMD reindex (optional)
    reindex_qmd()
    
    log("=== Nightly Memory Compaction Complete ===")


if __name__ == '__main__':
    main()
