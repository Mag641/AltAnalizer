def get_org_events_datetimes(history):
    for obj in history:
        for key in obj.copy():
            if key not in ['type', 'created_at']:
                obj.pop(key)
    return history
