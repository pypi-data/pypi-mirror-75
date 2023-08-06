import json
from .validator import validate_source_ids, validate_job_id, validate_stage, validate_timestamp, validate_limit, validate_page, \
    validate_sort_by, validate_order_by
from ..utils import validate_key, validate_provider_keys


class JobScoring():
    """Manage job related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api


    def get(self, board_keys=None, source_key=None, profile_key=None, use_agent=None, stage=None, page=1, limit=30,
            sort_by='created_at', order_by=None, **kwargs):
        """
        Retrieve the scoring information.

        Args:
            board_keys:         <list>
                                board_keys
            source_key:         <string>
                                source_key
            profile_key:        <string>
                                profile_key
            use_agent:          <int>
                                use_agent
            stage:              <string>
                                stage
            limit:              <int> (default to 30)
                                number of fetched profiles/page
            page:               <int> REQUIRED default to 1
                                number of the page associated to the pagination
            sort_by:            <string>
            order_by:           <string>

        Returns
            parsing information

        """

        query_params = {'board_keys': json.dumps(validate_provider_keys(board_keys)),
                        'source_key': validate_key('Source', source_key),
                        'profile_key': validate_key('Profile', profile_key),
                        'use_agent': use_agent,
                        'stage': validate_stage(stage),
                        'limit': validate_limit(limit),
                        'page': validate_page(page),
                        'sort_by': validate_sort_by(sort_by),
                        'order_by': validate_order_by(order_by)
                        }

        params = {**query_params, **kwargs}
        response = self.client.get('jobs/scoring', params)
        return response.json()
