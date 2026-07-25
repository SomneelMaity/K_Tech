"""
Script to validate knowledge base entries
"""
import json
import sys
from pathlib import Path
from datetime import datetime
import argparse


def validate_entry(entry: dict, line_num: int) -> list[str]:
    """Validate a single KB entry"""
    errors = []
    
    # Required fields
    if 'content' not in entry:
        errors.append(f"Line {line_num}: Missing 'content' field")
    elif not entry['content'].strip():
        errors.append(f"Line {line_num}: Empty 'content' field")
    
    if 'metadata' not in entry:
        errors.append(f"Line {line_num}: Missing 'metadata' field")
        return errors
    
    metadata = entry['metadata']
    
    # Required metadata fields
    required_meta = ['act', 'topic', 'last_verified', 'language']
    for field in required_meta:
        if field not in metadata:
            errors.append(f"Line {line_num}: Missing metadata.{field}")
    
    # Validate date format
    if 'last_verified' in metadata:
        try:
            date = datetime.fromisoformat(metadata['last_verified'])
            # Warn if older than 6 months
            age = (datetime.now() - date).days
            if age > 180:
                errors.append(f"Line {line_num}: WARNING - Entry is {age} days old (re-verification needed)")
        except:
            errors.append(f"Line {line_num}: Invalid date format in 'last_verified'")
    
    # Language should be valid
    valid_languages = ['en', 'hi', 'bn', 'te', 'mr', 'ta', 'gu', 'kn', 'ml', 'or', 'pa']
    if metadata.get('language') not in valid_languages:
        errors.append(f"Line {line_num}: Invalid language code '{metadata.get('language')}'")
    
    return errors


def validate_segment(segment_path: Path) -> tuple[int, list[str]]:
    """Validate all entries in a segment"""
    entries_file = segment_path / "entries.jsonl"
    
    if not entries_file.exists():
        return 0, [f"No entries.jsonl file found in {segment_path}"]
    
    errors = []
    count = 0
    
    with open(entries_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                entry = json.loads(line)
                count += 1
                errors.extend(validate_entry(entry, line_num))
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: Invalid JSON - {e}")
    
    if count < 60:
        errors.append(f"WARNING: Only {count} entries found. Minimum 60 required for submission.")
    
    return count, errors


def main():
    parser = argparse.ArgumentParser(description='Validate knowledge base entries')
    parser.add_argument('--segment', help='Segment ID (e.g., s1-consumer)', default=None)
    args = parser.parse_args()
    
    kb_root = Path(__file__).parent.parent / "knowledge-base"
    
    if args.segment:
        segments = [args.segment]
    else:
        # Validate all segments
        segments = [d.name for d in kb_root.iterdir() if d.is_dir() and d.name.startswith('s')]
    
    total_count = 0
    total_errors = 0
    
    for segment in segments:
        segment_path = kb_root / segment
        if not segment_path.exists():
            print(f"❌ Segment not found: {segment}")
            continue
        
        print(f"\n📁 Validating {segment}...")
        count, errors = validate_segment(segment_path)
        
        total_count += count
        
        if errors:
            total_errors += len(errors)
            print(f"  ⚠️  {count} entries, {len(errors)} issues:")
            for error in errors[:10]:  # Show first 10
                print(f"    - {error}")
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more")
        else:
            print(f"  ✅ {count} entries validated successfully")
    
    print(f"\n{'='*60}")
    print(f"Total entries: {total_count}")
    print(f"Total issues: {total_errors}")
    
    if total_errors > 0:
        print("❌ Validation failed")
        sys.exit(1)
    else:
        print("✅ All validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
