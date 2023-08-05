# -*- coding: utf-8 -*-
# Tests of pymongo interface

from datetime import datetime

from bson import ObjectId
from objdict import Struct

from .view_models import Student, StudentWithNameFieldWithAlias
from viewmodel import BaseView, DBMongoSource, IdField, IntField, JournalView, TxtField, ViewRow
from viewmodel.viewFields import viewModelDB

database = viewModelDB.baseDB.db


class StudentXX(BaseView):
    models_ = database.Students
    id = IdField(cases={})  # , name = '_id')
    name = TxtField()
    course = TxtField(value='engineering')
    course_year = IntField()


class TestStudentsTutorial:
    def test_init_db_tutversion(self):
        name = "Fred Smith"
        student = Student(models=viewModelDB.default('Student2s'))
        assert len(student) == 0
        student.insert_()
        assert student._dbRows[0]['Student2s'] == {}

        with student:
            student.name = name
        assert student.name == name
        assert student.course == 'engineering'
        assert '_id' in student._dbRows[0]['Student2s']

    def test_init_db(self):
        student = Student()
        name = "Fred Smith"
        assert len(student) == 0
        student.insert_()
        with student:
            student.name = name
        assert student.name == name

    def test_read_student_and_modify(self):
        student = Student({})
        assert len(student) == 1
        assert student.course_year is None
        assert student.course == 'engineering'

        with student:
            student.course_year = 2
            student.course = 'Computing'

    def test_add_second_student(self):
        student = Student()
        assert len(student) == 0
        student.insert_()
        with student:
            student.name = 'Jane'
            student.course_year = 3
            student.course = 'Computer Engineering'

    def test_read_all_students(self):
        students = Student({})
        assert len(students) == 2
        student = students[1]
        assert student.course_year == 3
        with student:
            student.course_year = 2

    def test_read_multiple_by_find_dictionary(self):
        students = Student({'course_year': 2})
        assert len(students) == 2
        student = students[1]
        assert student.course_year == 2
        for student in students:
            assert student.course_year == 2

    def test_delete_method(self):
        # Prepare
        test_data = Student({})
        original_size = len(test_data)
        to_delete = test_data[0]
        id_to_delete = test_data[0]['id'].value

        # Delete one record
        with to_delete:
            to_delete.delete_()

        # Get the updated data
        after_delete = Student({})

        # Assert the size
        assert len(after_delete) == original_size - 1

        # Assert if the deleted data is gone
        for item in after_delete:
            assert item['id'] != id_to_delete


class ResultsView(BaseView):
    _id = IdField()
    score = IntField()
    course = TxtField()
    student = IdField()


class TestEmbeddedCollection:
    pass


class TestEmbeddedViewInContainer:
    def test_in_struct(self):
        tstruct = Struct(student=Student())
        st = str(tstruct)
        assert 'Student' in st

    def test_row_in_struct(self):
        stu_row = Student()[0]
        tstruct = Struct(student=stu_row)
        string = str(tstruct)
        assert '{"student": {}}' in string


class TestObjInside:
    def test_map_change(self):
        """ could do some more of these... like test 2 levels"""
        chng = DBMongoSource.map_change
        assert chng({'abc.def': 4})['abc'] == {'def': 4}

    def test_map_change_mult(self):
        """ could do some more of these... like test 2 levels"""
        chng = DBMongoSource.map_change
        changed = chng({'abc.def': 4, 'abc.2nd': 7})
        assert changed['abc'] == {'def': 4, '2nd': 7}

    def test_init(self):
        students = StudentWithNameFieldWithAlias()
        assert len(students) == 0
        student = students.insert_()
        assert len(students) == 1
        assert type(student) == ViewRow
        with student:
            student.first_name = 'fred'
            assert students._dbRows[0]['Students']['name'] == {"first_name": "fred"}
            assert 'name.first_name' in students.changes_[0]['Students']
        pass


class Teachers(Student):
    models_ = viewModelDB.default(viewModelDB.baseDB.db.Teachers)


class TestReUseView:
    def test_via_init(self):
        model = viewModelDB.default(viewModelDB.baseDB.db.Teachers)
        teaches = Student({}, models=model)
        assert len(teaches) == 0
        teach = teaches.insert_()
        with teach:
            teach.name = 'tom'
        pass

    def test_subclass(self):
        teaches = Teachers({})
        assert len(teaches) == 1
        teach = teaches.insert_()
        with teach:
            teach.name = 'bill'
        pass


class TestUpDateNoRead:
    def test_update_status(self):
        students = Student({})
        assert len(students) > 0
        first = students[0]
        sid = str(first.id)
        assert first.course_year == 2
        assert len(sid) > 10
        students = Student()
        newfirst = students.insert_()
        with newfirst:
            newfirst.id = sid
            assert isinstance(newfirst.id, ObjectId)  # check setting id via string
            newfirst.course_year = 3
        students = Student({})  # read back
        assert students[0].course_year == 3


from viewmodel import AuthBase
from dataclasses import dataclass


@dataclass
class SimpleAuth(AuthBase):
    _memberID: int
    _member_string: str

    @property
    def memberID(self):
        return self._memberID

    @property
    def member_string(self):
        return self._member_string


class TestJournal:
    """
    Test that changes made on appropriately annotated view fields (annotated with 'journal=True') are logged in the
    new collection called 'Journal'. Previously, this was file based but a decision was made to change to be DB based.
    """

    def test_changes_to_view_are_journalled(self):
        # Create a new student view
        students_view = Student()
        # Is view empty?
        assert len(students_view) == 0
        # Track the student name property only
        students_view.fields_['name'].field.journal = True
        # Prepare view for insert
        students_view.insert_()
        # Has a row been inserted?
        assert len(students_view) == 1
        assert len(students_view.changes_) == 1
        assert len(students_view.log_changes_) == 1
        # Get the first row
        student_zero = students_view[0]

        # Define the Journal model
        models_ = viewModelDB.default(viewModelDB.baseDB.db.Journal)
        # Save the length of the journal_view (it might already have something in it) - used below
        journal_view_size = len(JournalView({}, models=models_))

        # Work with the students[0] e.g. change the value stored in 'name', etc
        with student_zero:
            student_zero.name = "whatever"  # journalled
            student_zero.course = "changed"  # not journalled
            # What changes & log_changes_have been captured in the underlying changes_ & log_changes_ data structures?
            changes = students_view.changes_[0]['Students']
            log_changes = students_view.log_changes_[0]['Students']
            # Has the number of changes increased?
            assert len(changes) == 2
            # Has the change to the 'name' property been captured in log_changes_?
            assert len(log_changes) == 1

        # open a new journal_view
        journal_view = JournalView({}, models=models_)
        # Check that the update made on the student name is recorded in the journal
        assert len(journal_view) == journal_view_size + 1
        # Who made the change? What values are captured for memberId & memberName.
        # Get the last row in the view (might be more than 1 row in the view)
        auth = journal_view.auth
        assert journal_view[-1].memberId == auth.memberID
        assert journal_view[-1].memberName == auth.member_string
        assert journal_view[-1].collection == "Students"
        assert isinstance(journal_view[-1].dateTime_, datetime)
        assert "whatever" in journal_view[-1].updates

    def test_changes_to_view_are_journalled_with_auth(self):
        # Create a new student view
        auth = SimpleAuth(1, "me")
        students_view = Student(auth=auth)
        students_view.fields_['name'].field.journal = True
        # Prepare view for insert
        students_view.insert_()
        student_zero = students_view[0]

        models_ = viewModelDB.default(viewModelDB.baseDB.db.Journal)
        journal_view_size = len(JournalView({}, models=models_))

        with student_zero:
            student_zero.name = "from_me"  # another chang

        # new journal_view
        journal_view = JournalView({}, models=models_)
        assert len(journal_view) == journal_view_size + 1
        # Who made the change? What values are captured for memberId & memberName.
        # Get the last row in the view (might be more than 1 row in the view)
        assert journal_view[-1].memberId == auth.memberID
        assert journal_view[-1].memberName == auth.member_string
        assert journal_view[-1].collection == "Students"
        assert isinstance(journal_view[-1].dateTime_, datetime)
        assert "from_me" in journal_view[-1].updates
