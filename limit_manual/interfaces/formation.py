from ..relations import formation as FormationRelations

class Formation(object):
    @staticmethod
    def location_reference(uid):
        return FormationRelations.FormationLocation.query.filter_by(formation_id=uid).all()

    def enemy_reference(uid):
        return FormationRelations.FormationEnemy.query.filter_by(formation_id=uid).all()

    def __init__(self,uid):
        self.uid = uid
        self.locations = []
        self.enemy_rows = {}

        '''
        loc_ref = Formation.location_reference(self.uid)
        for loc in { r.location for r in loc_ref }:
            loc_entries = [ l for l in loc_ref if l.location == loc ]
            areas = [ r.area for r in loc_entries ]
            self.locations.append( { 'location': loc, 'areas': areas } )

        enemy_ref = Formation.enemy_reference(self.uid)
        for row_num in { r.row_num for r in enemy_ref }:
            row_entries = [ { 'name': e.enemy.base.name, 'version': e.enemy.version } for e in enemy_ref if e.row_num == row_num ]
            self.enemy_rows[row_num] = row_entries
        '''

    def __repr__(self):
        return '<Formation {0}>'.format(self.uid)
