# -*- coding: utf-8 -*-
# Named 'test_1_views to ensure this runs first as it is the most basic tests
import json
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from unittest.mock import MagicMock

import pytest
from bson import Decimal128
from bson.objectid import ObjectId
from dataclasses import dataclass
from objdict import (ObjDict)

from viewmodel import viewFields
from viewmodel.viewFields import (
    BaseField, Case, DateField, DateTimeField, DecField, DisplayType, EnumField, EnumForeignField, Fmt, IdAutoField,
    IdField,
    IntField, SimpleDateTimeField, TimeField, TxtField, viewModelDB, ObjListField
)
from viewmodel.viewModel import BaseView, NestedView


@pytest.fixture
def req():
    res = MagicMock(spec=SaltReq)
    res.getData = {}
    res.postData = {}
    res.hostName = 'salt'
    res.saltScript = 'register'
    return res


@pytest.fixture
def testmid():
    return 8


class EColour(Enum):
    red = 'r'
    blue = 'b'
    green = 'green'  # to provide test of value is also a name

@dataclass
class SubViewObject:
    """SubView should provide this functionality but does not at this stage"""
    label: str
    paragraph: str = None

@dataclass
class Numeric:
    one: str


class SubView(BaseView):
    models_ = None
    viewName_ = "ListData"
    label = TxtField('Sub Label', 10)
    paragraph = TxtField("Longform text", fmt=Fmt(displayType=DisplayType.TextMultiLine.value))

class SampleView(BaseView):
    models_ = None
    id = IdField(name='sqlid', cases={})
    salt = IntField(cases={})
    label = TxtField('Label for Profile', 10)
    date = DateField('Date')
    time = TimeField('Time', cases={})
    datetime = SimpleDateTimeField('DateTime', cases={})
    newfield = TxtField('new', 10, cases={})
    amount = DecField("0.1")
    colour = EnumField(fmt=Fmt(names=("red", "green", "blue")), cases={})
    colour2 = EnumField(fmt=Fmt(values=EColour), cases={})
    country = EnumForeignField('Default Country', session=viewModelDB,
                               dispFields=('countries.countryName',),
                               values='countries.phoneCode'
                               )
    first_name = TxtField(src='.name', cases={})
    mainHTML = ObjListField('HTML main version', elementObjType=Numeric)
    testHTML = ObjListField('HTML test version', elementObjType=SubViewObject, elementObjectView=SubView)



    # favourites  = FavField('theFavs!')
    # extra = TxtField('used as a dummy',src=None)
    def getRows_(self):
        row = ObjDict(id=1)
        row.salt = 5
        row.label = 'Label'
        row.colour = 1
        row.colour2 = 'b'
        row.country = '061'
        row.amount = Decimal128('2.7')
        row.date = datetime(16, 2, 1)
        row.time = time(16, 15)
        # row.time = datetime( 16,3, 2)
        row.mainHTML = [{"one": "Hello World"}]
        row.testHTML = [{"label": "Hello World"}]
        return [ObjDict(((self.row_name_, row),))]


@pytest.fixture
def sampleView():
    return SampleView()


class SampleDefView(BaseView):
    models_ = None
    id = IdField(name='sqlid', cases={})
    salt = IntField(cases={}, value=5)
    label = TxtField('Label for Profile', 8, value='Label')
    date = DateField('Date', datetime(16, 2, 1))
    newfield = TxtField('new', 10, cases={})
    amount = DecField("0.1")


class SampleIdView(BaseView):
    models_ = None
    id = IdField(name='id')
    id2 = IdField(name='id')
    sid = IntField(name='sqlid')
    rawsql = BaseField(name='sqlid')
    rawid = BaseField(name='id')
    rawidu = BaseField(name='_id')
    auto = IdAutoField()
    salt = IntField(cases={})


@pytest.fixture
def sampleIdView():
    return SampleIdView()


class SampleIdView2(BaseView):
    models_ = None
    id = IdField()
    id2 = IdField(name='id')
    rawid = BaseField(name='id')
    rawidu = BaseField(name='_id')
    auto = IdAutoField()
    salt = IntField(cases={})


@pytest.fixture
def sampleIdView2():
    return SampleIdView2()


class TestFuncs:
    def test_str_to_date1(self):
        strto = viewFields.strToDate
        assert strto("2017/03/02") == datetime(2017, 3, 2)


class TestDefaults:
    def test_def_int(self):
        view = SampleDefView()
        assert view._dbRows[0]['__None__'] == {}  # ensure no actual data
        assert view.salt == 5  # but it looks like data through defaults
        assert view.label == 'Label'


class TestFields:
    def testText(self, sampleView):
        assert sampleView.label == 'Label'
        assert sampleView[0]['label'].value == 'Label'
        assert sampleView[0].label == 'Label'

    def testDateFld(self, sampleView):
        assert sampleView[0].date == date(16, 2, 1)
        assert sampleView[0]['date'].strvalue == ' 1/02/0016'

    def testTimeFld(self, sampleView):
        assert sampleView.time == time(16, 15)
        # import pdb; pdb.set_trace()
        assert sampleView[0]['time'].strvalue == ' 16:15'

    def testEnum(self, sampleView):
        assert sampleView[0].colour.name == "red"
        assert sampleView[0].colour.value == 1

    def testEnum2(self, sampleView):
        assert sampleView[0].colour2.name == "blue"
        assert sampleView[0].colour2.value == 'b'

    def testEnumForeignKey(self, sampleView):
        assert sampleView.country.value == '061'

    def test_decimal_value(self, sampleView):
        assert sampleView.amount == Decimal('2.7')

    def test_new(self, sampleView):
        assert sampleView.newfield == ''

    def test_embed(self, sampleView):
        assert sampleView.first_name == ''

    def test_obj_list_field_element_obj_type(self, sampleView):
        assert isinstance(sampleView.testHTML[0], SubViewObject)
        assert sampleView.testHTML[0].label == "Hello World"


class TestViewJsonPrimitives:
    def test_find_sub_views(self, sampleView):
        sub_views = sampleView.sub_views_()
        assert SubView in sub_views,"test can get list of nested views used within fields "

    def test_view_name(self, sampleView):
        assert "SampleView" in sampleView.safeName_,"class name contained in view name when no view name"
        assert SubView().safeName_ == "ListData","class name otherwise is as provided by viewName_ "


@pytest.fixture()
def sample_json(sampleView):
    return json.loads(sampleView.__json__())


class TestValuesPropagateToJSON:
    def test_jsonrow(self, sampleView):
        jsdata = sampleView[0].__json__(True)
        assert jsdata.label == "Label"

    def test_json_topLevel(self, sampleView):
        jsdata = sampleView.__json__()
        json_data = json.loads(jsdata)
        topLevelFieldsKeys = list(json_data.keys())
        expectedTopLevelKeys = ['className', 'viewName', 'idx', 'data', 'fields', 'objects']
        for key in expectedTopLevelKeys:
            assert key in topLevelFieldsKeys, f"{key} should be present in View json"

    def test_topLevel_values_that_are_simple(self, sampleView):
        jsdata = sampleView.__json__()
        json_data = json.loads(jsdata)
        assert json_data['className'] == "SampleView"
        assert "SampleView" in json_data['viewName']
        assert json_data["idx"] == None, "value should match row to be dislayed first"
        # ToDo why is idx None, should test when it has a value too


    def test_json_secondLevel_fields(self, sampleView):
        jsdata = sampleView.__json__()
        json_data = json.loads(jsdata)
        secondLevelFieldsKeys = list(json_data["fields"].keys())
        expectedSecondLevelFields = ['id', 'salt', 'label', 'date', 'time', 'datetime', 'newfield', 'amount',
                                  'colour', 'colour2', 'country', 'first_name', 'testHTML']

        for i in expectedSecondLevelFields:
            assert json_data["fields"][i]

    def test_json_field_values(self, sampleView):
        jsdata = sampleView.fields_['label'].__json__(True)
        assert jsdata['label'] == "Label for Profile"
        assert jsdata['fmt'].wide == 10
        assert jsdata['fmt'].max == 10
        assert jsdata['fmt'].postPrefix == 'field'
        assert jsdata['fmt'].readOnlyBracket == '  '

    def test_json_objects(self, sample_json):
        assert "SubView" in sample_json["objects"], "SubView should be in objects since used by TestHtml"
        assert "label" in sample_json["objects"]["SubView"], "should have info for label field"

    def test_json(self, sampleView):
        jsdata = sampleView.__json__()
        assert "Label for Profile" in jsdata

        json_data = ObjDict(jsdata)
        assert hasattr(json_data.fields.label, 'fmt')
        assert hasattr(json_data.fields.label.fmt, 'wide')
        assert json_data.fields.label.fmt.wide == 10
        assert hasattr(json_data.fields.label.fmt, 'max')
        assert json_data.fields.label.fmt.max == 10

    def testDisplaySubTypeInJSON(self, sampleView):
        jsdata = sampleView.__json__()
        json_data = json.loads(jsdata)
        testHTMLFieldsData = json_data["fields"]["testHTML"]["fmt"]
        assert testHTMLFieldsData["displayType"] == 'ObjectList'

    def testElementObjectViewInJSON(self, sampleView):
        jsdata = sampleView.__json__()
        json_data = json.loads(jsdata)
        testHTMLFieldsFmtData = json_data["fields"]["testHTML"]["fmt"]
        assert testHTMLFieldsFmtData["elementObjectView"] == SubView.__name__

    def test_Enum_selected_value_in_view(self, sampleView):
        """Test whether we could get the selected value for a Enum"""
        view_info = ObjDict(sampleView.__json__())  # this test should be reproduced in TestFields without using json method
        assert hasattr(view_info.data[0], 'country')
        assert view_info.data[0].country == '061'

    def test_EnumKey(self, sampleView):
        fields_info = sampleView.fields_['country'].__json__(True)   # this test should be reproduced in TestFields without using json method
        assert 'type' in fields_info
        assert fields_info['type'] == 'Enum'

        assert 'items' in fields_info
        assert isinstance(fields_info['items'], list)
        assert {'Australia': '061'} in fields_info['items']
        assert {'Indonesia': '062'} in fields_info['items']

    def test_subLevel_json_objects_displayType(self,sample_json):
        sub_objects = sample_json["objects"]["SubView"]
        assert sub_objects["label"]["fmt"]["displayType"] == 'TextSingleLine', "testing sub view fmt data can be read"
        assert sub_objects["paragraph"]["fmt"]["displayType"] == 'TextMultiLine'

class TestSetFields:
    def testText(self, sampleView):
        assert sampleView.label == 'Label'
        assert sampleView[0]['label'].strvalue == 'Label'
        sampleView[0]['label'].strvalue = 'xLabel'
        assert sampleView[0]['label'].strvalue == 'xLabel'

    def testDateFld(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        assert sampleView[0]['date'].strvalue == ' 1/02/0016'
        # assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView[0]['date'].strvalue = '02/03/2017'
        assert sampleView.date == date(2017, 3, 2)

    def testDateFld2(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        save = sampleView[0]['date'].strvalue
        assert save == ' 1/02/0016'
        # assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView[0]['date'].strvalue = '02/03/2017'
        assert sampleView.date == date(2017, 3, 2)
        sampleView[0]['date'].strvalue = save
        assert sampleView.date == date(16, 2, 1)

    def test_date_from_str(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        save = sampleView[0]['date'].strvalue
        assert save == ' 1/02/0016'
        # assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView.date = ' 2032017'
        assert sampleView.date == date(2017, 3, 2)
        sampleView[0]['date'].strvalue = save
        assert sampleView.date == date(16, 2, 1)

    def testTimeFld(self, sampleView):
        sampleView[0]['time'].strvalue = '10:15'
        assert sampleView.time == time(10, 15)

    def testDateTimeFld(self, sampleView):
        sampleView[0]['datetime'].strvalue = '2015/11/02 10:15'
        assert sampleView.datetime == datetime(2015, 11, 2, 10, 15)

    def test_dec_fld(self, sampleView):
        assert sampleView.amount == Decimal('2.7')
        assert sampleView[0]['amount'].strvalue == '2.7'
        sampleView[0]['amount'].strvalue = '3.50'
        assert sampleView.amount == Decimal('3.5')
        sampleView.amount = Decimal('1.23')
        assert sampleView.amount == Decimal('1.2')

    def test_set_enum2_when_name_and_value_match(self, sampleView):
        assert sampleView[0].colour2.name == "blue"
        sampleView[0].colour2 = 'green'  # EColour('green')
        assert sampleView[0].colour2.name == 'green'
        assert sampleView[0].colour2.value == 'green'

    # @pytest.mark.xfail(raises=ValueError)
    def test_set_enum2_not_name_or_value(self, sampleView):
        assert sampleView[0].colour2.name == "blue"
        with pytest.raises(ValueError):
            sampleView[0].colour2 = 'yellow'

    def test_set_enum2_not_name_or_value_but_default(self, sampleView):
        assert sampleView[0].colour2.name == "blue"
        sampleView[0]['colour2'].field.fmt.default = EColour.green
        sampleView[0].colour2 = 'orange'
        assert sampleView[0].colour2.name == 'green'
        assert sampleView[0].colour2.value == 'green'

    def test_set_embed(self, sampleView):
        assert sampleView.first_name == ''
        sampleView[0].first_name = 'fred'
        assert sampleView.first_name == 'fred'

    def test_id_fld(self, sampleIdView, sampleIdView2):
        siv, siv2 = sampleIdView, sampleIdView2
        assert siv.id is None
        assert siv.rawsql is None
        assert siv.sid is None
        assert siv.auto is None
        assert siv2.id is None
        siv.rawidu = 10
        assert siv.auto == 10
        siv.rawsql = 15
        siv.rawid = 12
        siv2.rawid = 112
        siv2.rawidu = 113
        assert siv.auto == 15
        assert siv.sid == 15
        assert siv.rawsql == 15
        assert siv.id == 12
        assert siv.id2 == 12
        assert siv2.id == 113
        assert siv2.id2 == 112

    def test_id_fld_set(self, sampleIdView, sampleIdView2):
        """ checking type conversion on set of idfield
        """
        siv, siv2 = sampleIdView, sampleIdView2
        siv.id = None
        assert isinstance(siv.id2, ObjectId)


class TestLoops:
    """ testing row structure supports looping through rows
        and within rows through fields"""

    def test_loop_row(self, sampleView):
        loopcount = 0
        for row in sampleView:
            assert row.label == 'Label'
            loopcount += 1
        assert loopcount == 1

    def test_loop_fields(self, sampleView):
        row = sampleView[0]
        names = []
        values = []
        for field in row:
            names.append(field.name)
            values.append(field.value)
        assert names == ['label', 'date', 'amount', 'country', 'mainHTML', "testHTML"]
        assert values == ['Label', date(16, 2, 1), Decimal('2.7'),
                          type(row.country)('061'),[Numeric(one='Hello World')], [SubViewObject(label='Hello World', paragraph=None)]]

    def test_loop_fields_loop(self, sampleView):
        row = sampleView[0]
        names = []
        for field in row.loop_(case=Case.allFields):
            names.append(field.name)
        assert names == ['sqlid', 'salt', 'label', 'date', 'time', 'datetime',
                         'newfield', 'amount', 'colour', 'colour2',
                         'country', 'first_name', 'mainHTML', "testHTML"]


class TestIndexAttr:
    """ testings access to attributes ViewRow """

    def test_row_index(self, sampleView):
        row = sampleView[0]
        assert row['label'].value == 'Label'
        with pytest.raises(TypeError):
            row['label'] = 5

    def test_out_of_range_index_value_raises_index_error(self, sampleView):
        rows = len(sampleView)
        with pytest.raises(IndexError) as e:
            sample_row = sampleView[rows + 1]

        assert "Index value '2' is out-of-range! View has 1 item(s)." in str(e)


class TestView_idx_labelsList:
    def test_view_(self, sampleView):
        assert sampleView.view_ is sampleView
        assert sampleView[0].view_ is sampleView

    def test_idx_(self, sampleView):
        assert sampleView.idx_ is None
        sampleView.idx_ = 3
        with pytest.raises(ValueError):
            sampleView.idx_ = 5

    def test_idx_row(self, sampleView):
        assert sampleView[0].row_idx_ == 0
        with pytest.raises(AttributeError):
            sampleView[0].idx_ = 5

    def test_labelsList_with_no_rowLabel_set(self, sampleView):
        assert sampleView.labelsList_() == ['no labels']

    def test_labelsList_with_rowLabel_set(self, sampleView):
        sampleView._baseFields['label'].rowLabel = True
        assert sampleView.labelsList_() == ['Label']

        # Restore the default value
        sampleView._baseFields['label'].rowLabel = False


class EmptyView(BaseView):
    models_ = None
    id = IntField(name='sqlid', cases={})
    label = TxtField('Label for Profile', 8, value='hello')
    date = DateField('Date')


@pytest.fixture
def emptyView():
    return EmptyView()


class TestEmptyView:
    def test_init(self, emptyView):
        ev = emptyView
        assert len(ev) == 1
        assert ev.label == 'hello'
