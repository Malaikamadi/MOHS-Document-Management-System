#!/usr/bin/env python3
"""Print MoHS directorates and document types (no Django required)."""
from __future__ import print_function

import os
import sys

# Repo root: .../mayan-edms-official
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from mayan.apps.mohs.literals import (  # noqa: E402
    MOHS_DIRECTORATES,
    mohs_record_types_for,
)


def main():
    print('MoHS bootstrap plan (mayan.apps.mohs)\n')
    total = 0
    for code, cabinet, full in MOHS_DIRECTORATES:
        types_ = mohs_record_types_for(code)
        total += len(types_)
        print('[%s] %s' % (code, cabinet))
        print('    Full name: %s' % full)
        print('    Group: MoHS_%s  |  Role: MoHS %s Staff' % (code, code))
        print('    Document types (%s):' % len(types_))
        for t in types_:
            label = '%s – %s' % (code, t)
            ok = len(label) <= 96
            print('      - %s [%s chars]%s' % (t, len(label), '' if ok else ' !! >96'))
        print()
    print('Total document types: %s' % total)
    print('Cabinets: %s root cabinets (one per directorate)' % len(MOHS_DIRECTORATES))


if __name__ == '__main__':
    main()
