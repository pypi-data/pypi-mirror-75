"""
Copyright (c) 2020 Riptide
"""
_ROUTE = "api/entities"

_TAGS_STR = "tags"
_PRIORITY_ARRAY_STR = "priorityArray"


class RiptideEntityApp:

    def __init__(self, client):
        self._client = client

    def get_entity(self, uri, client_id=None):
        uri = "{}/{}".format(_ROUTE, uri.lstrip("/"))
        if client_id:
            uri = "{}?client_id={}".format(uri, client_id)
        return self._client.rc_get(uri=uri)

    def get_entity_tag(self, uri, name):
        uri = "{}/{}/{}/{}".format(
            _ROUTE, uri.strip("/"), _TAGS_STR, name
        )
        return self._client.rc_get(uri=uri)

    def get_entity_tags(self, uri):
        uri = "{}/{}/{}".format(_ROUTE, uri.strip("/"), _TAGS_STR)
        return self._client.rc_get(uri=uri)

    def entity_read_override(self, uri):
        uri = "{}/{}/{}".format(
            _ROUTE, uri.strip("/"), _PRIORITY_ARRAY_STR
        )
        return self._client.rc_get(uri=uri)

    def entity_read_override_at(self, uri, level):
        uri = "{}/{}/{}/{}".format(
            _ROUTE, uri.strip("/"), _PRIORITY_ARRAY_STR, level
        )
        return self._client.rc_get(uri=uri)


# __END__
