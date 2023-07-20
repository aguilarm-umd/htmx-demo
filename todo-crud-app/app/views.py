from app import app, db
from flask import render_template, request, jsonify
from app.models import Creator, Assignment

@app.route("/", methods=["GET"])
def home():
    assignments = db.session.query(Assignment, Creator).filter(Assignment.creator_id == Creator.creator_id).all()
    return render_template("index.html", assignment=assignments)


@app.route("/submit", methods=["POST"])
def submit():
    global_assignment_object = Assignment()

    assignment_title = request.form["assignment"]
    creator_name = request.form["creator"]

    creator_exists = db.session.query(Creator).filter(Creator.name == creator_name).first()
    print(creator_exists)
    # check if author already exists in db
    if creator_exists:
        creator_id = creator_exists.creator_id
        assignment = Assignment(creator_id=creator_id, assignment=assignment_title)
        db.session.add(assignment)
        db.session.commit()
        global_assignment_object = assignment
    else:
        creator = Creator(name=creator_name)
        db.session.add(creator)
        db.session.commit()

        assignment = Assignment(creator_id=creator.creator_id, assignment=assignment_title)
        db.session.add(assignment)
        db.session.commit()
        global_assignment_object = assignment

    response = f"""
    <tr>
        <td>{assignment_title}</td>
        <td>{creator_name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{global_assignment_object.assignment_id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_assignment_object.assignment_id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_assignment(id):
    assignment = Assignment.query.get(id)
    db.session.delete(assignment)
    db.session.commit()

    return ""


@app.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    assignment = Assignment.query.get(id)
    creator = Creator.query.get(assignment.creator_id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-assignment-row/{id}">
  <td><input name="assignment" value="{assignment.assignment}"/></td>
  <td>{creator.name}</td>
  <td>
    <button class="btn btn-primary" hx-get="/get-assignment-row/{id}">
      Cancel
    </button>
    <button class="btn btn-primary" hx-put="/update/{id}" hx-include="closest tr">
      Save
    </button>
  </td>
    </tr>
    """
    return response

@app.route("/get-assignment-row/<int:id>", methods=["GET"])
def get_assignment_row(id):
    assignment = Assignment.query.get(id)
    creator = Creator.query.get(assignment.creator_id)

    response = f"""
    <tr>
        <td>{assignment.assignment}</td>
        <td>{creator.name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/update/<int:id>", methods=["PUT"])
def update_assignment(id):
    db.session.query(Assignment).filter(Assignment.assignment_id == id).update({"assignment": request.form["assignment"]})
    db.session.commit()

    assignment_title = request.form["assignment"]
    assignment = Assignment.query.get(id)
    creator = Creator.query.get(assignment.creator_id)

    response = f"""
    <tr>
        <td>{assignment_title}</td>
        <td>{creator.name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response
