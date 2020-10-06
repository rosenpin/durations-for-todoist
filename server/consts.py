import pathlib

SERVER_PORT = 9990

# Page locations
SETTINGS_PAGE_LOCATION = "settings"

# HTML related consts
HTML_CHECKED = "checked"
HTML_MODE_FORMAT = "[[{mode}_checked]]"
HTML_CURRENT_USER_PH = "{{USER_ID}}"
HTML_CURRENT_MODE_PH = '{{CURRENT_MODE}}'

# Paths
SETTINGS_PAGE = pathlib.Path(__file__).parent.parent / "resources/settings.html"
HOME_PAGE = pathlib.Path(__file__).parent.parent / "resources/index.html"

# Client keys
CLIENT_SECRET = "98f91bda2f894fa19c03e92e5cb2e0fc"
CLIENT_ID = "da3de3dd940f45b898e04c9d9796e09b"

modes = [
    "labels", "projects"
]

# URLS
SERVER_REDIRECT_URL = "https://durations.rosenpin.io/redirect"
TODOIST_AUTHORIZE_URL = "https://todoist.com/oauth/authorize"
TODOIST_TOKEN_URL = 'https://todoist.com/oauth/access_token'

# Todoist related consts
TODOIST_PREMISSIONS = "data:read_write"

# Param names
PARAM_STATE = "state"
PARAM_ACCESS_TOKEN = "access_token"
PARAM_CODE = "code"
WEB_HOOK_USER_ID_FIELD = "user_id"

# Cookie names
COOKIE_STATE = "state"
COOKIE_USERID = "user_id"

# Workaround proxy
INNER_SERVER = "http://0.0.0.0:9990"
OUTER_SERVER = "https://durations.rosenpin.io"

# Cooldown related consts
MINUTE = 60
BUSY_INSTANCE = 0
UPDATE_ALL_COOLDOWN = 15 * MINUTE

# Webhook related consts
WEB_HOOK_TASK_ID = "id"
WEB_HOOK_TASK_DATA = "event_data"

# Error Messages
WEBHOOK_ERROR_MESSAGE = "Error in webhook for request:\n\n {request}:\n\n {error}"
SERVER_ERROR_MESSAGE = "Server error: \n\n{error}"
USER_NOT_FOUND_MESSAGE = "user with user_id %s not found in db"
USER_IN_COOLDOWN_MESSAGE = "ignoring request because user is in cooldown"

# Messages
ALL_TASKS_SUCCESS_MESSAGE = "SUCCESS you tasks won't be updated for the next 15 minutes"

# HTTP codes
HTTP_USER_ERROR = 401
HTTP_SERVER_ERROR = 501
