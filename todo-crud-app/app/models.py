from app import db

class Creator(db.Model):
    creator_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    assignments = db.relationship("Assignment", backref="creator")

    def __repr__(self):
        return '<Creator: {}>'.format(self.assignments)

class Assignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("creator.creator_id"))
    assignment = db.Column(db.String)
