from django.contrib.auth import get_user_model
from django.db import transaction
from .models import KeyValue
User = get_user_model()

def assign_supervisor():
    # Round-robin among staff users using KeyValue persistence
    staff = list(User.objects.filter(is_staff=True).order_by('id'))
    if not staff:
        return None
    kv, _ = KeyValue.objects.get_or_create(key='last_supervisor')
    last = kv.value
    # find next supervisor after last
    ids = [str(u.id) for u in staff]
    next_id = None
    if last and last in ids:
        idx = ids.index(last)
        next_id = ids[(idx+1) % len(ids)]
    else:
        next_id = ids[0]
    kv.value = next_id
    kv.save()
    return User.objects.get(id=next_id)
