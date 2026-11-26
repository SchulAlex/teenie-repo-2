import uuid

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from .forms import PollForm, StoryForm
from .models import Poll, PollOption, PollVote, Story, db

main = Blueprint('main', __name__)


def _current_user_id():
    """Anonymous, session-based id (used to prevent double voting)."""
    if 'uid' not in session:
        session['uid'] = uuid.uuid4().hex
    return session['uid']


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/Other Projects')
def other_projects():
    return render_template('other_projects.html')


@main.route('/stories')
def stories():
    all_stories = Story.query.order_by(Story.id.desc()).all()
    return render_template('stories.html', stories=all_stories)


@main.route('/story/new', methods=['GET', 'POST'])
def new_story():
    form = StoryForm()
    if form.validate_on_submit():
        story = Story(
            title=form.title.data,
            content=form.content.data,
            author=(form.author.data or '').strip() or 'Anonymous',
        )
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('main.stories'))
    return render_template('new_story.html', form=form)


@main.route('/polls', methods=['GET', 'POST'])
def polls():
    form = PollForm()
    if form.validate_on_submit():
        poll = Poll(question=form.question.data)
        for text in form.parsed_options(form.options.data):
            poll.options.append(PollOption(option_text=text))
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('main.poll_detail', poll_id=poll.id))
    all_polls = Poll.query.order_by(Poll.id.desc()).all()
    return render_template('polls.html', form=form, polls=all_polls)


@main.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def poll_detail(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    user_id = _current_user_id()

    if request.method == 'POST':
        option_id = request.form.get('option', type=int)
        option = PollOption.query.filter_by(id=option_id, poll_id=poll.id).first() \
            if option_id is not None else None
        already_voted = (
            PollVote.query.join(PollOption)
            .filter(PollOption.poll_id == poll.id, PollVote.user_id == user_id)
            .first()
        )
        if option is None:
            flash('Please select a valid option.', 'error')
        elif already_voted:
            flash('You have already voted in this poll.', 'error')
        else:
            db.session.add(PollVote(option_id=option.id, user_id=user_id))
            db.session.commit()
            flash('Thank you for your vote!', 'success')
        return redirect(url_for('main.poll_detail', poll_id=poll.id))

    total_votes = sum(len(o.votes) for o in poll.options)
    return render_template('poll_detail.html', poll=poll, total_votes=total_votes)


@main.route('/quiz')
def quiz():
    return render_template('quiz.html')
