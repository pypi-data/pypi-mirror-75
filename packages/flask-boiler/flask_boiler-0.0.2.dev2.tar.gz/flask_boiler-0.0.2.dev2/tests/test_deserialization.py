# import typing
#
# import pytest
# from marshmallow import schema, fields, post_load
#
#
# def test_stuffs():
#
#     class ReferenceField(fields.Field):
#
#         def _deserialize(
#         self,
#         value: typing.Any,
#         attr: typing.Optional[str],
#         data: typing.Optional[typing.Mapping[str, typing.Any]],
#         **kwargs
#     ):
#             dm_cls = self.context['dm_cls']
#             general_schema = dm_cls.schema_cls()
#
#             obj_type = general_schema.find_obj_type(value)
#
#             class TmpSchema(schema.Schema):
#                 d = fields.Nested(obj_type.schema_cls)
#
#             this_schema = TmpSchema()
#             this_schema.context['obj_type'] = obj_type
#
#             this_schema.context['stuffs'] = self.context['stuffs']
#             return this_schema.load(dict(d=value))
#
#     class FirestoreSnapshotSchema(schema.Schema):
#         d = ReferenceField()
#
#     class Location:
#
#         @classmethod
#         def from_dict(cls, d):
#             src = dict(d=d)
#             master_schema = FirestoreSnapshotSchema()
#             master_schema.context['dm_cls'] = cls
#             return master_schema.load(data=src)
#
#
#     class LocationSchema(schema.Schema):
#         sublocation = ReferenceField()
#
#         @post_load
#         def make_object(self, data, **kwargs):
#             obj_type = self.context['obj_type']
#             return obj_type.new(**data)
#
