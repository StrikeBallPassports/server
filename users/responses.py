from copy import deepcopy

from utils.responses import error_responses as error_responses_template, responses
from .enums import ResponseDetail

error_responses = deepcopy(error_responses_template)

error_responses[401]['content']['application/json']['example']['detail'] = ResponseDetail.UNAUTHORIZED.value
error_responses[403]['content']['application/json']['example']['detail'] = ResponseDetail.FORBIDDEN.value
error_responses[409]['content']['application/json']['example']['detail'] = ResponseDetail.ALREADY_EXISTS.value

