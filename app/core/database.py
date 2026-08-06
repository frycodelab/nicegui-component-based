"""SQLite database access via SQLAlchemy: engine, ORM models and sessions.

The database file lives next to the application code so the demo is
self-contained. A default admin account (admin/admin) is seeded on the first
run; change its password from the Users page afterwards.
"""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from sqlalchemy import String, create_engine, event, inspect, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / 'data' / 'app.db'
BACKUP_DIR = Path(__file__).parent.parent / 'backup'

_DEFAULT_ADMIN_USERNAME = 'admin'
_DEFAULT_ADMIN_PASSWORD = 'admin'


class Base(DeclarativeBase):
    pass


class UserRecord(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, server_default='user')
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=text('1'))
    must_change_password: Mapped[bool] = mapped_column(nullable=False, server_default=text('1'))
    email: Mapped[str | None] = mapped_column(String)
    display_name: Mapped[str | None] = mapped_column(String)
    avatar: Mapped[str | None] = mapped_column(String)
    language: Mapped[str] = mapped_column(String, nullable=False, server_default='en')
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, server_default=text("(datetime('now'))")
    )


class AuditLogRecord(Base):
    """One recorded action in the audit trail (who did what, when)."""

    __tablename__ = 'audit_log'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[str] = mapped_column(
        String, nullable=False, index=True, server_default=text("(datetime('now'))")
    )
    action: Mapped[str] = mapped_column(String, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int | None] = mapped_column()
    target: Mapped[str | None] = mapped_column(String)
    details: Mapped[str | None] = mapped_column(String)
    ip: Mapped[str | None] = mapped_column(String)



_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None
_engine_path: str | None = None


@event.listens_for(Engine, 'connect')
def _set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA journal_mode = WAL')     # concurrent readers during a write
    cursor.execute('PRAGMA synchronous = NORMAL')   # safe, fast companion to WAL
    cursor.execute('PRAGMA busy_timeout = 5000')    # wait instead of failing on a lock
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.close()


def _get_session_factory() -> sessionmaker[Session]:
    """Return the session factory, rebuilding the engine if DB_PATH changed.

    Rebuilding on a changed path keeps the test suite working, where DB_PATH is
    monkeypatched to a temporary file before init_db().
    """
    global _engine, _session_factory, _engine_path
    if _session_factory is None or _engine_path != str(DB_PATH):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            f'sqlite:///{DB_PATH}', connect_args={'timeout': 5.0}, future=True
        )
        _session_factory = sessionmaker(bind=_engine, future=True)
        _engine_path = str(DB_PATH)
    return _session_factory


@contextmanager
def get_session() -> Iterator[Session]:
    """Yield a SQLAlchemy session, committed on success and rolled back on error.

    A single with get_session() block is one atomic unit of work.
    """
    session = _get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _migrate(engine: Engine) -> None:
    """Additively add any columns missing from databases created by older versions."""
    inspector = inspect(engine)
    if not inspector.has_table('users'):
        return
    existing = {col['name'] for col in inspector.get_columns('users')}
    additions = {
        'is_active': 'INTEGER NOT NULL DEFAULT 1',
        'must_change_password': 'INTEGER NOT NULL DEFAULT 1',
        'email': 'TEXT',
        'display_name': 'TEXT',
        'avatar': 'TEXT',
        'language': "TEXT NOT NULL DEFAULT 'en'",
    }
    missing = {name: ddl for name, ddl in additions.items() if name not in existing}
    if not missing:
        return
    with engine.begin() as conn:
        for name, ddl in missing.items():
            conn.execute(text(f'ALTER TABLE users ADD COLUMN {name} {ddl}'))


def init_db() -> None:
    """Create the schema if missing, migrate older databases and seed admin."""
    from models.enums import UserRole
    from services.user_service import UserService

    engine = _get_session_factory().kw['bind']
    Base.metadata.create_all(engine)
    _migrate(engine)

    with get_session() as session:
        if session.query(UserRecord).count() == 0:
            # must_change_password=True forces the first admin login to set a real password
            UserService(session).create_user(
                _DEFAULT_ADMIN_USERNAME,
                role=UserRole.ADMIN,
                password=_DEFAULT_ADMIN_PASSWORD,
            )
            logger.info('Seeded default admin account (admin/admin); change the password.')


def backup_database(*, label: str | None = None) -> Path:
    """Write a consistent online backup of the database to the backup/ folder.

    Uses SQLite's backup API, which produces a safe snapshot while the app is
    live, including under WAL. Returns the path of the written file.
    """
    _get_session_factory()  # ensure the data directory and database file exist
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    suffix = f'-{label}' if label else ''
    destination = BACKUP_DIR / f'app-{stamp}{suffix}.db'

    source = sqlite3.connect(DB_PATH)
    try:
        target = sqlite3.connect(destination)
        try:
            source.backup(target)
        finally:
            target.close()
    finally:
        source.close()
    logger.info('Database backed up to %s', destination)
    return destination


def reset_admin_to_default() -> Path:
    """Restore the default admin account (admin/admin, forced password change).

    Takes a safety backup first, then resets the admin to an active admin with the
    default password, recreating it if it was deleted. Returns the backup path.
    """
    from core.security import hash_password
    from models.enums import UserRole
    from services.user_service import UserService

    backup_path = backup_database(label='pre-admin-reset')
    with get_session() as session:
        record = session.scalar(
            select(UserRecord).where(UserRecord.username == _DEFAULT_ADMIN_USERNAME)
        )
        if record is None:
            UserService(session).create_user(
                _DEFAULT_ADMIN_USERNAME,
                role=UserRole.ADMIN,
                password=_DEFAULT_ADMIN_PASSWORD,
            )
        else:
            record.role = UserRole.ADMIN.value
            record.is_active = True
            record.password_hash = hash_password(_DEFAULT_ADMIN_PASSWORD)
            record.must_change_password = True
    logger.warning('Admin account reset to default credentials (admin/admin).')
    return backup_path
