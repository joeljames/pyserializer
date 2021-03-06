=============
Serialization
=============
Serializers allow Python objects to be converted to native Python datatypes. The serialized data can then be easily rendered to json.

Getting started
===============
If you haven't installed pyserializer, simply use pip to install it like so::

    $ pip install pyserializer

Example: Simple Serialization
================================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Let's assume we have a user object::

    class User(object):
        def __init__(self, email, username):
            self.email = email
            self.username = username

Now let's define a serializer which we can use to serialize data that corresponds to User object::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

    class UserSerializer(Serializer):
        email = fields.CharField()
        username = fields.CharField()

Serailize the object
---------------------
Get the serialized data::

    users = [User(email='foo_1@bar.com', username='foo_1'), User(email='foo_2@bar.com', username='foo_2')]

    serializer = UserSerializer(users, many=True)
    serializer.data
    # [OrderedDict([('email', 'foo_1@bar.com'), ('username', 'foo_1')]), OrderedDict([('email', 'foo_2@bar.com'), ('username', 'foo_2')])]

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '[{"email": "foo_1@bar.com", "username": "foo_1"}, {"email": "foo_2@bar.com", "username": "foo_2"}]'


Example: Serialization With Meta Fields Defined
=================================================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Let's assume we have a user object::

    class User(object):
        def __init__(self, email, username):
            self.email = email
            self.username = username

Let's assume we only want to include the email field when serializing the User object. We can do this my defining a Meta class with fields property, within the serializer. Now let's define the serializer::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

    class UserSerializer(Serializer):
        email = fields.CharField()
        username = fields.CharField()

        class Meta:
            fields = (
                'email',
            )

Serailize the object
---------------------
Get the serialized data::

    users = [User(email='foo_1@bar.com', username='foo_1'), User(email='foo_2@bar.com', username='foo_2')]

    serializer = UserSerializer(users, many=True)
    serializer.data
    # [OrderedDict([('email', 'foo_1@bar.com')]), OrderedDict([('email', 'foo_2@bar.com')])]

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '[{"email": "foo_1@bar.com"}, {"email": "foo_2@bar.com"}]'


Example: Serialization With Meta Exclude Defined
=================================================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Let's assume we have a user object::

    class User(object):
        def __init__(self, email, username):
            self.email = email
            self.username = username

Let's assume we want to exclude the username field when serializing the User object. We can do this by defining a Meta class with exclude property, within the serializer. Now let's define the serializer::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

    class UserSerializer(Serializer):
        email = fields.CharField()
        username = fields.CharField()

        class Meta:
            exclude = (
                'username',
            )

Serailize the object
---------------------
Get the serialized data::

    users = [User(email='foo_1@bar.com', username='foo_1'), User(email='foo_2@bar.com', username='foo_2')]

    serializer = UserSerializer(users, many=True)
    serializer.data
    # [OrderedDict([('email', 'foo_1@bar.com')]), OrderedDict([('email', 'foo_2@bar.com')])]

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '[{"email": "foo_1@bar.com"}, {"email": "foo_2@bar.com"}]'


Example: Nested Serialization
===============================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Let's assume we have a comment object and the comment object has a user attached to it::

    from datetime import date, datetime

    class User(object):
        def __init__(self):
            self.email = 'foo@example.com'
            self.username = 'foobar'

    class Comment(object):
        def __init__(self):
            self.user = User()
            self.content = 'Some text content'
            self.created_date = date(2015, 1, 1)
            self.created_time = datetime(2015, 1, 1, 10, 30)

Now let's define a serializer which we can use to serialize data that currospond to User and Comment object::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

    class UserSerializer(Serializer):
        email = fields.CharField()
        username = fields.CharField()

    class CommentSerializer(Serializer):
        user = UserSerializer(source='user') # Eg: Nested serialization
        content = fields.CharField()
        createdDate = fields.DateField(source='created_date', format='%d/%m/%y') # Eg: Specify you own datetime format. Defaults to ISO_8601. Also, demonstrates specifying the source on the field.
        created_time = fields.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ') # Eg: Specify you own datetime format. Defaults to ISO_8601


Serailize the object
---------------------
Get the serialized data::

    user = User()
    comment = Comment()
    serializer = CommentSerializer(comment)
    serializer.data
    # OrderedDict([('content', 'Some text content'), ('created_time', '2015-01-01T10:30:00Z'), ('user', OrderedDict([('username', 'foobar'), ('email', 'foo@example.com')])), ('createdDate', '01/01/15')])

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '{"content": "Some text content", "created_time": "2015-01-01T10:30:00Z", "user": {"username": "foobar", "email": "foo@example.com"}, "createdDate": "01/01/15"}'


Example: Serialization with custom method field
=================================================

Defining our serailizer
-----------------------

Let's start by creating a python object which we can use to demonstrate our serializer. Let's assume we have a user object::

    class User:
        def __init__(self, first_name, last_name):
            self.first_name = first_name
            self.last_name = last_name

Now let's define a serializer which we can use to serialize data that corresponds to User object::

    from pyserializer.serializers import Serializer
    from pyserializer import fields

    class UserSerializer(Serializer):
        first_name = fields.CharField()
        last_name = fields.CharField()
        full_name = fields.MethodField(
            method_name='get_full_name'
        )

        def get_full_name(self, obj):
            return '{0} {1}'.format(
                obj.first_name,
                obj.last_name
            )

        class Meta:
            fields = (
                'first_name',
                'last_name',
                'full_name',
            )

Serailize the object
---------------------
Get the serialized data::

    user = User(first_name='John', last_name='Smith')
    serializer = UserSerializer(user)
    serializer.data
    # OrderedDict([('first_name', 'John'), ('last_name', 'Smith'), ('full_name', 'John Smith')])

Get in json serialized format::

    import json
    json.dumps(serializer.data)
    # '{"first_name": "John", "last_name": "Smith", "full_name": "John Smith"}'
