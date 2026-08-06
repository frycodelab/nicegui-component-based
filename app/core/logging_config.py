"""Central application logging: daily rolling file handler plus console, runtime-adjustable level.

A new log file is started every day at midnight in logs/; rotated files are
suffixed with their date (app.log.2026-08-06). The active level is persisted so
it survives restarts and can be changed live from the admin settings page.
"""

import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / 'logs'
LOG_FILE = LOG_DIR / 'app.log'
_LEVEL_FILE = LOG_DIR / '.log_level'

# Selectable levels, ordered from most to least verbose.
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
_DEFAULT_LEVEL = 'INFO'

_BACKUP_COUNT = 0            # 0 = keep every daily log file forever

_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'

logger = logging.getLogger(__name__)


def _read_persisted_level() -> str:
    try:
        level = _LEVEL_FILE.read_text(encoding='utf-8').strip().upper()
        if level in LOG_LEVELS:
            return level
    except OSError:
        pass
    return _DEFAULT_LEVEL


def setup_logging() -> None:
    """Configure root logging with a rolling file handler and a console handler.

    Idempotent: safe to call more than once (e.g. under the dev auto-reloader)
    without stacking duplicate handlers.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(_read_persisted_level())

    # Silence the dev auto-reloader's change logs: writing them into logs/app.log
    # is itself a file change, which retriggers the watcher in an endless loop.
    logging.getLogger('watchfiles').setLevel(logging.WARNING)

    if any(getattr(h, '_app_handler', False) for h in root.handlers):
        return

    formatter = logging.Formatter(_FORMAT)

    # Rolls over at midnight; rotated files get a .YYYY-MM-DD suffix.
    file_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_FILE, when='midnight', interval=1, backupCount=_BACKUP_COUNT, encoding='utf-8'
    )
    file_handler.suffix = '%Y-%m-%d'
    file_handler.setFormatter(formatter)
    file_handler._app_handler = True

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console._app_handler = True

    root.addHandler(file_handler)
    root.addHandler(console)
    logger.info('Logging initialised — level=%s, file=%s', get_log_level(), LOG_FILE)


def get_log_level() -> str:
    """Return the current root log level name (e.g. ``'INFO'``)."""
    return logging.getLevelName(logging.getLogger().level)


def set_log_level(level: str) -> bool:
    """Set and persist the root log level. Returns ``True`` when applied."""
    level = level.upper()
    if level not in LOG_LEVELS:
        return False
    logging.getLogger().setLevel(level)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        _LEVEL_FILE.write_text(level, encoding='utf-8')
    except OSError:
        logger.warning('Could not persist log level to %s', _LEVEL_FILE)
    logger.info('Log level changed to %s', level)
    return True
