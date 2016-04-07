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

def add_description(action_type,action_id,format='',fillers=[]):
    descrs = DescriptionFormat.query.filter_by(format_string=format).all()
    if len(descrs) == 0:
        descr = DescriptionFormat(format,len(fillers))
        db.session.add(descr)
        descr_id = descr.uid
        db.session.commit()
    else: descr_id = descrs[0].uid

    for i in range(len(fillers)):
        db.session.add(DescriptionFiller(action_type,action_id,i,fillers[i]))
    db.session.commit()

    return descr_id
