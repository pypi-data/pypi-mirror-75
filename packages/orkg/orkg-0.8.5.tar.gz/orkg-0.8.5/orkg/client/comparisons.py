from orkg.utils import NamespacedClient, query_params, dict_to_url_params
from orkg.out import OrkgResponse


class ComparisonsClient(NamespacedClient):

    @query_params("contribution_ids", "title", "description", "reference")
    def add(self, params=None):
        if 'contribution_ids' not in params or 'title' not in params:
            raise ValueError('at least contribution_ids and title should be provided')

        for contribution_id in params['contribution_ids']:
            contribution_resource = self.client.resources.by_id(id=contribution_id).content

            if 'Contribution' not in contribution_resource['classes']:
                raise ValueError('this ID is not a contribution: ' + str(contribution_id))

        description = params['description'] if 'description' in params else ''
        reference = params['reference'] if 'reference' in params else ''
        contribution_ids = ','.join(params['contribution_ids'])

        comparison_resp = self.client.resources.add(label=params['title'], classes=['Comparison'])
        comparison_id = comparison_resp.content['id']
        description_id = self.client.literals.add(label=description).content['id']
        reference_id = self.client.literals.add(label=reference).content['id']
        url_id = self.client.literals.add(label='?contributions=' + contribution_ids).content['id']

        self.client.statements.add(subject_id=comparison_id, predicate_id='description', object_id=description_id)
        self.client.statements.add(subject_id=comparison_id, predicate_id='url', object_id=url_id)
        self.client.statements.add(subject_id=comparison_id, predicate_id='reference', object_id=reference_id)

        print('Created successfully, comparison id: ' + comparison_id)

        return OrkgResponse(comparison_resp)
