from django.db import connection
from django.conf import settings
from .models import App
import math

def suggest_apps(q, limit=8):
    q = q.strip()
    if len(q) < 3:
        return []
    # Use simple icontains fallback; if SQLite FTS5 present, use it
    cursor = connection.cursor()
    vendor = connection.vendor
    if vendor == 'sqlite':
        try:
            # FTS5 virtual table named reviews_app_fts created by migration
            sql = "SELECT rowid, name FROM reviews_app_fts WHERE reviews_app_fts MATCH ? LIMIT ?"
            args = (q+'*', limit)
            cursor.execute(sql, args)
            return [{'id': r[0], 'name': r[1]} for r in cursor.fetchall()]
        except Exception:
            pass
    qs = App.objects.filter(name__icontains=q)[:limit]
    return [{'id': a.id, 'name': a.name} for a in qs]

def full_search(q, limit=50):
    q = q.strip()
    vendor = connection.vendor
    results = []
    if len(q) < 1:
        return App.objects.all().order_by('-installs')[:limit]
    if vendor == 'sqlite':
        try:
            cursor = connection.cursor()
            # compute fts rank using bm25 if available or simple match
            sql = '''
                SELECT a.rowid, a.name, bm25(reviews_app_fts) as score, apps.installs
                FROM reviews_app_fts a
                JOIN reviews_app apps ON apps.id = a.rowid
                WHERE reviews_app_fts MATCH ?
                LIMIT ?
            '''
            cursor.execute(sql, (q+'*', limit))
            rows = cursor.fetchall()
            ids_scores = []
            for row in rows:
                rowid, name, score, installs = row
                # lower bm25 = better, so invert
                if score is None:
                    fscore = 1.0
                else:
                    fscore = 1.0/(score+0.001)
                norm_inst = math.log(installs+1)
                rank = 0.7 * fscore + 0.3 * (norm_inst / (1 + norm_inst))
                ids_scores.append((rowid, rank))
            ids = [r[0] for r in ids_scores]
            preserved = 'CASE ' + ' '.join([f'WHEN id={i} THEN {idx}' for idx,i in enumerate(ids)]) + ' END'
            qs = App.objects.filter(id__in=ids).order_by('-installs')  # fallback
            return qs
        except Exception:
            pass
    # fallback icontains
    return App.objects.filter(name__icontains=q)[:limit]
