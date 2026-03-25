import platform
import shutil

_tesseract_which = shutil.which('tesseract')
if _tesseract_which:
    DEFAULT_TESSERACT_BINARY_PATH = _tesseract_which
elif platform.system() in ('FreeBSD', 'OpenBSD', 'Darwin'):
    DEFAULT_TESSERACT_BINARY_PATH = '/usr/local/bin/tesseract'
else:
    DEFAULT_TESSERACT_BINARY_PATH = '/usr/bin/tesseract'

DEFAULT_TESSERACT_TIMEOUT = 600  # 600 seconds, 10 minutes
