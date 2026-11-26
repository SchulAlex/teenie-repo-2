from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False, default='Anonymous')
<<<<<<< HEAD
    image_filename = db.Column(db.String(200), nullable=True)
=======
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
<<<<<<< HEAD
    image_filename = db.Column(db.String(200), nullable=True)
=======
>>>>>>> 2e30b332e272c2b4ba395f0b61e71434b00f2dfb
    options = db.relationship('PollOption', backref='poll', lazy=True,
                              cascade='all, delete-orphan')


class PollOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(100), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    votes = db.relationship('PollVote', backref='option', lazy=True,
                            cascade='all, delete-orphan')


class PollVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_option.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
