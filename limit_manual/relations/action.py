from .. import db

class Action(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    category = db.Column(db.String(20))

    def __init__(self,name,category):
        self.name = name
        self.category = category

    def __repr__(self):
        return '<\"{1}\"-type action {0}>'.format(self.name,self.category)

class ActionDamage(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('action.uid'),
                          primary_key=True)
    primary = db.Column(db.Boolean, primary_key=True)
    modifier = db.Column(db.Float)
    element = db.Column(db.String(16))
    split = db.Column(db.Boolean)

    def __init__(self,action_id,modifier,element,primary=True,split=True):
        self.action_id = action_id
        self.primary = primary
        self.modifier = modifier
        self.element = element
        self.split = split

    def __repr__(self):
        return '<Action {0} Damage Effect>'.format(self.action_id)

class ActionProperty(db.Model):
    action_id = db.Column(db.Integer, db.ForeignKey('action.uid'),
                          primary_key=True)
    prop_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20))
    value = db.Column(db.String(20))

    def __init__(self,action_id,prop_id,description,value):
        self.action_id = action_id
        self.prop_id = prop_id
        self.description = description
        self.value = value

    def __repr__(self):
        return '<{1} Property of Action {0}: {2}>'.format(self.action_id,self.description,self.value)
