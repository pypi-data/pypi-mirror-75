# ViewModels

## [Introduction](#introduction)

## [Uses](#uses)

- [Interface to Provide Access to Database and
Abstraction](#interface-to-provide-access-to-database-and-abstraction).  
- [Repository for All Information Relating to Data: Schema and
Beyond](#repository-for-all-information-relating-to-data-schema-and-beyond).  
- [Increasing Range of Types Available to
Applications](#increasing-range-of-types-available-to-applications).  
- [An Explanation of ViewModel Uses](#an-explanation-of-viewmodel-uses).

## [Background](#background)

- [History](#history).  
- [Data Tables/Collections and Data Views](#data-tablescollections-and-data-views).

## [Instructions](#instructions)

- [Simple Example](#simple-example).  
- [Describing a Table/Collection With
ViewFields](#describing-a-tablecollection-with-viewfields).  
- [Using 'ViewField' Derived
Classes](#using-viewfield-derived-classes).  
- ['ViewModel' Interface](#viewmodel-interface).  
- ['ViewRow': The Row Interface](#viewrow-the-row-interface).  
- [Extended ViewModel Declarations and
Instancing](#extended-viewmodel-declarations-and-instancing).  
- [models_ and _sources](#models_-and-_sources).  
- [Setting Field Source](#setting-field-source).  
- ['ViewField' Interface](#viewfield-interface).  
- [Building HTML Forms](#building-html-forms).  
- [Updating from HTML Forms](#updating-from-html-forms).  
- [How to Load Test DB Data From JSON Files for
Testing](#how-to-load-test-db-data-from-json-files-for-testing).

## [Data Relationships and Joins](#data-relationships-and-joins)

- [Data Relationship Types](#data-relationship-types).  
- [Joins](#joins).  
- [Inserts With Joins](#inserts-with-joins).

## [How It Works](#how-it-works)

- [The Rows Structure](#the-rows-structure).

## Introduction

Viewmodels provides for declaring a [data dictionary](https://en.wikipedia.org/wiki/Data_dictionary): a full definitions for the data processed by the application.

While a dataclass provides a declaration of the _type_ of each element of
the class, a data dictionary provides for storing all details about each element, going beyond just type.

This information can be used by utilities to display and/or edit the data, as
well as providing information for storing and retrieving the data from the database.

A data model describes additional details beyond type that are required from loading and
storing information to a database.

Viewmodel goes beyond details needs from storage and adds details needed from display/edit.

The viewmodel definition describes all attributes
of data, those used for storage, but also those uses for displaying the
data and generating on screen views, in addition to attributes of
data describing how the data is stored in a database.

An [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping) is a key
part of the model. The current implementation is with MongoDB for the
bottle framework. Generally, the concept is to allow flexibility and
independence from the constraints of the underlying DB. ViewModels
provide for the model and also support the view code, and simplifies
both model and view code. Data is described through a set of
'ViewModels'. A view model contains data description of one or more
collections or tables, and is used to bring windows of data (either a
single row, a specific collection of rows, and in some cases possible
the entire collection/table into memory for reading and manipulation. So
in addtion to all attributes of the fields, the view contains rules on
how to select windows into the table with selected rows. As an example,
a 'View' could represent rows of a collection/table within a database
that meet defined criteria, and represents a window or subset of the
specific collection/table. Note that depending on criteria, a view could
be empty, as no entries in the collection meet the specified criteria.
An empty view does not imply the collection is empty. Changes to the
view, including insertions and deletions are automatically propagated to
the database, but changes to the database made using other views or
other access to the database DO NOT currently propagate to the view. If
the database is updated by other views, or other code, then a new
ViewModel object should be instanced again to reload the view.

## Uses

### Interface to Provide Access to Database and Abstraction

To access a Mongo collection directly through pymongo could not be much
more straightforward, but misses features of view model and does not
provide:

- abstraction between code and database;  
- types beyond those covered in the BSON typeset;  
- joins, and joins with 'lazy' execution;  
- a record of the schema in use;  
- support for a web maintenance interface to the database;  
- web interface supports security and templates for full application.

All these advantages are provided by using ViewModel. However, there are
times when none of these justifies an additional layer. The more complex
the collection, the higher the amount of code, generally the higher the
value of using ViewModels.

#### Abstraction Between Code and Database

Databases migrate. Our main project database started with direct SQL,
then SQLAlchemy, then MongoDB. Abstraction assists with migrations as
the code is written to abstract API, leaving the application able to
remain unchanged during migration, and only internet interface to the
new system need change. In reality, some changes also require a change
of API, but even in those cases, application changes are reduced. The
current main application system uses MongoDB, and the direct pymongo
interface can be perfect for simple access, but misses the DSL
methodolgy advantages of thinking at a higher level, so is best
restricted to low level code. A rewrite would be needed to change that
low level code, which is ok if code is small, so it is not a significant
barrier for small, uncomplicated cases. However, more complex code cases
are another matter!

### Repository for *All* Information Relating to Data: Schema and Beyond

A single repository for all information about data. Information on both
storage as well as information used for display, all in one place.

Data descriptions can be simple tables/collections or views which
comprise multiple tables which are effectively joined.

The data description provided by ViewModel library can include extended
types described at a layer of abstraction separate from the storage
specification, allowing the application layer free of the mechanics.

ViewModel was created for SQL based applications, but then evolved to
also work with NoSQL MongoDB applications.

NoSql collections (or tables) can effectively be irregular with
different fields present potentially in every entry. While with SQL,
just examining a row can give a reasonable view of that schema, but this
can be less clear from NoSql. Even with SQL, the schema recorded is
restricted to what the database engine requires, and lacks richer
descriptions of the data and rules not implemented by the database, but
a repository for a schema becomes even more essential with NoSQL.

### Increasing Range of Types Available to Applications

ViewModel provides a mapping between the data in the database and the
data seen by the application. Far more descriptive types and more
complex types can be used by the application with the mapping between
these types and the underlying storage format handled by the ViewModel.

### An Explanation of ViewModel Uses

Every window has a view even if it is just a view of a brick wall. In
the case of ViewModel, each view has a window into the database at
initialisation. Each window consists of an arbitrary number of rows. You
can send the whole window, i.e. contents and attributes to the HTML
browser in JSON format. The rules for how this JSON is shown in the
browser is typically defined in the view.

## Background

- [History](#history).  
- [Data Tables/Collections and Data
Views](#data-tablescollections-and-data-views).

### History

The original Salt project development worked with SQL at a time when the
SQLAlchemy project was still in early stages. So Salt developed its
layer to abstract to the database in 2007 around the same time as
SQLAlchemy was developed. Both the salt 'DataModel' and SQLAlchemy
libraries developed specific advantages, but as a popular open sourced
project, SQLAlchemy became the more mature product. In 2015 the Salt
project chose to replace the internal 'DataModel' library with the
SQLAlchemy, due to wider use and greater development of the open source
project, but then found several key features of 'DataModel' were missing
from SQLAlchemy. The solution was a new library 'ViewModel', which acted
as an abstraction layer between SQLAlchemy and the application. The name
'ViewModel' came from the fact that the main elements present in
'DataModel' that were missing from SQLAlchemy were data extended data
schema information that was also useful in providing data description to
views.

The next step brought the current 'ViewModel', by transforming that
library to become an interface between pymongo and the application.

### Concepts

There are four basic concepts:

- a container of objects - a '[view](#view---the-container)'
- an 'ViewRow' or '[ViewObject](#viewobject)'
- a ViewField
- a set of 'sources'

#### View - the container

Currently, instancing a 'ViewModel' returns a 'view' - container of objects.
The container behaves as a List of the ViewObject(s).

In the future, it is planned containers will
also replicate the functionality of a Dictionary/Map, but as, like a database, any
field can act as 'key', this may require indexing with a dictionary/map.

Every ViewObject has a 'container', even if there is only a single ViewObject
within the container.

Currently, containers with a single object can be used as that viewObject,
however it is planned that this functionality be deprecated  

#### ViewObject

##### Also known as a ViewRow

indexing into a 'View' ( e.g. view[0]) returns a view object.

 reserved properties of a viewObject

- view_
- fields_  (to be added at a future time)

#### ViewField

Every property of a viewobject is a 'ViewField'. The goal of each viewfield
is firstly, as every property, enable 'get' and 'set' operations with the regular syntax.
Beyond the standard get and set, each ViewField as a field object containing an extensive
set of attributes of the that 'ViewField' (or 'property').

The 'fields_' attribute of the ViewObject contains the map of all ViewField style properties
of that object.  Note that since

    <viewObject>.<viewField>

will always return the value of the viewField, by calling the setter (unless in an assignment,
where the getter would be called) the full set of properties of the ViewField itself can
only be accessed via this 'fields_' map of all the ViewFields.

#### Sources

The sources for View .... to be added

### Data Tables/Collections and Data Views

The ViewModel package focuses on preparing data for views. How is the
data in a table/collection to be viewed? For example, consider a
'Products' table or collection, where products may be viewed:

- individually by product code;  
- as a list of products by product group, or by brand;  
- as a list through a custom search.

These become the views of the data from the database. It is never
relevant to retrieve the entire table/collection for the products as if
processing the entire table; each document will be processed in
sequence. In contrast, there may be other table/collections with either
a single or small fixed number of rows/collections the entire
table/collection may constitute a view.

Further, the product table could have a join to a 'pack sizes'
table/collection and for some views, these are also part of the view.

The main concept is that each table has a set of relevant views of the
table/collection for various uses. The ViewModel specifies not just the
schema of the table/collection, but the actual views of the
table/collection.

## Instructions

- [Simple Example](#simple-example).  
- [Describing a Table/Collection With
ViewFields](#describing-a-tablecollection-with-viewfields).  
- [Using 'ViewField' Derived
Classes](#using-viewfield-derived-classes).  
- [Extended ViewModel Declarations and
Instancing](#extended-viewmodel-declarations-and-instancing).  
- [Building HTML Forms](#building-html-forms).  
- [Updating from HTML Forms](#updating-from-html-forms).

### Simple Example

This example is given in advance the instructions or details on how the
components of the example work. The idea is: read the example to gain an
overview, then see more details to understand more and return to this
example.

#### The Simple Database

Consider a database with a table of students. Rows (or Documents)
have:

- an id;  
- a name;  
- a course;  
- year number within the course.

#### Code to Describe Table Find an Entry

A class for the student data is declared, inheriting from 'ViewModel'.

    class StudentView(ViewModel):

Attributes or 'fields' are declared at the class level, with 'ViewFields' assigned for each
 (the id, name, course, year number).  e.g.

    id = IdField()
    name = TxtField()
    course = IntField()
    #  .... field definitions may  continue

The view can be given an optional 'viewName_' to be displayed to system users.
The view name will default to the class name if no view name is supplied.
Note that all attributes of the class that are not 'fields' are given a trailing underscore
to reduce the changes of them colliding with a field name.

     viewName_ = "Students"

Full working code follows:

    from ViewModel import ViewModel, IdField, TxtField, IntField
    import pymongo
    
    database = pymongo.MongoClient(dbserver).get_database("example")
    
    class StudentView(ViewModel):
        viewName_ = "Students"
        models_ = database.Students
        
        id = IdField()
        name = TxtField()
        course = IntField()
        #  .... field definitions may  continue
    
    student = StudentView({}, models=database.Students)
    # could have used 'models_' within class to avoid needing 'models' parameter
    # for the init
    #   {} empty dictionary to ensure an empty view, not needed if the database
    #   does not even exist yet, as with a new database, initial view will always
    #   be an empty view
    
    if len(student) > 0:
        print("oh no, we already have data somehow!")
    
    students.insert_() # add an empty entry to our view
    
    with student:  # use 'with', so changes written at the end of 'with'
        student.name = 'Fred'
    
    # ok ... now we have a 'Student' table with one entry

#### Code to Read and Update Our Entry

A key concept is that while the class for the view describes a table,
set of tables or joined tables (or collections in Mongo speak), an
instance of a ViewModel is the set of data or a window of the tables.
Instancing the view reads from the database in most straightforward
cases, although in more complicated cases the data may be read from the
database when accessed, the view instance logically includes all data
from a 'read' operation:

    # same class definition and imports as above
    
    student = StudentView({'name': 'Fred'},model = database.Students)
    # would save if we could have 'models_' in class definition!
    
    if not student.course:
        with student:
            student.course_year = 2
            student.course = 'Computing'

#### Multiple Entry Views

So far our view has only one entry. An instance of our view is a window
viewing part of the database. This window can be a single row/collection
or a logical group of entries(from rows/collections), and for small
tables, may even be the entire table/collection. The code that follows
adds another entry, so the sample has more than one entry, then works
with a multi-entry view:

    StudentView.models_ = database.Students
    # modify class, add 'models_' as an attribute,
    # this saves specifying 'models_' each time instancing StudentView

    student = StudentView()
    # no dictionary, this gives an empty view (not multi entry yet)

    student.insert_()
    with student:  # adding a second student
        student.name = 'Jane'
        student.course = "Computing"
        student.course_year = 2

    # now our multi entry view for all year 2 Students
    students = StudentView({'course_year':2})

    for student in students:
        print(student.name)

Note how multi-entry view instances can be treated as lists. In fact,
single entry views can also be treated as a list, however for
convenience view properties for single entry views also allow direct
access as one entry. For a single entry view 'student':

    student.name == student[0].name

#### Example Summary

The example bypasses the power of ViewModels to show you a simple
introduction. A fundamental concept is that classes describe a table (or
collection or set/join of tables). An *instance* of a ViewModel is one
set specific subset, a set of data from a table (or set/join of multiple
tables).

### Describing a Table/Collection With ViewFields

When creating a class derived from a ViewModel, add class attributes
which are 'ViewFields' for each field in the table or collection.

The example ([Simple Example](#simple-example). ) uses several types of
view fields. However each 'ViewField' can contain information well
beyond the type of data. An alternative name, a short and long
description, formatting and other display defaults, value constraints
and many other settings, as well as a 'default value' set with the
'value=' init parameter. Note that when a new row is inserted into a
view, no fields are set to their default value, and instead all fields,
even those with default values, remain 'unset'. However 'unset' fields
return their default value when accessed. This means that if a ViewModel
can have a new field (or even merely a new default value for an existing
field) added after several rows are already in the database. Existing
records will behave automatically return the 'default value' even though
they were saved prior to the default being defined. This makes
ViewModels stable and safe for software updates which add new fields
without the need to update the database itself.

In the example, only the 'value' attribute of the "name" ViewField is
accessed. 'student.name' does not access the ViewField, but instead
returns "value" attribute of the "name" ViewField. To access the actual
ViewField (or IntField, TextField etc) and have access to these other
attributes use 'student["name"]' thus:

    student.name == student["name"].value

### Using 'ViewField' Derived Classes

All 'fields' are sub-classed from ViewField and represent individual
data types. Each field contains the following properties:

- `name`: set explicitly, or defaulting to the property name;  
- `label`: set explicitly but defaulting to the name;  
- `hint`: defaults to '' for display;  
- `value`: returns value when a field is an attribute of a row
object.

### 'ViewModel' Interface

The 'ViewModel' provides a base class defines a database
table/collection, and each instance of a ViewModel. Note all system
properties and methods start of end with underscore to avoid name
collision with database field names.

#### ViewModel Interface Methods

- `insert_()`  
- `labelsList_()`  
- `update_()`  
- `<iterate> for row in <ViewModel instance>`  
- `<index> <ViewModel instance>[row]`

#### ViewModel Interface Properties

- `viewName_`  
- `models_`  
- `dbModels_`

#### ViewModel Details

The `insert_()` method adds an empty new
row (ViewRow instance) to the current ViewModel instance. At the next
`update_()`, an actual database
document/row will be created, provided some values have been set in the
new row.

Note that a record is currently marked for insert if there is no '_id',
and otherwise for update. So if a record created by
`insert_()` has an '_id' added, currently
this record will then allow changes by update, without reading the
record first.

The `labelsList_()` method returns a list
of the labels from the rows of the current ViewModel instance. It
computes the list of labels by, first, looking for the row_label
attribute if that fails then it will search through all possible fields
for anything called rowLabel and then set row_label to the
corresponding value of rowLabel. If rowLabel is not declared as True in
the view definition, the rowLabel will default to 'no labels'.

The `update_()` method is called
automatically at end of a 'with <ViewModel instance>' statement
(python keyword 'with'), or can be called directly, to update the actual
database with values changed by assignments through '<ViewModel
Instance>.<fieldname> = statements'.

`viewName_` is merely a title for the view
for display purposes.

`models_` is a list of the names of
tables, or actual database tables objects used by the view

`dbModels_` is a dictionary of database
table objects used by the view, with the model names as keys.

Note: all 'ViewModel' instances with one row implements all of the
ViewRow interfaces in addition to the methods and properties discussed.
'ViewModel' instances with more than one row will raise errors if the
'ViewRow' interface as it is ambiguous which row/document to use.

### 'ViewRow': The Row Interface

ViewRow objects and ViewModel objects both implement the 'ViewRow'
interface.

Where a ViewModel contains one logical row, the operations can be
performed on the ViewModel, which also supports this interface for
single row instances.

#### ViewRow Interface Methods

- `<iterate>: for field in <ViewRow instance>`  
- `loop_(case=<case>): for field in a <ViewRow instance>`  
- `<index>: <ViewRow instance>[<fieldname>]`  
- `<attribute> <ViewRow instance>.field_name`

#### ViewRow Interface Properties

- `fields_`  
- `view_`  
- `label_`  
- `idx_`

#### ViewRow Details

The statement: `for <field> in <ViewRow
instance>:` provides for using a 'for loop' to iterate over the
fields in a row of a viewfield.

Note that this iteration can be for building a view, and as such the
iteration allows for selecting which fields are included in the view.
When fields are declared (see ['ViewField'
Interface](#viewfield-interface)), they can set a 'case' where they are
applicable for views. For example, this can be in a view, on an edit
panel, or the field is for calculation purposes and part of the model,
but not revealed in a view.

Using `<ViewRow instance>[<field
name>]` (or indexing), retrieves the instance of the ViewField
named. For example:

    student['name'].value = 'Jane'
    print(student['name'].value)
    
    # is equivalent to
    student.name = 'Jane'
    print(student.name)
    # but the point of using indexing to access other field attributes
    assert student['name'].wide == 16 # check the name field is 16 characters wide

`fields_` returns a 'ViewRow' is a logical
entry in a ViewModel. Consider the example ( [Simple
Example](#simple-example). ). The line of code:

    student.name = 'Fred'

Is using the ViewRow set attribute interface to set the 'value' of the
'name' field within the 'row' created by the
`insert_()` method.

In this example, because the 'student' ViewModel has only one row, the
'name' field can be accessed directly in the ViewModel. However, if
there were, for example, three students in the view, which 'name' is to
be changed? As stated previously, ViewModel objects support the ViewRow
interface but report an error if there is more then one row.

There are two main ways to access 'ViewRow' objects (apart from simple
treating the ViewModel as also a ViewRow, which only works for single
row views). If our 'student' ViewModel contains three students, there
will be a row for each student, and these 'rows' could be accessed as:

    students = StudentView({})
    assert len(students) == 3  # check we have 3 students
    student_0 = students[0]
    student_2 = students[2]
    for student in students:
        <print details from student>

From the ViewModel, indexing or iterating can access the ViewRows.

This interface allows retrieving and setting data 'fields' or ViewField
entries by name as object attributes. All internal attributes of ViewRow
have either a trailing underscore to avoid name collisions with field
names of the database, or a leading underscore to indicate that these
attributes should not be accessed externally of the ViewRow or
ViewModel.

Provided database fields have no leading or trailing underscore, they
will not collide with the names of internal workings of these classes.

### Extended ViewModel Declarations and Instancing

#### getRows

The `__init__()` method calls
`getRows_` which is designed for
subclassing. getRows_ can return either:

1. An empty list (for an empty view);
2. The raw data from a find (where all data is from a single source and
    in this case the 'source' parameter to the class is used to build
    `dbRows_` automatically;
3. A list of dicts (for the rows, dict with one entry for each
    'source', and that entry itself being a dictionary of the fields of
    that 'source'.

Previous versions of the library required (2) to be instead a list of
ObjDicts. This is no longer supported. The statement:

    # below statement no longer will produce functioning code
    # remove it
    result = [ObjDict(res) for res in result]

... would convert the result of a find into a list of ObjDicts, where
each ObjDict is a row. What is now required is such data is embedded in
a 'source' dictionary. A replacement for the above line, (which is not
need as the standard class init method will make this adjustment
automatically), would be the line:

    result = [Objdict(((row,res),)) for res in self._dbRows]

### `models_` and `_sources`

As the names suggest, 'models' is for 'public' use (or in this case
declaration) and `_sources` is 'private'.
The data to construct `_sources` is
provided in but the _sources class variable, or the 'sources' parameter
to a viewmodel constructor.

If sources (either `_sources` class
variable or sources parameter), is not a list then internal logic treats
it as a one element list: [sources], so even if only one value is
provided, consider that value a one element list.

Each value in the 'models' list can be one of the legacy values of
'None' or a MongoDB collection, or (preferred) an object instanced using
a class based on the DBSource class. Currently, four such classes exist:
DBNoSource; DBVMSource; DBMongoSource and DBMongoEmbedSource.

#### DBNoSource

When generating a sources list from 'models', a value of None is used as
a legacy alternative to creating a DBNoSource object, but the preferred
way is an explicit object. Fields with a 'NoSource', as the class name
suggests, have no database source and thus no storage and as such are
temporary values only. Since a collection or table name is not part of a
'NoSource' object, the source name must be described explicitly or will
be '__None__'. Note that at the time of writing, any string entry in
a source list that beginning with an underscore will be taken as a
DBNoSource object with the name of that string.

#### DBVMSource

A DBVMSource is used for data that exists within another ViewModel. This
allows nested views. This time, this is merely a provision for the
future.

#### DBMongoSource

The source used for mongo collections, and instanced from legacy MongoDB
collections, as well as from the preferred explicit instances. The
'name' of a DBMongoSource is the name of the collection. So the
collection 'students' would have the string name 'students'.

#### DBMongoEmbedSource

These are used when the table is embedded within a document inside a
mongo collection. The source is specified as
"<collection>.<object-list_name>", where the object list name is
the object containing the entire embedded collection as a list of
objects.

#### Declaring 'models_'

Models (`models_`) may be declared as a
class variable, or passed as a parameter ('models') to the
`__init__()` method for the ViewModel.

In either case, the value is a list of each source, with each entry of
one of the 'DBSource' types listed above, or an application specific
class derived from DBSource. Note that while models are in theory a
list, the code will convert a single entry into a list, eliminating the
need to have a single entry as a list.

### Setting Field Source

Any field can belong to any 'source', as described above. The first
'source' for a view is considered the default source, so if using the
first source, or 'default source', it is possible to omit the 'src='
parameter. Any field which is from a view other than the first view
needs to specify the view by name with the 'src' parameter:

    src=<name of the source as a string>

For an embedded source, the name will use 'dot notation'.

Further, a field may be embedded in another object. The name of the
object should also be a specified through source. Examples:

    models_ = DBMongoSource('students'), DBMongoSource('courses')
    
    num1 = IntField()  # no 'src' specified -- field is in default 'students' collection
    num2 = IntField(src='courses')  # field is in 'courses' table/collection
    num3 = IntField(src='courses.scores') # field is in scores object in courses table
    num4 = IntField(src='students.scores') # field is in scores object in students table
    num5 = IntField(src='.scores') # alternative using default notation, same location as 'num4'

### 'ViewField' Interface

#### Getting and Setting 'Row Member' Values

To be added

### Building HTML Forms

To be added

### Updating from HTML Forms

To be added

### How to Load Test DB Data From JSON Files for Testing

Loading tables (collections) for testing is made easier by using the
JSONLoad class provided in ViewModel. The class allows you to load
previously downloaded JSON tables (Mongo collections -- just make sure
they are created as JSON array types -- see [How to Export Mongo
Databases/Collections to
JSON](https://saltnz.atlassian.net/wiki/spaces/DEV/pages/89456642/How+to+Export+Mongo+Databases+Collections+to+JSON)
for more about this). The JSONLoad class is in "json_load.py".

The JSONLoad class sets the following defaults:

- The default JSONLoad location is "dumped_data". It is located
    at the same level as the test file (test_file.py) that is using the JSONLoad class (see below):

        project_root/
        |-- ...
        |-- tests/
            |-- dumped_data/
            |-- test_file.py/
        |-- ...

    To override the default location, import
    "DEFAULT_DUMP_DATA_FOLDER_NAME" and set it to what you want it
    to be.

- The default host name & port number is:

    host_name = localhost
    port = 271017

- The default DB name is '' by design and is a required parameter i.e.
db_name defaults to '' so must be passed in when you use JSONLoad:

    JSONLoad(db_name="MY_TEST_DB_NAME")

To load JSON data into a test DB of your choice, follow the instruction
below. The best place is in your "conftest.py" file if you are using
pytest.

To import and use JSONLoad and optionally,
DEFAULT_DUMP_DATA_FOLDER_NAME, include the following import
statement in your test script:

    from viewmodel.json_load import JSONLoad, DEFAULT_DUMP_DATA_FOLDER_NAME

Optionally, override the DEFAULT_DUMP_DATA_FOLDER_NAME with another
in your script:

    DEFAULT_DUMP_DATA_FOLDER_NAME = 'my_alternate_folder_name'

Provide a test DB name (here in a separate variable called TEST_DB) and
create a test fixture that uses JSONLoad to call the method
`restore_db_from_json`:

    TEST_DB = 'my_test_db_name'
    
    @pytest.fixture(scope='session', autouse=True)
    def restore_db_from_json():
        JSONLoad(db_name=TEST_DB).restore_db_from_json()

Then be sure to connect to your test DB:

    res = ObjDict(dbname=TEST_DB, dbserver=None)
    viewModelDB.baseDB.connect(res)

#### JSONLoad Method Signatures

    # not sure what the idea here is...see .rst file history? these signature need a way of being written, then cleaned up
    __init__(host_name: str = 'localhost', port_number: int = 27017, db_name: str = None)
    insert_one(collection_name: str = None, data: dict = None)
    insert_many(collection_name: str = None, data: List = None)
    drop_db(db_name: str)
    drop_collection(collection_name: str)
    read_json_data_file(path_to_file: str, file_name: str)
    load_data(collection_name: str, path_to_file: str, file_name: str)
    get_default_dumped_data_path()
    load_all(json_data_path: str = None)
    restore_db_from_json()

## Data Relationships and Joins

The term 'relational database' comes from the concept that data
contained in separate tables (or collections) is related.

### Data Relationship Types

#### Many-to-One

These are classic 'dry' (Dont Repeat Yourself) solutions. Several
records (or rows or documents) in a table/collection will use the same
information. For example, consider the Students are each signed up for a
degree. Consider a model where are several Students for each degree, but
each Student is in only one degree program at one time, even if that
degree program is itself a double degree. For each degree, there could
be further information such as the degree description, number of years
within the degree, head teacher for the degree and an information URL.
Each Student document could contain all of this information about their
degree program, but many students documents would repeat the same
information. The solution is having a separate document for each degree
and linking the students to their degree.

See the tests tutorialtest_tutorial::class GenerateCourseData

on (name, city code, state) from a separate city table will mean that
information for each city is not repeated for each address with the same
city. From the perspective of the address, the relationship is
'one-to-one' because for each address there is only one city. The
'many-to-one' is that many addresses may reference each city.

If our view is based on a single address, then retrieving the 'join' of
the information for the address together with the information for the
city still leaves a single 'row' in the resulting view.

In database design, to implement a 'many-to-one', each entry from the
many tables, contains a key to the city table. Read an address, the use
the 'key to the city' to read data from the city table.

#### One-to-Many

From a technical perspective, this is simply the same as 'many-to-one',
but viewed from the opposite perspective. However, the devil is in the
detail, and having the opposite perspective has implications that can
mean the correct implementation is very different. Looking at the
previous cities and addresses, the 'one-to-many' view from the city
perspective is to consider all addresses with the city.

If our view is based on a single city, then retrieving the 'join' would
result in rows for each address. So while the one-to-many is the
many-to-one from the opposite perspective, the view changes entirely and
in nature depending on which perspective.

In database design, the cross-reference key is still the 'key to the
city' within the address table. Read the city key (as 'our city key').
Then using the key field find all addresses with their 'key to the city'
value matching the key in 'our city key'.

#### One of Many Selector

This is a real-world application of the 'many-to-one' join, where the
table of possible 'ones' effective represents one of a finite set of
choices which may be chosen from a 'drop-down list box'. ViewModel has a
specific Field Type, the 'EnumForeignField'. Note that to display
choices for editing the entire table of choices is required. There are
no strict formulae as to when the number of choices or total data of the
choices table is too large but generally the system must have the
capacity to consider having the entire table in memory acceptable.

#### Many-to-Many

Consider now database with not just addresses and cities, but also
people. Each person might have a relationship to several addresses.
However, rather than this being a 'one-to-many' relationships, like the
Cities -> Addresses, where viewed from the other perspective, Addresses
-> Cities, for each address, there would be only one city, this time
for each address there may be multiple people.

In database design, this usually represents more of a challenge. If we
start with people, we cannot look for addresses with a 'person key'
field that matches since our person, since each address will need to
match potentially several (or many) people. The matching person cannot
be stored as a single value in our table. With SQL and even sometimes
with NoSQL, the solution is to have a separate table of relationships.
If we read this table for all entries matching our person we can find an
entry for each relationship to an address for that person. This solves
the problem because we can have more relationships than we have either
people or addresses, so one entry per table will not work without a
particular table that can have an entry for each relationship.

NoSQL like Mongo provides another alternative, which is keeping a list
of relationships inside one (or even both) of the tables. Since an entry
in the table can be a list, we could keep a list of addresses in the
people table. Read a person, and we have a list of addresses. Read an
address, and we can read all people with our address in their address
list. The principle is still the same, but there is this implementation
choice.

#### Relationship Specific Data

In some cases, there can be data specific to a relationship. Consider
the following people, addresses and then relationships:

    People:  Bob, Tom, Alice
    Addresses: RedHouse, Office1, Office2, GreenHouse
    Relationships:
        Bob: RedHouse is 'home', Office1 is 'work'
        Alice: RedHouse is 'home' and 'office'
        Tom: GreenHouse is Home, RedHouse is 'work1' and Office2 'work2'

The relationships between the people can each have their labels, just as
the relationships between people can. In fact, each relationship can
have a label from each perspective. Consider people relationships where
Bob could be 'husband' to Alice, but the same relationship from the
other perspective could be 'wife'.

So for Bob, we may have to have not only added 'RedHouse' and created a
relationship, we also have to manage a label for the relationship.

### Joins

In SQL, a join is a read, or update, of data from more than one table.
The join uses the relationship between tables to select rows of data
that combine information from multiple tables. Each table in the join is
effectively a source of data.

ViewModel support data from multiple sources, but currently this has
only been used to support joins from relationship tables and tables that
are part of the relationship.

### Inserts With Joins

When a new document is inserted for any source within a ViewModel,
fields within the current view can be automatically updated to reference
the new `_id` generated. These fields
should be listed in the `_sources[<source
updated>].join_links` list. This list is the field names to be
updated.

## How It Works

### The Rows Structure

The actual data is kept in a view list called
`dbRows_`, which reflects the actual data
being held in the underlying database. For each row of the view, there
is one entry in `dbRows_`.

#### The List of Elements of 'dbRows_'

Each entry is of type 'objdict' and the elements of the objdict were
originally the values of the fields in the view, but a new layer has
been added, so that 'objdict' entries at the top level represent the
data from a single source.

From:

    [ {'name':'Jane','course':'computing'}]

To:

    [ {'students': {'name':'Jane','course':'computing'}}]

The two-tiered structure, keyed by the 'table/collection' which is the
data source, better provides for data from multiple sources.

Data is not added directly to these rows but through the
'viewmodel_row' wrappers. So if a ViewModel row has a view_field (say
'last_name') which is not present in the row, setting the name would
add a new field to the appropriate ObjDict within the row, but also an
an entry to an additional 'changes' copy of the row, which holds new
values not yet committed to the database.

The 'rows' and 'changes' are the bridges between what is in the database
files, and what is held in memory.

#### The DBSource Descriptor

See the DBSource class documentation, but this class describes the
sources of data that are held within the dbRows.

Each 'row' has a set of a least one 'source'. Source types can be
MongoDB table, MongoDB document, memory, (and soon) another view.

Each source requires a method to load from the source, and update to the
source. 'getrows' methods currently takes a 'load filter' and uses that
to load all sources, but a structure is required to more flexible to
handle all sources.

Update methods again handle all source types.

It is suggested that a useful revision would be to have 'getrows' that
calls a `src_getrows` for each source and
update call `src_update()` for each
source.

#### New getRows

A new getrows would take a filter dictionary or list as valid
parameters. Each entry would need a lead and a lazy. Run 'leads' in
sequence until lead returns a non zero list. List is applied for that
source, all other sources are empty, but have 'lazy' load available.

Once a lead returns true, the
`scr_getrows_table()` would apply a
dictionary;
