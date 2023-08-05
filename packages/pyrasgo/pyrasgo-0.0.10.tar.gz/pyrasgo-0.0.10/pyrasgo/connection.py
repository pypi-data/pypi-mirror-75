
import os
import json
import requests
import amplitude
import pandas as pd
import snowflake.connector

from pyrasgo.feature_list import FeatureList

class RasgoConnection(object):

    def __init__(self, api_key):
        self._production_domain = "api.rasgoml.com"
        self._amplitude_key = "08836b1e33763119e01fc62c604a7ea8"
        self._user_id = None
        
        self._api_key = api_key
        self._hostname = os.environ.get("RAGSO_DOMAIN", self._production_domain)
        self._event_logger = amplitude.AmplitudeLogger(api_key = self._amplitude_key)
        if self._hostname != self._production_domain:
            self._event_logger.turn_off_logging()

    def get_lists(self):
        self.note({'event_type': 'get_lists'})
        response = self._request("/models", {"join": ["features", "author"]})
        response.raise_for_status()
        lists = response.json()
        return [FeatureList(entry) for entry in lists]

    def get_feature_list(self, list_id):
        self.note({'event_type': 'get_feature_list'})
        response = self._request("/models/{}".format(list_id), {"join": ["features", "author"]})
        response.raise_for_status()
        entry = response.json()
        return FeatureList(entry)

    def get_feature_data(self, feature_list_id):
        self.note({'event_type': 'get_feature_data'})
        feature_list = self.get_feature_list(feature_list_id)
        
        conn = self._snowflake_connection(feature_list.author())
        
        table_metadata = feature_list.snowflake_table_metadata()
        query = self._make_select_statement(table_metadata)
        result_set = self._run_query(conn, query)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    def _run_query(self, conn, query):
        cursor = conn.cursor().execute(query)
        return cursor

    def _make_select_statement(self, table_metadata):
        return "SELECT * FROM {database}.{schema}.{table}".format(**table_metadata)
    
    def _snowflake_connection(self, member):
        creds = member.snowflake_creds()
        conn = snowflake.connector.connect(**creds)
        return conn

    def _request(self, resource, params = {}):
        return requests.get(self._url(resource), headers=self._headers(), params = params)

    def _headers(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % self._api_key,
            }
        return headers
    
    def _url(self, resource):
        if '/' == resource[0]:
            resource = resource[1:]
        return f'https://{self._hostname}/{resource}'
        
    def note(self, event_dict):
        event_dict['user_id'] = self.get_user_id()
        event_dict['source'] = 'pyrasgo'
        event = self._event_logger.create_event(**event_dict)
        self._event_logger.log_event(event)

    def get_user_id(self):
        if self._user_id:
            return self._user_id
        else:
            response = self._request("/users")
            response.raise_for_status()
            try:
                response_body = response.json()
                user = response_body['data']
                self._user_id = user.get('id')
                return self._user_id
            except Exception:
                return None
