
from pyrasgo.member import Member

class FeatureList(object):
    
    def __init__(self, api_object):
        self._api_object = api_object

    def join_keys(self):
        return self._api_object['join_keys']

    def id(self):
        return self._api_object['id']

    def name(self):
        return self._api_object['name']

    def description(self):
        return self._api_object.get('description')

    def author(self):
        return Member(self._api_object.get('author'))

    def snowflake_table_metadata(self):
        features = self._api_object
        metadata = {
            "database": features.get("database", "rasgoalpha"),
            "schema": features.get("schema", "public"),
            "table": self._snowflake_table_name(),
            }
        return metadata

    def _snowflake_table_name(self):
        table_name = self._api_object.get("dataTableName")
        if table_name is None:
            raise ValueError("No Table found for Feature List '{}'".format(self.id()))
        return table_name

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "FeatureList(id={}, name={}, description={}".format(self.id(), self.name(), self.description())
