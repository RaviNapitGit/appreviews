from django.db import migrations

FTS_SQL = '''
CREATE VIRTUAL TABLE IF NOT EXISTS reviews_app_fts USING fts5(name, category, genres, content='reviews_app', content_rowid='id');
-- Triggers to update FTS virtual table automatically
CREATE TRIGGER IF NOT EXISTS reviews_app_ai AFTER INSERT ON reviews_app BEGIN
  INSERT INTO reviews_app_fts(rowid, name, category, genres) VALUES (new.id, new.name, new.category, new.genres);
END;
CREATE TRIGGER IF NOT EXISTS reviews_app_ad AFTER DELETE ON reviews_app BEGIN
  INSERT INTO reviews_app_fts(reviews_app_fts, rowid, name, category, genres) VALUES('delete', old.id, old.name, old.category, old.genres);
END;
CREATE TRIGGER IF NOT EXISTS reviews_app_au AFTER UPDATE ON reviews_app BEGIN
  INSERT INTO reviews_app_fts(reviews_app_fts, rowid, name, category, genres) VALUES('delete', old.id, old.name, old.category, old.genres);
  INSERT INTO reviews_app_fts(rowid, name, category, genres) VALUES (new.id, new.name, new.category, new.genres);
END;
'''

def create_fts(apps, schema_editor):
    if schema_editor.connection.vendor == 'sqlite':
        schema_editor.execute(FTS_SQL)

class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_fts),
    ]
