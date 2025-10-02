# reviews/migrations/0002_create_fts.py
from django.db import migrations

FTS_SQL_STATEMENTS = [
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS reviews_app_fts USING fts5(
      name, category, genres,
      content='reviews_app', content_rowid='id'
    );
    """,
    # populate from existing rows
    """
    INSERT OR REPLACE INTO reviews_app_fts(rowid, name, category, genres)
      SELECT id, name, category, genres FROM reviews_app;
    """,
    # triggers
    """
    CREATE TRIGGER IF NOT EXISTS reviews_app_ai AFTER INSERT ON reviews_app BEGIN
      INSERT INTO reviews_app_fts(rowid, name, category, genres) VALUES (new.id, new.name, new.category, new.genres);
    END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS reviews_app_ad AFTER DELETE ON reviews_app BEGIN
      INSERT INTO reviews_app_fts(reviews_app_fts, rowid, name, category, genres) VALUES('delete', old.id, old.name, old.category, old.genres);
    END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS reviews_app_au AFTER UPDATE ON reviews_app BEGIN
      INSERT INTO reviews_app_fts(reviews_app_fts, rowid, name, category, genres) VALUES('delete', old.id, old.name, old.category, old.genres);
      INSERT INTO reviews_app_fts(rowid, name, category, genres) VALUES (new.id, new.name, new.category, new.genres);
    END;
    """,
]


def create_fts(apps, schema_editor):
    conn_wrapper = schema_editor.connection
    # Only apply on sqlite
    if conn_wrapper.vendor != 'sqlite':
        return

    # Try to get the raw DB-API connection (sqlite3.Connection)
    raw_conn = getattr(conn_wrapper, 'connection', None)

    if raw_conn is not None and hasattr(raw_conn, 'executescript'):
        # raw sqlite connection available: use executescript for multi-statement execution
        script = "\n".join(stmt.strip() for stmt in FTS_SQL_STATEMENTS if stmt and stmt.strip())
        raw_conn.executescript(script)
    else:
        # Fallback: run statements one-by-one through schema_editor.execute()
        for stmt in FTS_SQL_STATEMENTS:
            if stmt and stmt.strip():
                schema_editor.execute(stmt)


class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_fts),
    ]
