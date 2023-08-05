from orkg.utils import NamespacedClient, dict_to_url_params
from orkg.out import OrkgResponse
from typing import List, Tuple
import pandas as pd


class ContributionsClient(NamespacedClient):

    def simcomp_available(func):
        def check_if_simcomp_available(self, *args, **kwargs):
            if not self.client.simcomp_available:
                raise ValueError("simcomp_host must be provided in the ORKG wrapper class!")
            return func(self, *args, **kwargs)

        return check_if_simcomp_available

    @simcomp_available
    def similar(self, cont_id: str) -> OrkgResponse:
        self.client.simcomp._append_slash = True
        response = self.client.simcomp.similar(cont_id).GET()
        return OrkgResponse(response=response)

    @simcomp_available
    def compare(self, contributions: List[str], response_hash: str = None) -> OrkgResponse:
        self.client.simcomp._append_slash = False
        params = f'?contributions={",".join(contributions)}'
        if response_hash is not None:
            params = f'{params}&response_hash={response_hash}'
        response = self.client.simcomp.compare.GET(params)
        return OrkgResponse(response=response)

    def __get_contributions_from_comparison(self, comparison_id: str) -> Tuple[List[str], str]:
        resource = self.client.resources.by_id(comparison_id).content
        if 'Comparison' not in resource['classes']:
            raise ValueError("This id is not for a comparison")
        statements = self.client.statements.get_by_subject(subject_id=resource['id']).content
        obj = [statement['object'] for statement in statements if statement['predicate']['id'] == 'url'][0]
        url = obj['label']
        response_hash = None
        if 'response_hash=' in url:
            response_hash = url[url.index('response_hash=')+14:]
        return url[15:url.index('&')].split(','), response_hash

    def compare_dataframe(self, contributions: List[str] = None, comparison_id: str = None) -> pd.DataFrame:
        if contributions is None and comparison_id is None:
            raise ValueError("either provide the contributions, or the comparison ID")
        response_hash = None
        if comparison_id is not None:
            contributions, response_hash = self.__get_contributions_from_comparison(comparison_id)
        response = self.compare(contributions=contributions, response_hash=response_hash)
        if not response.succeeded:
            return pd.DataFrame()
        content = response.content
        contributions_list = content['contributions']
        columns = [f"{contribution['title']}/{contribution['contributionLabel']}" for contribution in
                   contributions_list]
        properties_list = content['properties']
        property_lookup = {prop['id']: prop['label'] for prop in properties_list}
        # create table view of the data
        data = content['data']
        indices = []
        rows = []
        for prop_id, values in data.items():
            indices.append(property_lookup[prop_id])
            row = []
            for index, value in enumerate(values):
                if not value[0]:
                    row.append('')
                else:
                    row.append('/'.join([v['label'] for v in value]))
            rows.append(row)
        # create dataframe from peaces
        df = pd.DataFrame(rows, columns=columns, index=indices)
        return df
