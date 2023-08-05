# 2.02 feb 2008
# improved editDrawN  for arrays to handle display as well as edit
import copy
import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

# import saltSqlaDB
from bson import Decimal128
from bson.objectid import ObjectId

from .vmdatetime import VMDateTime, VMTimezone

try:
    import saltMongDB as viewModelDB
except ImportError:
    # from .
    import viewmodel.viewMongoDB as viewModelDB

import datetime
from collections import namedtuple
from dataclasses import asdict
from itertools import count
from objdict import unParse, ObjDict, Struct, OEnum
from enum import Enum, EnumMeta

Case = Enum('ViewCase', 'viewAll viewOne edit allFields')


# 'edit' in Case.__members__    viewAll is for viewAll rows


class ModelStatus(dict):
    def __init__(self, action=None, **kwargs):
        super().__init__(**kwargs)

        if action is not None and not isinstance(action, ActionType):
            raise ValueError('Expected type of `action`: None or `ActionType`')

        self.action = action

    def __setitem__(self, keys, v):
        if isinstance(keys, tuple):
            assert len(keys) == 2, "Only two keys allowed for set of ModelStatus"
            entry, subentry = keys
            if not entry in self:
                self[entry] = ModelStatus()
            self[entry][subentry] = v
        else:
            super().__setitem__(keys, v)


class ActionType(OEnum):
    Insert = 1
    Delete = 2


def noBlanks(plist):
    return [p if p else '<blank>' for p in plist]


class FieldItem:

    def __init__(self, viewObj, field, row_index):
        ''' viewobj is obj containing value and prop is property '''
        self.viewObj = viewObj
        self.field = field
        self.types = FieldTypes()
        self.idx = row_index

    def __getattr__(self, name):
        return getattr(self.field, name)

    def __json__(self, internal=False):

        fields_dict = {
            'class_string': str(self.field),
            'idx': self.idx,
            'cases': self.field.cases,
            'hint': self.field.hint,
            'label': self.field.label,
            'fmt': self.field.fmt,
            'misc': self.field.misc,
            'name': self.field.name,
            'postID': self.field.postID,
            'postPrefix': self.field.postPrefix
        }

        if isinstance(self.Type, EnumMeta):
            fields_dict['type'] = 'Enum'
            fields_dict['items'] = []

            for item in self.Type:
                fields_dict['items'].append({
                    item.name: item.value
                })

        res = fields_dict

        if not internal:
            res = str(fields_dict)

        return res

    @property
    def Type(self):
        return self.field.Type(self.viewObj)

    @property
    def fieldatt(self):
        """since get attr looks in field, this should not be needed
           other than to make what is happening clearer in code
        """
        return self.field

    @property
    def value(self):
        return self.field.__get__(self.viewObj, None, self.idx)

    @value.setter
    def value(self, svalue):
        self.field.__set__(self.viewObj, svalue, self.idx)

    @property
    def json_value(self):
        """
        An alternate value for which to store in a JSON string.
        If not specified the normal value is presumed to be JSON compatible.
        """
        if hasattr(self.field, "json_value"):
            return self.field.json_value(self.viewObj, idx=self.idx)

        return self.value

    @property
    def strvalue(self):
        rawval = self.field.__get__(self.viewObj, None, self.idx)
        val = self.field.toStr(rawval)
        return str(val)

    @strvalue.setter
    def strvalue(self, svalue):
        '''note it could be that __set__ handles str format anyway
          actual class may override either, but no need to do both'''
        self.field.__set__(self.viewObj, self.field.Type(self.viewObj)(svalue),
                           self.idx)


class DisplayType(Enum):
    """
    Display Types and how they will be represented on the web.

    Use for Fmt.displayType

    Numeric: A regular text input field occasionally we will have use for number input fields if we want to increment
        numeric values on the screen
    Text/String: A regular text input field. Should also describe what type editor is necessary for this field
        SingeLine: Should be represented by a single line text input field. The use case is varied but likely reserved
         for Titles and Headings.
        MultiLine: A multiple-line text input field. Used for long-form text like paragraphs but can be used for
            everything but Titles and Headings.

    Boolean: Can be represented in several ways, the default should probably be checkbox but it can also be a
        dropdown list or a radio button.
    Enum: Dropdown list or Radio Buttons.
    List of Objects: For instance a list of Text fields which consists of a label, imgPanel, txtPanel field.
        Should be displayed as grouped fields logically, with subheadings to describe what the field is.
        These fields can be single or multi-line editable so this information should come with the format data.
    Map of Objects: Bit confusing, would this not be functionally the same as a list of objects? We would display all
        objects that are on the same level as if they were a part of a list of objects with subheadings describing what
        the field is.
    """
    Numeric = "Numeric"
    TextSingleLine = "TextSingleLine"
    TextMultiLine = "TextMultiLine"
    Boolean = "Boolean"
    Enum = "Enum"
    Object = "Object"
    ObjectList = "ObjectList"
    ObjectMap = "ObjectMap"


class Fmt(Struct):
    """ the original idea of format was to capture a variety of extra data for
    rendering info, but originally fell into the faux class trap (and was dict)

    the names and values lists can be extracted from an enum
    (if an enum is given as the values parameter), or supplied separately.
    if names and not values are supplied, then the convention of Python
    (1,2,3 etc) will be used for the values
    note: an Enum field uses these two lists to create a new equivalent type,
    not the actual Enum type supplied as values
    """

    def __init__(self, wide=0, date=None, time=None, max=0,
                 names=[], values=[],
                 readOnlyBracket="  ",
                 rowspc=[],  # not currently used in serverjs ... needs review
                 vals=[],
                 default=NotImplemented, displayType=DisplayType.TextSingleLine.value, elementObjectView=None):
        self.wide = wide  # width to use for display, 0 = use default for type
        self.max = max  # maximum number of characters can be entered (0=same max as width)
        self.date = date
        self.time = time
        self.names = names
        self.default = default
        self.displayType = displayType
        self.elementObjectView = elementObjectView
        if vals != []:
            print("vals are:", vals)
            if vals != values:
                print("and not like values:", values)
        if isinstance(values, EnumMeta):
            self.values = [v.value for v in values.__members__.values()]
            self.names = [v for v in values.__members__]
        else:
            self.values = values
        self.postPrefix = "field"  # why is this in here?
        self.readOnlyBracket = readOnlyBracket

    @classmethod
    def getfmt(cls, data):

        if isinstance(data, cls):
            return data
        elif isinstance(data, dict):
            # print("data is ",data)
            return cls(**data)
        return cls()

    def __json__(self, internal=False):
        res = super().__json__(internal=True)
        if self.elementObjectView is not None:
            res["elementObjectView"] = self.elementObjectView.__name__
        if not internal:
            res = str(res)
        return res


class BaseField(object):
    """ fm elts make up the screen of fmpages
    elts may refer to data from the database table- or not!
    """
    """
    take II - to be rename FmCols or XxxCols with the base as BaseCol
    Cols are logical fields in the db. They may be direct db cols (db=True)
    or calculated from other columns.
    Columns with that are only used to calcuate other columns have form=False

    a dictionary of Cols derived from basecol is needed by a SaltTable to enable
    the salttable to do the following:-
      for every logical 'col' - render a html view of the data
                            - render an html input form of the data
                            -render a default label
                            -render a hint
                            -xtract new values from post data from an earlier input render
        salt tables have a 'render' method to perform those tasks - see saltTable class

    """
    clsCounter = count(0)

    def __init__(self, label=None, maxim=16, wide=0, hint="", *, hint2='', name=None, src='',
                 rowLayout='[xx]', fmt={}, edit=True, readOnlyBracket="  ", db=None, row=None,
                 form=True, misc=None, colwidth=0, postPrefix='field', value=None, posn=0,
                 comment="", rowLabel=False, key=None, cases=None, journal=False, elementObjType=None,
                 elementObjectView=None):
        """
        'src' is where the data is located - by default this is assumed to be in the first
             database rows of the container view class.  Set src=None for fields with no external source.
        'name' is the field name matches sql row db(where relevant - sql). Normal name is not provided
            as a paramter, and calculated from the name of attribute the field is assigned to
            If 'src' is not None and name is not in the rows provided, then an error will result
            for MongoDB src can indicate the object containing the field

        label is the display version of the name-None for use name, empty string for blank

        maxim is the maximum field width
        wide is the display width
        hint,hint2 hint is for 'help' type display...hint2 may be deprecated or reused for long verison
        rowLayout  - deprecated!
        fmt: contains field postPrefix, width etc plus sub field information
            -(eg enum texts)see indivdual fld types for more details

        #To Do: Joining together elementObjType with elementObjectView
        elementObjType: a class used to wrap database data when more than a plain dict is required.


        ---> deprec fields follow!
        edit is now deprecated...it is decided by the view ???
        readOnlyBracket ...still in use for wrapping 'd'isplay views...could be a render parm?


        db - dbTable that field is in. Can be set after __init__. Cols can also exist without a table
                set as '' at init(rather than None) to have no table & prevent setname setting a valid db

        row - same rules as db- and moving to supercede db so db is extracted from row
            the row object holds all col entries in a dict. thus a datatable can have
            several active rows each having a its own set of cols .

        form is a bool- field existing on the form but not in db?
        posn is the character position within the field. A single text dbfield can support
            a set of logical cols (bool and scalar cols support this) allowing 'flags' contain
            several subelements

        value is taken as the initial value.  The insert_ method uses this value to initialise
            new fields in inserted rows.  Note 'None' values are ignored, and one insert_()
            occurrs automatically for DBNoSource sources so by default the 'value' will appear.

        <---- end of deprec

        misc is for use by individual derived classes
        colwidth ...tba(but it is in use)

        postPrefix... the string to use when to avoid display id clashes
        postID:   a property retrieveing the field name with the postPrefix attached


        _value - the data content. None indicates it should be loaded from the dbTable.data
        value: property for actual value
        strvalue: property for 'str' version of value. Obtain str formatted for display and parse str
            in order to set value


        comment is just that- allows adding a comment. nothing is done with the comment at this time

        rowLabel:  True if use this field is a label for the row

        cases:
           if not None (all cases) then this is the cases in which the field is to be included in iteration
           (as per 'Case' type posibilities)

        journal: a flag set on fields that are to be journalled

        viewobj:  the view object this field is on - set during 'setup' which is called from viewObject.

        subObjectView: for fields with nested views (e.g ObjListField), ViewModel of the subObject
        ( it could be considered only having this data in the fields with nestedViews )

        deprecated:
           key is the key in the columns dict - not the db key (which is name).
            This allows for virtual cols with different keys than the dbcol name
        )"""
        # self.instanceNum = self.clsCounter
        # self.__class__.clsCounter += 1
        self.instanceNum = next(self.clsCounter)
        # print('instance field label:{} count:{}'.format(label,self.instanceNum))

        if hasattr(self, 'preInit'):
            self.preInit()
        self.name = name
        self.asked_name = name
        self.src = src
        self.raw_src = src if isinstance(src, str) else ''

        """ deprec for now
        if key:
            self.key=key
        else:
            self.key=name"""

        if src is None:
            self._value = value if value is not None else ''
        # default empty string if no src for column
        # src = None is not a useful way to specify src....
        #  unless perhaps there is a default name for a src of None?

        self._default = value

        self.postPrefix = postPrefix

        self.label = label  # updated at setup
        self.rowLabel = rowLabel

        def hintMap(hint):
            if hint == '' or hint[:1] == ' ':
                return hint
            return '' + hint  # we are adding a <br> here

        self.hint = hintMap(hint)
        self.hint2 = hintMap(hint2)
        self.cwidth = colwidth
        self.posn = posn
        self.elementObjType = elementObjType

        if wide == 0:
            wide = maxim
        # self.fmt = {'size': wide, 'max': maxim,
        #             'postPrefix': postPrefix, 'readOnlyBracket': readOnlyBracket}
        # self.fmt.update(fmt)
        # a strange thing is wide could come from fmt... or from

        if isinstance(fmt, Fmt):  # allows for a format handed in as a template
            localfmt = copy.copy(fmt)
            if fmt.wide == 0:
                localfmt.wide = wide
            if fmt.max == 0:
                localfmt.max = maxim
            if elementObjectView is None:
                localfmt.elementObjectView = elementObjectView
            self.fmt = localfmt
        else:
            fmtdata = dict(wide=wide, max=maxim, elementObjectView=elementObjectView)
            fmtdata.update(fmt)
            self.fmt = Fmt.getfmt(fmtdata)

        # import pdb; pdb.set_trace()

        self.layout = {}  # 2015  is this deprecated?
        # if hasattr(rowLayout,'islower'):#test for string
        #   self.layout={'row':rowLayout}
        # else:
        #   rowLayout['row']=defVal(rowLayout,'row','[xx]')
        #   self.layout=layout
        # self.readOnlyBracket=readOnlyBracket

        # 2015 ....following enties
        self.noEdit = not edit
        self.edit = edit
        # self.mkFmtStrs(rowLayout)
        # self.labelStr=self.mkLabelStr()
        # self.fieldStr=self.mkFieldStr()
        # self.rowBracks()

        # self.dbTable=db
        # self.row=row

        if name == "":
            self.db = False
        self.misc = misc if misc else {}

        self.cases = cases
        self.journal = journal
        return

    def __get__(self, obj, objtype=None, idx=None):
        """ field could be local, could be direct in view.rows_,
            or each row could have multiple documents from separate collections
            with 'source' indicating the relevant collection: effectively a join
            'Lazy' get allows retrieving the data from the collection on demand
            where 'joins_' is set to indicate which collections

            the format returned by get is the 'working format' of the type
            this is the type of the value from the perspective of programs
            doing calcualtions with the value

            idx is the row to be accessed
        """
        # import pdb; pdb.set_trace()
        if idx is None:
            if len(obj._dbRows) > 1:
                raise TypeError("cannot read direct from multi element view")
            idx = 0  # we have just ensured only 1 row maximum
        if obj is None:  # test if called from class not instance
            return None

        if obj._dbRows:
            src_nm = obj._source_list[self.src]
            if src_nm not in obj._dbRows[idx]:
                obj._sources[src_nm].loader(idx)

            srcdict = obj._dbRows[idx][src_nm]
            for embed in self.src_dicts:
                srcdict = srcdict.get(embed, {})

            value = srcdict.get(self.name, self.default(obj))
            return value

        return self.default(obj)

    @staticmethod
    def toStr(val):

        return str(val)

    @staticmethod
    def storageFormat(data):
        """ convert data from format returned by get, to raw database format
          this is the placeholder for routines specific to derived classes"""
        return data

    def __set__(self, obj, val, idx_=None):
        """as a base method this assumes 'val' is in the format data comes __get__()
          overrides must handle 'txt' or format from __get__(), then call this method
          may also need to override storage format to reverse mapping from db in get"""
        # print('Updating', self.name)
        if idx_ is None:
            # if hasattr(obj,'idx_'):  #checking quack better than checking type
            #    idx_= obj.old_idx_
            if len(obj) > 1:
                raise ValueError('Cannot set multi row view')
            else:
                idx_ = 0

        if val != self.__get__(obj, None, idx_):
            # print(' it is changed?',val,self.__get__(obj),val!=self.__get__(obj))
            old_v = self.__get__(obj, None, idx_)
            v = self.storageFormat(val)

            src_nm = obj._source_list[self.src]
            storage_location = obj._dbRows[idx_].get(src_nm)
            for embed in self.src_dicts:
                if not embed in storage_location:
                    storage_location[embed] = {}
                storage_location = storage_location[embed]
            storage_location[self.name] = v
            if v != old_v:
                name = '.'.join(self.src_dicts + [self.name])
                obj.changes_[idx_][src_nm, name] = v

                if self.journal:
                    obj.log_changes_[idx_][src_nm, name] = v

    def setup(self, name, sampleRow, view):
        self.container_name = name
        if self.name is None:
            self.name = name
        src = self.src
        if not isinstance(src, int):
            try:
                self.src = view._source_list.index(self.src)
            except ValueError:
                self.src = 0
        self.src_name = view._source_list[self.src]
        self.src_dicts = view._sources[self.src_name].map_src(self.raw_src)
        # if self.src is None:
        #     self._value = ''  # code to establish src in the field
        # elif self.src == '':
        #     #if view.joins_:
        #     self.src = view.row_name_  # use default
        # else:
        #    self.src = True

        # for dbrow in obj.dbrows:  any loop should be for compound names
        # self.src=True  #2016-03 mongo simpler but no check for in row
        # elif view.joins_:
        #     dirs=[(dir(getattr(sampleRow,j)),j)
        #         for j in view.joins_]
        #     #print('the dirs',dirs)
        # else:
        #     dirs=[(dir(sampleRow),True)]
        # for the_dir,src in dirs:
        #     if name in the_dir:
        #         self.src=src #obj._dbRows
        #         break
        #     #if self.src:
        #     #    break
        # else:
        #     print('dir sam',dir(sampleRow))
        #     raise KeyError("View Field {}:{} not found in database".format(
        #             view.viewName_,name))
        # #if name=='id':
        #     #print('name the src',name,self.src,view.viewName_)
        # assert self.src != '','got though view setup with weird not found'
        # if self.src=='':
        #     print('got though setup with weird not found')
        if self.label is None:
            self.label = self.name
        if self.rowLabel:
            view.__class__.rowLabel_ = name

        return self.name

    @property
    def postID(self):
        return self.postPrefix + self.container_name

    def Type(self, obj):
        return str

    def default(self, *args):
        return self._default


##############################################
# below here fns not updated to fields yet


# ================================================================================================
NameVals = namedtuple('NameVals', 'names values')


class EnumField(BaseField):
    """  and enum has names and matching values
    these names & values are separate lists in the Fmt object
    see the format object for details.
    (the lists in future be stores as an Enum type the fmt Object builds

    The EnumField currently builds s new type with names and values
    matching the two lists, so the same names and values, but not same type
    as an external emum
    the lists from either an Enum

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = None
        self._Type = None

    def nameVals(self, obj):
        if not self.fmt.values:
            self.fmt.values = list(range(1, len(self.fmt.names) + 1))
        return NameVals(self.fmt.names, self.fmt.values)

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        if res is None:
            return None
        # print("ok did the get",res)
        # print('self defau',self.default(obj).value)
        if isinstance(self.default(obj).value, int):
            # print('default is int!')
            # if values are int ensure working with int
            # print('enum get int',res)
            res = int(res)

        try:
            # print('bout to get tyoe')
            Type = self.Type(obj)
            # print('got the type',Type)
            return Type(res)
        except ValueError:
            return self.default(obj)

    def Type(self, obj):
        """ a property to defer buiding type until actually needed"""
        # print('enum type')
        if not self._Type:
            # defer building type until needed
            nameVals = self.nameVals(obj)
            # print('namvale',nameVals,self.label)
            self._Type = Enum(self.label, zip(
                noBlanks(nameVals.names), nameVals.values))
        # print('at enum tr')
        # print('enum type return',self._Type,self.name)
        return self._Type

    def default(self, obj):
        if not self._default:
            Type = self.Type(obj)
            self._default = Type(self.nameVals(obj).values[0])
        return self._default

    @staticmethod
    def storageFormat(data):
        """ convert data from format returned by get, to raw database format """
        return data.value

    def __set__(self, obj, val, idx_=None):
        """as a base method this assumes 'val' is in the format data comes __get__()
          overides must handle 'txt' or format from __get__(), then call this method
          may also need to overide storage format to reverse mapping from db in get"""
        if isinstance(val, str):
            if isinstance(self.default(obj).value, int):
                print('isint')
                val = int(val)
            if val in self.Type(obj).__members__:
                val = self.Type(obj).__members__[val]  # case of name
            else:  # prefer to have value
                try:
                    val = self.Type(obj)(val)
                except ValueError as err:
                    default = self.fmt.default
                    if default == NotImplemented:
                        raise err
                    # import pdb; pdb.set_trace()

                    if default.name in self.Type(obj).__members__:
                        val = self.Type(obj).__members__[default.name]
                    else:
                        val = list(self.Type(obj).__members__.values())[0]
        super().__set__(obj, val, idx_)


class EnumForeignField(EnumField):
    """ the field is an index into another table
    the contents of the field is restricted to being one of the field
    values in the other table (a foreign key), or an index into the
    other table.
    If a filter is specified, then the field can only reference rows in the
    other table that match the filter.
    The field value is restricted to having the values contained in the 'values'
    field of the other table,
    .  or
    valid index (1...6 if there are six values) plus optionally 'zero' if 'zero text is supplied.

    The 'values' parameter either specifies the column in the other table containing the
    possible field values. If values = none then values are just indexes into the list.
    """

    def __init__(self, *args, zeroText=None, values=None, dispFields=(), session=None, saltFilter=None, sqfilter=None,
                 **kwargs):
        """load possible values from other table, question is when to reload!
        if 'values' is none, then values as range of possibles """
        self.zeroText = zeroText
        self.values = values
        if not isinstance(dispFields, (list, tuple)):
            raise TypeError('dispfields should be a list')
        self.dispFields = dispFields
        self.session = session
        self.sqfilter = sqfilter
        self.saltFilter = saltFilter

        super().__init__(*args, **kwargs)

    def nameVals(self, obj):
        # prrint('enff namevals',self.name,self.dispFields)
        firstDisp = self.dispFields[0]
        if not isinstance(firstDisp, str):
            raise TypeError("Dispfield for Emum Foreign not SQLA Field")
        # print('typeok')
        self.xtable = self.session.baseDB.db.get_collection(
            viewModelDB.pclass(firstDisp))  # table name
        filt = {}
        try:
            if self.saltFilter:
                filt = {self.saltFilter: obj.salt}
        except (AttributeError) as e:
            print('at catchall?', e.__doc__, e)
        # print (e.message)

        # session.query(self.xtable)
        rows = [r for r in self.xtable.find(filt)]

        # if self.sqfilter:
        #    rows = rows.filter(self.sqfilter())
        # rows = rows.all()
        # print("len rows nv",len(rows))

        values = self.values
        if '.' in values:
            # print('dir val',dir(values))
            values = viewModelDB.key(values)

        baseNms, baseVls = ([], []) if not self.zeroText else (
            [self.zeroText], [0])
        # print('bases',baseNms,baseVls)
        values = baseVls + [row[values] for row in rows
                            ] if values else [*range(1, len(rows) + 1)]

        names = baseNms + [', '.join([row[viewModelDB.key(dispField)]
                                      for dispField in self.dispFields])
                           for row in rows]
        Res = NameVals(values=values, names=names)
        # print('resnv',Res,Res.values,Res.names)
        return Res


# all below here not in current format yet

BaseCol = BaseField

# ======================================================================

YMD = namedtuple('YMD', 'y m d')


def strToDate(val):
    swap = False
    for char in ':/-':
        if char in val:
            swap = True
            res = YMD(*(val.split(char)))
            break
    else:
        # no separator found assum ddmmyy
        if len(val) == 4:  # expiry date?
            res = YMD('20' + val[2:], val[:2], 1)
        elif len(val) == 6:
            res = YMD('20' + val[4:], val[2:4], val[:2])
        elif len(val) == 8:
            res = YMD(val[4:], val[2:4], val[:2])
        else:
            raise ValueError(
                f'Cannot convert {val} to date: no separator found and bad length'
            )

    res = YMD(*(int(a) for a in res))
    if swap and res.y < 32:
        res = YMD(res.d, res.m, res.y)
    return datetime.datetime(*res)


def strToTime(val):
    swap = False
    for char in ':/-':
        if char in val:
            swap = True
            res = val.split(char)
            break
    else:
        # no separator found assum hhmmss
        if len(val) == 4:  # expiry date?
            res = val[:2], val[2:]
        elif len(val) == 6:
            res = val[:2], val[2:4], val[2]
        else:
            raise ValueError(
                'Cannot conver str to time: no separator found and bad lenght')
    return datetime.datetime(1, 1, 1, *[int(i) for i in res])


def strToDateTime(val):
    if ' ' in val:
        da, ti = val.split(' ', 1)
        da = strToDate(da)
        ti = strToTime(ti)
        return datetime.datetime.combine(da.date(), ti.time())
    return strToDate(val)  # no separator....just date?


class SimpleDateTimeField(BaseField):
    """ raw database format is 'datetime.date'
       get is ok- returns date time.date
       getstr coulc format better

       fmt['date'] sets how datetimes are converted to str
       which allows converting to date or time or any format
       fields are per  strftime().  Currently supported are
          d m Y H M S, as well as B(month name) and A(day name)
            use [-2:] to truncate Y or [-3:] to truncate B or A
            eg '{d}/{m}/{Y[-2:]}'
        when converting from string, the format examined first
        if fmt has a 'd' but no 'H' it is assumed to be a date only field
        if fmt has an 'H' but no 'd' it is assumed to be a time only field.
       """
    months = ('January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December')
    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        # print('datetype', type(res), res)
        return res

    @staticmethod
    def storageFormat(data):
        """ convert data from format returned by get, to raw database format """
        return data

    def __set__(self, obj, val, idx_=None, converter=strToDateTime):
        """as a base method this assumes 'val' is in the format data comes __get__()
          overides must handle 'txt' or format from __get__(), then call this method
          may also need to overide storage format to reverse mapping from db in get"""
        # print('Datefild',type(val),val)
        # import pdb; pdb.set_trace()
        if isinstance(val, datetime.datetime):
            pass  # nothing to do
        elif isinstance(val, datetime.date):
            val = datetime.dateime.combine(val, datetime.time(0, 0, 0))
        elif isinstance(val, datetime.time):
            val = datetime.dateime.combine(datetime.date(1, 1, 1), val)
        elif isinstance(val, str):
            val = converter(val)
        else:
            raise ValueError('Date must be str or datetime.date')
        super().__set__(obj, val, idx_)

    def toStr(self, value):
        if value is None: return ""

        date = self.fmt.date
        datestr = date if date else '{d:2}/{m:02}/{Y} {H}:{M:02}:{S:02}'
        dt = value  # self.__get__(self.viewObj)
        return datestr.format(**dict(d=dt.day, m=dt.month,
                                     Y=str(dt.year).rjust(4, '0'),
                                     H=dt.hour, M=dt.minute, S=dt.second,
                                     B=self.months[dt.month], A=self.days[dt.weekday()]))


class DateField(SimpleDateTimeField):
    """ set fmt[date] with a 'd' but without and 'H' (hour)field,
        and you have a date that does not expect the time on input
    """

    def __init__(self, *args, **kwargs):
        fmt = kwargs.get('fmt', {})
        if not 'date' in fmt:
            fmt['date'] = '{d:2}/{m:02}/{Y}'
            kwargs['fmt'] = fmt
        super().__init__(*args, **kwargs)

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        # print('datetype', type(res), res)
        return res.date() if res else res

    def __set__(self, obj, val, idx_=None):
        super().__set__(obj, val, idx_, strToDate)

    def toStr(self, value):
        date = self.fmt.date
        datestr = date if date else '{d:2}/{m:02}/{Y}'
        dt = value  # self.__get__(self.viewObj)
        if value is None: return ""
        return datestr.format(**dict(d=dt.day, m=dt.month,
                                     Y=str(dt.year).rjust(4, '0'),
                                     B=self.months[dt.month], A=self.days[dt.weekday()]))


# ======================================================================

class TimeField(SimpleDateTimeField):
    """ set fmt[date] with a 'd' but without and 'H' (hour)field,
        and you have a date that does not expect the time on input
    """

    def __init__(self, *args, **kwargs):
        fmt = kwargs.get('fmt', {})
        if not 'time' in fmt:
            fmt['time'] = '{H}:{M:02}:{S:02}'
            kwargs['fmt'] = fmt
        super().__init__(*args, **kwargs)

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        return res.time() if hasattr(res, 'time') else res

    def __set__(self, obj, val, idx_=None):
        super().__set__(obj, val, idx_, strToTime)

    def toStr(self, value):
        if value is None: return ""
        date = self.fmt.date
        tdate = date if date else ' {H}:{M:02}'
        dt = value  # self.__get__(self.viewObj)
        return tdate.format(**dict(H=dt.hour, M=dt.minute, S=dt.second))


# ============================================================================

class DateTimeField(BaseField):

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        if res is None:
            return None
        elif isinstance(res, datetime.datetime):
            return VMDateTime(res, timezone=None)

        tzdata = res.get("timezone")
        if tzdata:
            tzdata = VMTimezone(
                tzdata["offset"],
                tzdata.get("name", ""),
                tzdata.get("offsetDstComponent")
            )
        return VMDateTime(
            res["utcDateTime"],
            timezone=tzdata
        )

    def __set__(self, obj, val, idx_=None):
        if isinstance(val, VMDateTime):
            result = val.__json__(internal=True, forDatabase=True)
            super().__set__(obj, result, idx_)
        else:
            raise ValueError('Date must be a VMDateTime, else use SimpleDateTime Implementation')


# ============================================================================

class AmtCol(BaseCol):
    # currently no field for currency amounts?
    pass


class IdField(BaseField):
    """ see IdDAutoField for old sql mapping
    now maps field name 'id' to '_id' and that is all
    now only maped is no 'name' was asked for in init
    """

    def __get__(self, obj, objtype=None, idx=None):
        if self.name == 'id' and self.asked_name is None:
            # odict = obj._dbRows[obj.old_idx_]
            # fld=obj.fields_[self.name] - which name to set?
            # self.name = 'sqlid' if 'sqlid' in odict else '_id'
            self.name = '_id'
        res = super().__get__(obj, objtype, idx)
        # print('int get',type(res),res) does not work for 'None' result
        return res

    def __set__(self, obj, val, idx_=None):
        if not isinstance(val, ObjectId):
            val = ObjectId(val)
        super().__set__(obj, val, idx_)

    @staticmethod
    def id_dict(id):
        if isinstance(id, int):
            return dict(sqlid=id)
        else:
            return dict(_id=id)


class IdAutoField(BaseField):
    """ - previously was IdField with the idea that it can
    work to help migration between sqlid and _id.  for get,
    return sqlid if present, otherwise return _id.
    for set??, set _id if type is IdObject, otherwise set sqlid

    does not matter what variable is called or name is set
    field will use 'sqlid' data if present, otherwise '_id'
    """

    def __get__(self, obj, objtype=None, idx=None):
        if True:  # self.name == 'id':
            local_idx = 0 if idx is None else idx
            # import pdb; pdb.set_trace()
            odict = obj._dbRows[local_idx][obj.row_name_]
            # fld=obj.fields_[self.name] - which name to set?
            self.name = 'sqlid' if 'sqlid' in odict else '_id'
        res = super().__get__(obj, objtype, idx)
        # print('int get',type(res),res) does not work for 'None' result
        return res

    @staticmethod
    def id_dict(id):
        if isinstance(id, int):
            return dict(sqlid=id)
        else:
            return dict(_id=id)


# ---------------------

class IntField(BaseField):
    """ raw database format is ???
       get is ok- returns int
       """

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        # print('int get',type(res),res) does not work for 'None' result
        return res

    @staticmethod
    def storageFormat(data):
        """ convert data from format returned by get, to raw database format """
        return data

    def __set__(self, obj, val, idx_=None):
        """as a base method this assumes 'val' is in the format data comes __get__()
          overides must handle 'txt' or format from __get__(), then call this method
          may also need to overide storage format to reverse mapping from db in get"""
        # print('IntField',type(val),val)
        try:
            val = int(val)
        except ValueError:
            raise ValueError(f"Failed to convert '{val}' to int for field '{self.name}' in view '{obj}'")
        super().__set__(obj, val, idx_)


# =========================== most common case no binary
class TxtField(BaseField):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        return res if res is None else str(res)

    def Type(self, obj):
        return str

    def default(self, obj):
        res = super().default(obj)
        return '' if res == None else res


# =========================== most common case no binary
class ObjDictField(BaseField):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        # print('int get',type(res),res) does not work for 'None' result
        return ObjDict(res) if res is not None else ObjDict()

    def __set__(self, obj, val, idx_=None):
        if isinstance(val, Struct):
            val = dict(val.items())
        super().__set__(obj, val, idx_)

    def Type(self, obj):
        return ObjDict

    def default(self, obj):
        res = super().default(obj)
        return ObjDict() if res == None else res


# =========================== most common case no binary
class DecField(BaseField):
    """
    Different countries have decimals places between 0 and 3,
    perhaps we should store up to 3? This supports all currencies.

    Or is it necessary to know the country when storing monetary values,
    and use the knowledge to pass in number of places for that country?
    """

    def __init__(self, places: str, intFactor: int = 1, *args, **kwargs):
        """
        :param places: A string matching the desired format of the decimal, as required by decimal.Decimal
            e.g 0.00 for 2 decimal places.
        :param intFactor: If an integer value is found when reading out of the database (e.g legacy data)
            it is divided by this factor to produce the decimal. I.e if converting cents to dollars apply
            a factor of 100 (and places of 0.00).
        """
        super().__init__(*args, **kwargs)
        self.places = places
        self.intFactor = intFactor

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        if res is None and self.default(obj) is None:
            return None
        if isinstance(res, Decimal128):
            res = res.to_decimal()
        elif isinstance(res, int):
            res = Decimal(res) / self.intFactor
        return res.quantize(Decimal(self.places), rounding=ROUND_HALF_UP)

    @staticmethod
    def storageFormat(data: Decimal):
        return Decimal128(data)

    def json_value(self, view, idx=None):
        """For JSON we want to store the Decimal as a string, because floats are not okay."""
        return str(self.__get__(view, idx=idx))


class BoolField(BaseField):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def __get__(self, obj, objtype=None, idx=None):
        res = super().__get__(obj, objtype, idx)
        return False if res is None else res


# ==================================================================================
class TxtListField(BaseField):
    """methods here work for top level item - which is a list
        methods to work with elements to be added
    """

    def Type(self, obj):
        return list

    def default(self, obj):
        res = super().default(obj)
        return [] if res == None else res

    # def __get__(self, obj, objtype=None):
    #     res = super().__get__(obj,objtype)
    #     #res = ",".join(res)
    #     return res

    @staticmethod
    def toStr(val):  # called by .strValue for use in forms etc
        return ", ".join(val)

    @staticmethod
    def storageFormat(data):
        """ convert data from format returned by get, to raw database format """
        if isinstance(data, str):
            data.replace(', ', ',')  # strip padding following ','
            return data.split(",")
        return data

    def __xxset__(self, obj, val, idx_):  # on hold in case we need it
        """as a base method this assumes 'val' is in the format data comes __get__()
          overides must handle 'txt' or format from __get__(), then call this method
          may also need to overide storage format to reverse mapping from db in get"""
        print('IntField', type(val), val)
        try:
            val = int(val)
        except ValueError:
            raise ValueError('Int value could not convert')
        super().__set__(obj, val, idx_)


class SetField(BaseField):
    """
    For when you want an Array with no repeated values stored in the mongo.

    Turns out it's tricky to manage storing as a list in database, converting to
    json as a list, and using value in code as a set. Json does not support sets,
    neither does mongodb. Until a better solution is found (TODO), the only use of the `set`
    type will be for removing repeated values in a list, then converting back to a list.
    It's a shame we can't get a set to use in python code, but, I tried... a little.
    """

    def __set__(self, obj, val, idx_=None):
        """Ensure data is essentially a set, even though it is not actually a set."""
        assert isinstance(val, (list, set)), f"Attempt to save value that is not a list or set, got {type(val)}"
        ensure_set = set(val)  # remove duplicate values if present
        super().__set__(obj, list(ensure_set), idx_)

    def Type(self, obj=None):
        return list

    def default(self, obj=None):
        res = super().default(obj)
        return list() if res is None else res


class BaseListField(BaseField):

    def default(self, obj):
        res = super().default(obj)
        return [] if res is None else res


class ObjListField(BaseListField):
    """methods here work for top level item - which is a list
        methods to work with elements to be added
    """

    @staticmethod  # TODO upgrade to handle insertion key
    def idxKey(input: Union[int, str]) -> str:
        if isinstance(input, str):
            lst = input.split(".")
        else:
            lst = [input]
        return ".".join([f"{int(i):04d}" for i in lst])

    @staticmethod  # TODO upgrade to handle insertion keys
    def idxKeyVal(input: Union[int, str]) -> int:
        if isinstance(input, str) and ("." in input):
            return int(input.split(".")[0]) + 1
        return int(input)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fmt.displayType = DisplayType.ObjectList.value

    def __set__(self, obj, val, idx_=None):
        """ currently updates write full value to database rather than just
        the actual updates.  At some time could move to direct change to held
        value and write changes in a manner can be used by db code to
        change individual fields

        updates come in the from of a map of values to be updated,
        keyed by the index.  An 'updated value' of None is use to signal
        entry is to be deleted

        allows for insertion by "5.1" is between 5 and 6, and 5.1.1 is
        between 5.1 and 5.2.  Current uses input order to determine where
        inserts actually are added, so order of input map is currently
        significant, but can move to sorted order at any point

        """
        if isinstance(val, dict):  # we have an updates dict
            buildNewVal = {self.idxKey(i): v for i, v in enumerate(self.__get__(obj, ObjListField, idx_))}
            for k, newvalsmap in val.items():
                key = self.idxKey(k)  # we still need to handle the case for a viewRow being passed in
                if key not in buildNewVal:  # insert
                    buildNewVal[key] = self.elementObjType(**newvalsmap)
                elif newvalsmap is None:  # delete
                    del buildNewVal[key]
                else:  # update
                    for fld, v in newvalsmap.items():
                        setattr(buildNewVal[key], fld, v)

            val = list(buildNewVal.values())
        super().__set__(obj, val, idx_)

    def __get__(self, obj, objtype=None, idx=None):
        """ When returning an ObjListField we need information from both
         the objtype and the elementObjectView.


         - elementObjectView is a property of a view that describes
            any nested view that could be inside the field.

        """
        res = super().__get__(obj, objtype, idx)
        if self.elementObjType is None:
            return res
        return [self.elementObjType(**i) for i in res]  # ObjDict(res) if res is not None else ObjDict()

    def Type(self, obj):
        return ObjDict()

    # def __get__(self, obj, objtype=None):
    #     res = super().__get__(obj,objtype)
    #     #res = ",".join(res)
    #     return res

    @staticmethod
    def toStr(val):  # called by .strValue for use in forms etc
        return unParse(val)

    @staticmethod
    def storageFormat(data):
        """ convert data from format returned by get, to raw database format """
        if isinstance(data, dict):  # this is an update map
            raise TypeError("map should be excluded by set method")
            return data
        if isinstance(data, str):
            try:

                return json.loads(data)
            # return combiParse(data)
            except:
                return []

        def asDictIfObj(obj):
            return asdict(obj) if hasattr(obj, "__dataclass_fields__") else obj

        if isinstance(data, list):
            return [asDictIfObj(i) for i in data]

        return data


class BaseArrCol(BaseCol):
    """ either single dbcol arrarys using split or multi col arrays
    minElts is the minimun size, maxElts is the maximum allowed

    """


# def preInit():
#   if rowLayout=='-xx-' and label=='':rowLayout='--x-'
#   BaseCol.__init__(self,name=name,label=label,rowLayout=rowLayout,misc=misc)


class NumArrCol(BaseArrCol):
    """ either single dbcol arrarys using split or multi col arrays
    minElts is the minimun size, maxElts is the maximum allowed

    """


class TxtArrCol(BaseArrCol):
    """ either single dbcol arrarys using split or multi col arrays
    minElts is the minimun size, maxElts is the maximum allowed

    """


# def preInit():
#   if rowLayout=='-xx-' and label=='':rowLayout='--x-'
#   BaseCol.__init__(self,name=name,label=label,rowLayout=rowLayout,misc=misc)
# def iterator(self,width,tbl):
#   return self.iteratorBase(len(self.thevals(tbl)),width)
# def thevals(self,tbl):
# debecho('valsec',tbl.numArr(self.name
#       ,defVal(self.misc,'minElts',0),defVal(self.misc,'maxElts',100)),self,dbTable.data)
#   return tbl.numArr(self.name
#           ,defVal(self.misc,'minElts',0),defVal(self.misc,'maxElts',100))

# def editDrawN(self,key,val,table,idx=None,edit=True,fmt=None):
# debecho('vvvVv',repr(self.thevals),self.thevals(),self,table.data)
#   return self.baseDraw(key+str(idx),self.thevals(table)[idx])


# ==========================================================================
PosnField = BaseField


class BoolFlagCol(PosnField):
    pass  # need a bool flag field than can display as a checkbox


# =============================================================


class FieldTypes:
    Enum = EnumField
    Txt = TxtField
    Int = IntField
