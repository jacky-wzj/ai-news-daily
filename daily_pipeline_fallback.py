#!/usr/bin/env python3
"""daily_pipeline_fallback.py – Fallback pipeline for AI daily news.

Fixes applied (architect review):
- P0#1: run_step checks returncode, prints stdout/stderr, exits on failure
- P0#2: existing == 0 exits with code 1
- P0#4: date_str regex validation
- P0#5: MIN_SECTIONS threshold
- P1#6: structured logging with timestamps (GMT+8)
- P1#7: .pipeline-done marker to prevent race with main cron
- P1#8: --dry-run mode (skips git push and dingtalk)
- P1#10: empty file detection
- P1#11: proper exit codes
"""

import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

# ─── Constants ───────────────────────────────────────────────────────────────
TZ_GMT8 = timezone(timedelta(hours=8))
MIN_SECTIONS = 3
COMPLETE_SECTIONS = 8  # threshold for "data is already complete and done marker should exist"
SECTIONS = [
    'insights', 'papers', 'xPosts', 'discord', 'github',
    'hn', 'reddit', 'tools', 'agent', 'siliconValley', 'mainlandChina'
]

HOME = os.path.expanduser('~')
WORKSPACE = os.path.join(HOME, '.openclaw', 'workspace', 'ai-news-daily')
PARTS_DIR = os.path.join(WORKSPACE, 'data', 'parts')
DATA_DIR = os.path.join(WORKSPACE, 'data')

# ─── Logging ─────────────────────────────────────────────────────────────────
class GMT8Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=TZ_GMT8)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S GMT+8')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(GMT8Formatter(
    fmt='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S GMT+8'
))
logger = logging.getLogger('fallback_pipeline')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def validate_date(date_str: str) -> str:
    """Validate date string format to prevent path traversal."""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        logger.error(f'Invalid date format: {date_str!r} (expected YYYY-MM-DD)')
        sys.exit(1)
    return date_str


def is_part_ready(section: str, date_str: str) -> bool:
    """Check if a part file exists AND is non-empty."""
    fp = os.path.join(PARTS_DIR, f'{date_str}_{section}.json')
    return os.path.exists(fp) and os.path.getsize(fp) > 0


def run_step(cmd: list, label: str, cwd: str = WORKSPACE, dry_run: bool = False,
             skip_on_dry_run: bool = False):
    """Run a subprocess step with error checking.
    
    Args:
        cmd: Command list
        label: Human-readable step name
        cwd: Working directory
        dry_run: If True and skip_on_dry_run is True, skip execution
        skip_on_dry_run: Whether this step should be skipped in dry-run mode
    """
    if dry_run and skip_on_dry_run:
        logger.info(f'[DRY-RUN] Skipping: {label}')
        return
    
    logger.info(f'Running: {label}')
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        logger.error(f'Step timed out after 300s: {label}')
        sys.exit(1)
    
    if result.stdout.strip():
        for line in result.stdout.strip().split('\n'):
            logger.info(f'  stdout: {line}')
    if result.stderr.strip():
        for line in result.stderr.strip().split('\n'):
            logger.warning(f'  stderr: {line}')
    
    if result.returncode != 0:
        logger.error(f'Step failed: {label} (exit code {result.returncode})')
        sys.exit(1)
    
    logger.info(f'  ✓ {label} succeeded')


def check_completed_today(date_str: str) -> bool:
    """Check if today's pipeline already completed (done marker exists with sufficient content)."""
    done_marker = os.path.join(DATA_DIR, f'.pipeline-done-{date_str}')
    if os.path.exists(done_marker):
        logger.info(f'Pipeline already completed: {done_marker} exists')
        return True
    
    # Also check if data file already has sufficient content
    data_file = os.path.join(DATA_DIR, f'{date_str}.json')
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # dual threshold: check both raw section count AND per-section item count
            populated = sum(1 for s in SECTIONS if data.get(s))
            rich_sections = sum(1 for s in SECTIONS if data.get(s) and len(data.get(s, [])) >= 2)
            if populated >= MIN_SECTIONS or rich_sections >= COMPLETE_SECTIONS:
                logger.info(f'Data file already has {populated} sections ({rich_sections} rich) – pipeline may have run already')
                return True
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    
    return False


def write_done_marker(date_str: str):
    """Write .pipeline-done marker to prevent race conditions."""
    done_marker = os.path.join(DATA_DIR, f'.pipeline-done-{date_str}')
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(done_marker, 'w') as f:
        f.write(datetime.now(TZ_GMT8).isoformat())
    logger.info(f'Written done marker: {done_marker}')


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    # Parse arguments
    dry_run = '--dry-run' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    date_str = args[0] if args else datetime.now(TZ_GMT8).strftime('%Y-%m-%d')
    date_str = validate_date(date_str)

    logger.info(f'=== Fallback Pipeline Start: {date_str} ===')
    if dry_run:
        logger.info('Mode: DRY-RUN (git push and dingtalk will be skipped)')

    # ─── Check if already completed (race condition guard) ───
    if check_completed_today(date_str):
        logger.info('Pipeline already completed today. Exiting gracefully.')
        sys.exit(0)

    # ─── Check available parts ───
    ready_sections = [s for s in SECTIONS if is_part_ready(s, date_str)]
    missing_sections = [s for s in SECTIONS if not is_part_ready(s, date_str)]
    existing = len(ready_sections)

    logger.info(f'Parts found: {existing}/{len(SECTIONS)}')
    if missing_sections:
        logger.warning(f'Missing sections: {", ".join(missing_sections)}')

    if existing == 0:
        logger.error('No parts found, aborting.')
        sys.exit(1)

    if existing < MIN_SECTIONS:
        logger.error(f'Only {existing} sections available, below minimum threshold ({MIN_SECTIONS}). Aborting.')
        sys.exit(1)

    # ─── Run pipeline steps ───
    run_step(
        ['python3', 'wait_and_merge.py', date_str],
        'Merge parts',
        cwd=WORKSPACE
    )

    run_step(
        ['node', 'generate.js', date_str],
        'Generate HTML',
        cwd=WORKSPACE
    )

    run_step(
        ['git', 'add', '-A'],
        'Git add',
        cwd=WORKSPACE
    )

    # Check if there are staged changes before committing (git commit returns non-zero when nothing to commit)
    diff_result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=WORKSPACE, capture_output=True)
    if diff_result.returncode == 0:
        logger.info('No staged changes (already up to date)')
    else:
        run_step(
            ['git', 'commit', '-m', f'Update: {date_str} (fallback)'],
            'Git commit',
            cwd=WORKSPACE
        )
        run_step(
            ['git', 'push', 'origin', 'main'],
            'Git push',
            cwd=WORKSPACE,
            dry_run=dry_run,
            skip_on_dry_run=True
        )

    run_step(
        ['node', 'dingtalk-notify.js',
         f'https://jacky-wzj.github.io/ai-news-daily/{date_str}.html',
         f'{date_str} AI资讯日报'],
        'DingTalk notify',
        cwd=WORKSPACE,
        dry_run=dry_run,
        skip_on_dry_run=True
    )

    # ─── Write done marker ───
    write_done_marker(date_str)

    logger.info(f'=== Fallback Pipeline Complete: {date_str} ===')
    sys.exit(0)


if __name__ == '__main__':
    main()
