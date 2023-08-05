from dataclasses import dataclass

import pytest

from viewmodel import BaseView
from viewmodel.viewFields import Fmt, ObjListField, TxtField, viewModelDB

testObjFields = viewModelDB.baseDB.db.testObjListFields


@dataclass
class Number:
    number: str
    # extra: str = "not yet used"


class SampleLists(BaseView):
    models_ = None
    obj_list = ObjListField("obj list", elementObjType=Number)


class ObjListFieldView(BaseView):
    models_ = testObjFields
    nested = ObjListField(elementObjType=Number)
    names = TxtField("Name Field")





@pytest.fixture
def AndrewView():
    view = ObjListFieldView({"names": "Andrew"})
    if len(view) == 0:
        row = view.insert_()
    else:
        row = view[0]
    with row:
        row.names = "Andrew"
        row.nested = [Number("one"), Number("two"), Number("three")]
    return ObjListFieldView({"names": "Andrew"})


class TestIdxKeys:

    def test_idxKey(self):
        idxKey = ObjListField.idxKey
        assert idxKey(5) == "0005", "idxkey should work with int"
        assert idxKey("5") == "0005", "idxkey should work with str"
        assert idxKey("5.2") == "0005.0002", "idxkey should allow 'dots'"

    def test_idxKeyVal(self):
        idxKeyVal = ObjListField.idxKeyVal
        assert idxKeyVal(5) == 5, "idxkeyval should allow int"
        assert idxKeyVal("5") == 5, "idxkeyval should allow str"
        assert idxKeyVal("5.2") == 6, "idxkeyval return indictates beyond base int"


class TestObjListField:
    expectedData = [Number("one"), Number("two"), Number("three")]

    def test_txtField_write(self):
        view = ObjListFieldView({})
        assert len(view) == 0

        with view.insert_() as row:
            row.names = "Peter"

        assert len(view) == 1
        assert view.names == "Peter"

    def test_objlist_write_with_map(self):
        view = ObjListFieldView({})
        expected = [{"number": "one"}, {"number": "two"}, {"number": "three"}]
        row = view.insert_()
        with row:
            row.names = "Geoff"
            row.nested = expected

        assert row.nested == self.expectedData

    def test_objlist_write_with_object(self):
        view = ObjListFieldView({})
        expected = [Number("four"), Number("two"), Number("three")]

        row = view.insert_()
        with row:
            row.names = "Andrew"
            row.nested = expected

        assert row.nested == expected

    def test_objlist_object_field_update(self, AndrewView):

        expected = [Number("one"), Number("seven"), Number("three"), Number("eighteen")]
        updates = {"001": {"number": "seven"}, "003": {"number": "eighteen"}}

        row = AndrewView[0]  # should be andrew
        with row:
            row.nested = updates

        assert row.nested == expected

    def test_db_saved_values(self):
        view = ObjListFieldView({})
        assert view[0].names == "Peter"
        assert view[1].names == "Geoff"
        assert view[2].names == "Andrew"

    def test_objlist_object_update_field_with_deletion(self, AndrewView):
        expected = [Number("one"), Number("seven"), Number("eighteen")]
        # updates = {"001": None}
        updates = {"001": None, "002": {"number": "seven"}, "003": {"number": "eighteen"}}

        row = AndrewView[0]  # should be andrew
        with row:
            row.nested = updates

        assert row.nested == expected

    def test_obj_list_set_str(self):
        """ set from str only valid for json str"""
        sample_list = SampleLists()

        sample_list.obj_list = "test"  # cannot set as non json string so get empty list
        assert sample_list.obj_list == []
        sample_list.obj_list = '[{"number":1}]'  # valid json
        assert isinstance(sample_list.obj_list[0], Number)
        assert sample_list.obj_list[0].number == 1

    def xtest_obj_list_with_escape_in_string(self):
        obj_list = SampleLists()
        obj_list.obj_list = '[{"\"under\"the weather"}]'
        assert obj_list.obj_list == '[{"\"under\"the weather"}]'
