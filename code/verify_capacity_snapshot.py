#!/usr/bin/env python3
"""Verify the frozen 2026-11-27 22:00 archive and its embedded ZIP history.

This checks bytes, not mathematical completeness or correctness.
"""
import argparse
import hashlib
import io
import re
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

EXPECTED = '3e6509df4b450d6bda4547d58315da9612fe392343c78344e9ff9909c917183a'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(data, name, seen):
    digest = sha(data)
    if digest in seen:
        return
    seen.add(digest)
    with ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(set(names)) != len(names):
            raise ValueError(f'{name}: duplicate member names')
        for member in names:
            p = PurePosixPath(member)
            if p.is_absolute() or '..' in p.parts or '\\' in member:
                raise ValueError(f'{name}: unsafe member {member}')
        bad = archive.testzip()
        if bad is not None:
            raise ValueError(f'{name}: CRC failure in {bad}')
        count = 0
        if 'SHA256SUMS.txt' in names:
            covered = set()
            for line in archive.read('SHA256SUMS.txt').decode('utf-8').splitlines():
                if not line.strip():
                    continue
                expected, member = line.split(maxsplit=1)
                member = member.lstrip('*').removeprefix('./')
                if not re.fullmatch('[0-9a-fA-F]{64}', expected):
                    raise ValueError(f'{name}: invalid SHA-256 entry')
                if member in covered or member not in names:
                    raise ValueError(f'{name}: invalid manifest member {member}')
                if sha(archive.read(member)) != expected.lower():
                    raise ValueError(f'{name}: SHA-256 mismatch in {member}')
                covered.add(member)
                count += 1
            missing = {n for n in names if not n.endswith('/')} - covered - {'SHA256SUMS.txt'}
            if missing:
                raise ValueError(f'{name}: uncovered members: {sorted(missing)}')
            print(f'{name}: {count} manifest entries verified')
        else:
            print(f'{name}: CRC verified; no root SHA256SUMS.txt')
        for member in names:
            if member.endswith('.zip'):
                verify(archive.read(member), member.rsplit('/', 1)[-1], seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    data = args.archive.read_bytes()
    if sha(data) != EXPECTED:
        raise SystemExit('The outer archive does not match the frozen 22:00 SHA-256.')
    seen = set()
    verify(data, args.archive.name, seen)
    print(f'PASS: {len(seen)} distinct ZIPs checked; no mathematical verification claimed.')


if __name__ == '__main__':
    main()
