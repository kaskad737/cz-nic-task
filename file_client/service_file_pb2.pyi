from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Uuid(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class StatRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: Uuid
    def __init__(self, uuid: _Optional[_Union[Uuid, _Mapping]] = ...) -> None: ...

class StatReply(_message.Message):
    __slots__ = ["data"]
    class Data(_message.Message):
        __slots__ = ["create_datetime", "size", "mimetype", "name"]
        CREATE_DATETIME_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        MIMETYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        create_datetime: _timestamp_pb2.Timestamp
        size: int
        mimetype: str
        name: str
        def __init__(self, create_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., size: _Optional[int] = ..., mimetype: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: StatReply.Data
    def __init__(self, data: _Optional[_Union[StatReply.Data, _Mapping]] = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ["uuid", "size"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    uuid: Uuid
    size: int
    def __init__(self, uuid: _Optional[_Union[Uuid, _Mapping]] = ..., size: _Optional[int] = ...) -> None: ...

class ReadReply(_message.Message):
    __slots__ = ["data"]
    class Data(_message.Message):
        __slots__ = ["data"]
        DATA_FIELD_NUMBER: _ClassVar[int]
        data: bytes
        def __init__(self, data: _Optional[bytes] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: ReadReply.Data
    def __init__(self, data: _Optional[_Union[ReadReply.Data, _Mapping]] = ...) -> None: ...
