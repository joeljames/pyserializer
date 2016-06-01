from nose.tools import *  # flake8: noqa
from mock import *  # flake8: noqa

from pyserializer.serializers import Serializer


class TestSerializer:

    @patch.object(Serializer, 'get_fields')
    def test_to_native(self, get_fields):
        field_object = Mock(name='id')
        fields = {'id': field_object}
        get_fields.return_value = fields
        instance = [Mock(name='object')]
        output = Serializer(instance).to_native(obj=instance)
        field_object.field_to_native.assert_called_with(instance, 'id')
        assert_equal(output, {'id': field_object.field_to_native()})

    @patch.object(Serializer, 'to_native')
    @patch.object(Serializer, 'get_fields')
    def test_data(self, get_fields, to_native):
        field_object = Mock(name='id')
        fields = {'id': field_object}
        get_fields.return_value = fields
        obj = Mock(name='object')
        instance = [obj]
        serializer = Serializer(instance)
        output = serializer.data
        to_native.assert_called_with(obj)
        assert_equal(output, [to_native()])
