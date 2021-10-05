"""Generic error messages."""

ERROR_CODE_AUTHORIZATION = 'authorization_error'
ERROR_CODE_BAD_REQUEST = 'bad_request'
ERROR_CODE_BAD_GRASS_REQUEST = 'bad_grass_request_error'
ERROR_CODE_CORRECTION_CONFLICT = 'correction_conflict'
ERROR_CODE_NOT_FOUND = 'not_found'
ERROR_CODE_MISSING_HEADER = 'missing_header_error'

ERROR_MESSAGE_MISSING_GRASS_HEADERS = 'Missing Grass Headers'
ERROR_MESSAGE_INCOMPLETE_GRASS_HEADERS = 'incomplete account headers'
ERROR_MESSAGE_INVALID_GRASS_ACCOUNT_TYPE = 'Invalid Grass Account Type'
ERROR_MESSAGE_FORBIDDEN_USER = 'User is forbidden'
ERROR_MESSAGE_INVALID_PROJECT = 'Invalid project id'
ERROR_MESSAGE_NOT_OWNER = 'Project is not owned by account'
ERROR_MESSAGE_NOT_PRODUCT_OWNER = 'Product is not owned by account'
ERROR_MESSAGE_MISSING_PRODUCT_INFORMATION = 'Product information is incomplete'
ERROR_MESSAGE_NO_ACCOUNT_GIVEN = 'No vendor or subaccount given'
ERROR_MESSAGE_UPC_NOT_AVAILABLE = 'UPC is not available for use'
ERROR_MESSAGE_UPC_NOT_VALID = 'UPC is not valid'
ERROR_MESSAGE_PRODUCT_CODE_NOT_AVAILABLE = 'product_code is not available'
ERROR_MESSAGE_ORCHARD_USER_ID_REQUIRED = 'Orchard-User-Id is required header'
ERROR_MESSAGE_GRASS_REJECT_VALIDATION = (
    'Direct access through ows-grass is blocked. Only'
    ' non-ows-grass microservice-to-microservice requests'
    ' are allowed.')
ERROR_MESSAGE_INVALID_RELEASE_CORRECTION = \
    'The release_correction does not reference the correct product'
ERROR_MESSAGE_PRODUCT_NOT_IN_PROGRESS = 'product not in progress state'
ERROR_MESSAGE_PRODUCT_NOT_SUBMITTED = 'product not in submitted state'
ERROR_MESSAGE_PRODUCT_ALREADY_SUBMITTED = 'Product is already submitted.'
ERROR_MESSAGE_PRODUCT_ALREADY_CHECKED_OUT = 'Product is already checked out'
ERROR_MESSAGE_INVALID_NOT_FOR_DISTRIBUTION = \
    'invalid value for not_for_distribution'
ERROR_MESSAGE_INVALID_RELEASE_STATUS = \
    'invalid value for release_status'
ERROR_MESSAGE_CANNOT_UPDATE_RELEASE_STATUS_FOR_DISTRIBUTION = \
    'cannot update release_status as product is for dsitribution'
INTERNAL_ERROR = 'internal_error'
VALIDATION_ERROR = 'validation_error'

SUCCESS_CODE = 'ok'
OWS_PRODUCT_WORKFLOW_ERROR_CODE = 'ows_product_workflow_error'
