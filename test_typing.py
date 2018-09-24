from typing import List, Mapping, Optional, NewType


def foo(bar: int = 10) -> List[int]:
    return [_ for _ in range(bar)]


class ServiceClientBase:
    def __init__(self,
                 schema: str = 'http',
                 host: str = 'host_name',
                 port: int = 80) -> None:
        self.schema = schema
        self.host = host
        self.port = port

    @property
    def url(self) -> str:
        return '{}://{}:{}'.format(self.schema, self.host,
                                   self.port)


ConnectionID = NewType('ConnectionID', int)


class ServiceAClient(ServiceClientBase):
    pass


class ServiceBClient(ServiceClientBase):
    pass


def get_client(conn_id: ConnectionID,
               cfg: Mapping) -> Optional[ServiceClientBase]:
    if conn_id == 1:
        return ServiceAClient(**cfg)
    if conn_id == 2:
        return ServiceBClient(**cfg)
    return None
