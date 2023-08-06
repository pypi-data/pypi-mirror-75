import json

from utils import constants
from datetime import datetime


class FormatLog:

    now_time = None

    def format_log(self,
                   dateformat=constants.DEFAULT_DATE_TEMPLATE,
                   type=constants.JSON,
                   content=None):

        now_time = datetime.now()

        formatted_now_time = now_time.strftime(dateformat)

        if type == constants.JSON:

            return json.dumps({
                "timestamp": formatted_now_time,
                **content
            })

        else:
            raise NotImplementedError


