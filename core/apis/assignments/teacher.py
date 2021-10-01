from flask import Blueprint, request

from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of teachers assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    print(teachers_assignments)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grading_assignment(p, incoming_payload):
    """Grading an assignment"""
    print(incoming_payload, p)
    grade_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.update_grade(
        _id=grade_payload.id,
        grade=grade_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_dump)
