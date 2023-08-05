from datetime import datetime
from decimal import Decimal

import pytest
from bson import Decimal128
from objdict import ObjDict, dumps
from viewmodel import BaseView
from viewmodel.viewFields import BoolField, DateTimeField, DecField, SetField, viewModelDB
from viewmodel.vmdatetime import VMDateTime, VMTimezone

from python.viewmodel import BaseField

testFields = viewModelDB.baseDB.db.testFields


class TestBaseField:

    def test_default_values(self):
        field = BaseField()
        assert field.fmt.max == 16


class TestSetField:
    class SetView(BaseView):
        models_ = testFields
        field = SetField()

        def getRows_(self, query=None):
            if query is None:
                return []

            return self.models_.find(query)

    the_list = [1, 1, 2, 3]  # we want duplicates for the sake of the tests
    the_set = [1, 2, 3]  # not actually a set, but no duplicates

    def test_default(self):
        assert SetField().default() == list()

    def test_type(self):
        assert SetField().Type() is list

    def test_insert_list_removes_duplicates_for_database(self):
        with self.SetView().insert_() as view:
            view.field = self.the_list

        data = self.SetView({"field": self.the_set})
        assert data.field == self.the_set

    def test_set_unsupported_type_gives_error(self):
        """
        No point in the set field allowing lists to be saved to the database, or any other type
        because then we might as well just use a list field.
        """
        with pytest.raises(AssertionError):
            with self.SetView().insert_() as view:
                view.field = "I am not a list or a set"

    def test_data_is_list_in_json(self):
        """
        JSON does not support sets so the SetField must convert to a list
        when converting to JSON format.
        """
        view = self.SetView({})
        data = ObjDict.dumps(view)
        json = ObjDict.loads(data)
        assert isinstance(json.data[0].field, list)


default_decimal_value = Decimal()


class TestDecField:
    class DecimalView(BaseView):
        models_ = testFields
        decField = DecField("0.00", value=default_decimal_value)
        defaultDecField = DecField("0")
        customDefaultDecField = DecField("0", value=default_decimal_value)

        intFactorBy100To2dp = DecField("0.00", intFactor=100)
        intFactorBy10To1dp = DecField("0.0", intFactor=10)
        intFactorBy1000To4dp = DecField("0.0000", intFactor=1000)
        intDirectTo0dp = DecField("0")
        intDirectTo3dp = DecField("0.000")

    def test_dec_field_read_write(self):
        testDecimal = Decimal("270")
        with self.DecimalView().insert_() as row:
            row.decField = testDecimal

        data = self.DecimalView({"decField": Decimal128(testDecimal)})
        assert data.decField == testDecimal
        assert data.defaultDecField is None  # If not in db, normally give None
        assert data.customDefaultDecField == default_decimal_value  # user can specify a default when not in db

    def test_dec_field_2dp_quantisation(self):
        testDecimal = Decimal("0.00")
        with self.DecimalView().insert_() as row:
            row.decField = Decimal("0")  # Set value not 2dp

        data = self.DecimalView({"decField": Decimal128(testDecimal)})
        assert str(data.decField) == str(testDecimal)

    def test_dumps_to_json_as_string(self):
        testDecimal = Decimal("99")
        with self.DecimalView().insert_() as row:
            row.decField = testDecimal

        returnedDecimal = Decimal("99.00")
        view = self.DecimalView({})
        json_string = dumps(view)
        assert f'"decField": "{returnedDecimal}"' in json_string

    def test_convert_integer_values_to_decimal(self):
        row = self.DecimalView({"testName": "IntToDecimal"})[0]
        assert row.intFactorBy100To2dp == Decimal("1.23")
        assert row.intFactorBy10To1dp == Decimal("12.3")
        assert row.intFactorBy1000To4dp == Decimal("12.3450")
        assert row.intDirectTo0dp == Decimal("123")
        assert row.intDirectTo3dp == Decimal("1234.000")


class TestBoolField:
    class BoolView(BaseView):
        models_ = testFields
        verified = BoolField()

    def test_bool_field_default_value(self):
        view = self.BoolView()
        default = view.verified
        assert default is False

    def test_bool_field_read_write(self):
        testBool = True
        with self.BoolView().insert_() as row:
            row.verified = testBool

        data = self.BoolView({"verified": testBool})
        assert data.verified == testBool


class TestDateTimeField:
    class DateTimeView(BaseView):
        models_ = testFields
        aDateTime = DateTimeField()

    def test_date_time_field_read_write(self):
        utc = datetime(2020, 4, 21, 5, 34, 23)  # 5:34 AM
        offset = 720  # +12 hours
        offsetDstComponent = 60
        name = "NZST +12"

        dateTime = VMDateTime(utc, timezone=VMTimezone(offset, name, offsetDstComponent))
        with self.DateTimeView().insert_() as row:
            row.aDateTime = dateTime

        data = self.DateTimeView({"aDateTime.utcDateTime": dateTime.utcDateTime})
        assert data[0].aDateTime.utcDateTime == dateTime.utcDateTime
        assert data[0].aDateTime.timezone == dateTime.timezone
        savedData = data._dbRows[0]["testFields"]["aDateTime"]["localisedFilters"]
        assert savedData["timeOfDay"] == 1054  # 1054 minutes is 17:34 or 05:34 +12 hours
        assert savedData["dayOfWeek"] == 2
        assert savedData["dayOfMonth"] == 21
        assert savedData["month"] == 4
        assert savedData["year"] == 2020

    def test_support_reading_simple_datetime(self):
        expected = datetime(2008, 10, 6, 0, 0, 0)
        data = self.DateTimeView({"aDateTime": expected})
        assert data[0].aDateTime.utcDateTime == expected

    def test_read_vmdatetime_without_timezone(self):
        utc = datetime(1999, 1, 1, 1, 1, 1)
        dateTime = VMDateTime(utc, timezone=None)
        with self.DateTimeView().insert_() as row:
            row.aDateTime = dateTime

        data = self.DateTimeView({"aDateTime.utcDateTime": utc})
        assert data[0].aDateTime.utcDateTime == utc
        assert data[0].aDateTime.timezone is None
