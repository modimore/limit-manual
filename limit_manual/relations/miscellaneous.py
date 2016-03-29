from .. import db

class DescriptionFormat(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    format_string = db.Column(db.String(80), nullable=False)
    num_slots = db.Column(db.Integer)

    def __init__(self, format_string,slots=None):
        self.format_string = format_string
        if slots == None:
            self.num_slots = min(format_string.count('{'),format_string.count('}'))
        else:
            self.num_slots = slots

    def __repr__(self):
        return self.format_string

    def __str__(self):
        return self.format_string

class DescriptionFiller(db.Model):
    referent_type = db.Column(db.String(10), primary_key=True)
    referent_id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20))

    def __init__(self,owner_type,owner_id,place,content):
        self.referent_type = owner_type
        self.referent_id = owner_id
        self.place = place
        self.content = content

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content

def get_description(descr_id,referent_type,referent_id):
    format_string = str(DescriptionFormat.query.filter_by(uid=descr_id).one())
    format_fillers = [ str(filler) for filler in DescriptionFiller.query.filter_by(referent_type=referent_type).filter_by(referent_id=referent_id).all() ]

    while len(format_fillers) < format_string.count('{'):
        format_fillers.append('{no filler}')

    return format_string.format(*format_fillers)
