from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify

from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from app import database
from app.models.user import User
from app.models.story import Story

from app.util import parse

database.init_db()
session = database.db_session

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return "hello home!"

@app.route("/users", methods=["GET", "POST"])
def get_users():
    if request.form:
        print("in form indent")
        username = request.form.get("username")
        user_type = request.form.get("user_type")
        user = User(username=username, user_type=user_type)
        session.add(user)
        session.commit()
    users = User.query.all()
    print(users)
    return render_template("users.html", users=users)

@app.route("/stories", methods=["GET", "POST"])
def get_stories():

    print("REQUEST ARGS")
    print(request.args)

    if request.method == "POST":
        req_data = request.get_json()

        summary = req_data["summary"]
        description = req_data["description"]
        story_type = req_data["story_type"]
        complexity = req_data["complexity"]
        estimated_time = req_data["estimated_time"]
        cost = float(req_data["cost"])
        # created_at = Column(TIMESTAMP)
        created_by = request.args['user']
        status = "DRAFT"
        # last_updated_at = Column(TIMESTAMP)
        # last_updated_by = Column(String)

        story = Story(summary=summary, description=description, story_type=story_type,
                      complexity=complexity, estimated_time=estimated_time, cost=cost,
                      created_by=created_by,status=status)
        session.add(story)
        session.commit()
        story_id = story.id
        return jsonify("story with id %s created."% (story_id))
    elif request.method == "GET":
        #TODO handle scenario where username is not present in users table
        user = User.query.filter(User.username == request.args['user']).first()
        if user.user_type == 'admin':
            stories = Story.query.all()
        else:
            stories = Story.query.filter(Story.created_by == request.args['user'])
        res = []
        for story in stories:
            res.append(story.to_dict())
        return jsonify(res)

@app.route("/stories/<int:id>")
def get_story(id):
    # TODO handle scenario where username is not present in users table

    if 'user' not in request.args:
        return jsonify({'error': 'username required'})
    username_q = request.args['user']
    user = User.query.filter(User.username == username_q).first()
    story = Story.query.get(id)
    if story.created_by == user.username or user.user_type == 'admin':
        return jsonify(story.to_dict_full())
    else:
        return jsonify({'error': 'Unauthorised access'})

#TODO allow update only of specific properties
#TODO allow updates based on user
@app.route("/stories/<int:id>", methods=["PUT"])
def update_story(id):
    user = User.query.filter(User.username == request.args['user']).first()
    story = Story.query.get(id)

    if story.created_by == user.username or user.user_type == 'admin':
        #TODO validate data for updating
        req_data = request.get_json()
        for key in req_data:
            setattr(story, key, req_data[key])
        session.commit()
        return jsonify("story with id %s updated"% (id) )
    else:
        return jsonify({'error': 'Unauthorised access'})

@app.route("/stories/<int:id>/submit", methods=["PUT"])
def submit_story_for_approval(id):
    user = User.query.filter(User.username == request.args['user']).first()
    story = Story.query.get(id)
    if story.created_by == user.username:
        story.status = "FOR REVIEW"
        session.commit()
        return jsonify({"success": "story with id %s submitted for admin approval" % id})
    else:
        return jsonify({"error": "unauthorised access"})

@app.route("/stories/<int:id>/approve", methods=["PUT"])
def approve_story(id):
    user = User.query.filter(User.username == request.args['user']).first()
    if user.user_type=='admin':
        story = Story.query.get(id)
        if story.status == "FOR REVIEW":
            story.status = "APPROVED"
            session.commit()
            return jsonify({"success": "story with id %s approved!" % id})
        else:
            return jsonify({"error": "story id %s in %s state cannot be approved" % (
                id, story.status)})
    else:
        return jsonify({"error": "unauthorised access"})

@app.route("/stories/<int:id>/reject", methods=["PUT"])
def reject_story(id):
    user = User.query.filter(User.username == request.args['user']).first()
    if user.user_type=='admin':
        story = Story.query.get(id)
        if story.status == "FOR REVIEW":
            story.status = "REJECTED"
            session.commit()
            return jsonify({"success": "story with id %s rejected!" % id})
        else:
            return jsonify({"error": "story id %s in %s state cannot be rejected" % (
                id, story.status)})
    else:
        return jsonify({"error": "unauthorised access"})

if __name__ == "__main__":
    app.run(debug=True)

