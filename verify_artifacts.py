#!/usr/bin/env python3
"""Verify the immutable release archives, not the mathematical claims."""
import hashlib
import shutil
from tempfile import NamedTemporaryFile
from pathlib import Path, PurePosixPath
import zipfile

root = Path(__file__).resolve().parent
for line in (root / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
    digest, name = line.split('  ', 1)
    path = root / name
    if not path.exists() and path.name == 'regular-polygons-49-58-and-local-arc-certificates.zip':
        parts = [Path(str(path) + f'.part{i:02d}') for i in range(2)]
        if not all(part.is_file() for part in parts):
            raise SystemExit(f'Missing one or more archive parts: {name}')
        with NamedTemporaryFile(dir=path.parent, delete=False) as temp:
            pending = Path(temp.name)
            try:
                for part in parts:
                    with part.open('rb') as stream:
                        shutil.copyfileobj(stream, temp)
                temp.flush()
                combined = hashlib.sha256()
                with pending.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        combined.update(block)
                if combined.hexdigest() != digest:
                    raise SystemExit(f'Reconstructed SHA-256 mismatch: {name}')
                pending.replace(path)
            finally:
                pending.unlink(missing_ok=True)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    if h.hexdigest() != digest:
        raise SystemExit(f'SHA-256 mismatch: {name}')
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            parts = PurePosixPath(member.filename)
            if parts.is_absolute() or '..' in parts.parts or '\\' in member.filename:
                raise SystemExit(f'Unsafe archive path: {member.filename}')
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise SystemExit(f'Unexpected symbolic link: {member.filename}')
        bad = archive.testzip()
        if bad is not None:
            raise SystemExit(f'ZIP CRC mismatch: {bad}')
        print(f'OK {name}: {path.stat().st_size} bytes, {len(archive.infolist())} entries')
print('Archive integrity verified. Mathematical replay must be run separately.')
