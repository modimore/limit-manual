from .. import get_connection

def get_description(descr_id,referent_type,referent_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''SELECT format_string, num_slots FROM description_formats
                   WHERE uid=%s''', (descr_id,))
    format_string, max_slots = cur.fetchone()

    cur.execute('''SELECT content FROM description_fillers
                   WHERE referent_type=%s AND referent_id=%s
                   ORDER BY place LIMIT %s''',
                   (referent_type,referent_id,max_slots))
    fillers = [ row[0] for row in cur.fetchall() ]
    if len(fillers) < max_slots: fillers.extend(['(not provided)'] * (max_slots-len(fillers)))
    conn.close()

    return format_string.format(*fillers)
