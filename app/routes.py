import os
import uuid

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from werkzeug.utils import secure_filename

from .forms import PollForm, StoryForm
from .models import Poll, PollOption, PollVote, Story, db

main = Blueprint('main', __name__)

# Magic bytes of the allowed image formats (so a renamed .exe is rejected)
_SIGNATURES = (b'\xff\xd8\xff', b'\x89PNG\r\n\x1a\n', b'GIF87a', b'GIF89a')


def _looks_like_image(header):
    if header.startswith(_SIGNATURES):
        return True
    return header[:4] == b'RIFF' and header[8:12] == b'WEBP'


def save_upload(file_storage):
    """Validate and store an uploaded image.

    Returns (filename, error). Both are None if nothing was uploaded.
    """
    if not file_storage or not file_storage.filename:
        return None, None
    header = file_storage.stream.read(16)
    file_storage.stream.seek(0)
    if not _looks_like_image(header):
        return None, 'The file is not a valid image.'
    ext = secure_filename(file_storage.filename).rsplit('.', 1)[-1].lower()
    filename = f'{uuid.uuid4().hex}.{ext}'
    file_storage.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return filename, None


@main.app_errorhandler(413)
def file_too_large(_error):
    flash('The file is too large (max. 5 MB).', 'error')
    return redirect(request.referrer or url_for('main.index'))


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
        filename, error = save_upload(form.image.data)
        if error:
            form.image.errors.append(error)
            return render_template('new_story.html', form=form)
        story = Story(
            title=form.title.data,
            content=form.content.data,
            author=(form.author.data or '').strip() or 'Anonymous',
            image_filename=filename,
        )
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('main.stories'))
    return render_template('new_story.html', form=form)


@main.route('/polls', methods=['GET', 'POST'])
def polls():
    form = PollForm()
    if form.validate_on_submit():
        filename, error = save_upload(form.image.data)
        if error:
            form.image.errors.append(error)
            all_polls = Poll.query.order_by(Poll.id.desc()).all()
            return render_template('polls.html', form=form, polls=all_polls)
        poll = Poll(question=form.question.data, image_filename=filename)
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
