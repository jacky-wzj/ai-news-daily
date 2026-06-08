#!/usr/bin/env python3
"""wait_and_merge.py – Wait for all section parts then merge into daily JSON.

Fixes applied (architect review):
- P0#3: safe_read_json with try/except for JSONDecodeError
- P0#4: date_str regex validation
- P0#5: MIN_SECTIONS threshold
- P1#6: structured logging with timestamps (GMT+8)
- P1#9: incremental backoff polling
- P1#10: empty file detection (size == 0 treated as missing)
- P1#11: proper exit codes
"""

import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta

# ─── Constants ───────────────────────────────────────────────────────────────
TZ_GMT8 = timezone(timedelta(hours=8))
MIN_SECTIONS = 3
SECTIONS = [
    'insights', 'papers', 'xPosts', 'discord', 'github',
    'hn', 'reddit', 'tools', 'agent', 'siliconValley', 'mainlandChina'
]
TIMEOUT = 900  # seconds
# Backoff schedule: (elapsed_threshold, interval)
BACKOFF_SCHEDULE = [
    (300, 10),   # 0-5 min: poll every 10s
    (600, 20),   # 5-10 min: poll every 20s
    (900, 30),   # 10-15 min: poll every 30s
]

# ─── Logging ─────────────────────────────────────────────────────────────────
class GMT8Formatter(logging.Formatter):
    converter = None  # unused, override formatTime

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
logger = logging.getLogger('wait_and_merge')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def validate_date(date_str: str) -> str:
    """Validate date string format to prevent path traversal."""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        logger.error(f'Invalid date format: {date_str!r} (expected YYYY-MM-DD)')
        sys.exit(1)
    return date_str


def get_backoff_interval(elapsed: int) -> int:
    """Return polling interval based on elapsed time (incremental backoff)."""
    interval = 10
    for threshold, iv in BACKOFF_SCHEDULE:
        if elapsed < threshold:
            return iv
        interval = iv
    return interval


def part_path(parts_dir: str, date_str: str, section: str) -> str:
    return os.path.join(parts_dir, f'{date_str}_{section}.json')


def is_part_ready(filepath: str) -> bool:
    """Check if a part file exists AND is non-empty."""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0


def safe_read_json(filepath: str, section: str) -> list:
    """Read JSON file safely; return empty list on decode error."""
    try:
        with open(filepath, 'r', encoding='utf-8') as fp:
            part = json.load(fp)
        return part.get('items', [])
    except (json.JSONDecodeError, ValueError, AttributeError) as e:
        logger.warning(f'Corrupt JSON in {section}: {e} – treating as empty')
        return []
    except OSError as e:
        logger.warning(f'Cannot read {section}: {e} – treating as empty')
        return []


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    # Parse and validate date
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    if not date_str:
        date_str = datetime.now(TZ_GMT8).strftime('%Y-%m-%d')
    date_str = validate_date(date_str)

    HOME = os.path.expanduser('~')
    parts_dir = os.path.join(HOME, '.openclaw', 'workspace', 'ai-news-daily', 'data', 'parts')
    data_dir = os.path.join(HOME, '.openclaw', 'workspace', 'ai-news-daily', 'data')

    logger.info(f'Starting wait_and_merge for {date_str}')
    logger.info(f'Parts dir: {parts_dir}')
    logger.info(f'Expecting {len(SECTIONS)} sections, min required: {MIN_SECTIONS}')

    # ─── Polling loop with incremental backoff ───
    waited = 0
    while waited < TIMEOUT:
        missing = [s for s in SECTIONS if not is_part_ready(part_path(parts_dir, date_str, s))]
        if not missing:
            logger.info(f'All {len(SECTIONS)} sections ready after {waited}s')
            break
        interval = get_backoff_interval(waited)
        logger.info(f'Waiting for {len(missing)} sections: {", ".join(missing)} '
                    f'(elapsed {waited}s, next poll in {interval}s)')
        time.sleep(interval)
        waited += interval
    else:
        # Timeout reached
        missing = [s for s in SECTIONS if not is_part_ready(part_path(parts_dir, date_str, s))]
        ready_count = len(SECTIONS) - len(missing)
        logger.warning(f'Timeout after {TIMEOUT}s – {ready_count}/{len(SECTIONS)} sections ready')
        if ready_count < MIN_SECTIONS:
            logger.error(f'Only {ready_count} sections ready, below minimum threshold ({MIN_SECTIONS}). Aborting.')
            sys.exit(1)
        logger.warning(f'Proceeding with {ready_count} sections (above min threshold {MIN_SECTIONS})')

    # ─── Merge ───
    result = {"date": date_str}
    for s in SECTIONS:
        fp = part_path(parts_dir, date_str, s)
        if is_part_ready(fp):
            result[s] = safe_read_json(fp, s)
        else:
            result[s] = []

    # Check threshold even if loop exited normally (some parts may have been corrupt)
    populated = [s for s in SECTIONS if result[s]]
    if len(populated) < MIN_SECTIONS:
        logger.error(f'Only {len(populated)} sections have data after merge '
                     f'(min {MIN_SECTIONS}). Aborting.')
        sys.exit(1)

    # Write output
    os.makedirs(data_dir, exist_ok=True)
    output = os.path.join(data_dir, f'{date_str}.json')
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in result.values() if isinstance(v, list))
    logger.info(f'Merged: {len(populated)}/{len(SECTIONS)} sections, {total} items → {output}')
    sys.exit(0)


if __name__ == '__main__':
    main()
