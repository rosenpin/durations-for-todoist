SERVER_PORT = 9990

# HTML related consts
HTML_CHECKED = "checked"
HTML_MODE_FORMAT = "[[{mode}_checked]]"
HTML_CURRENT_USER_PH = "{{USER_ID}}"
HTML_CURRENT_MODE_PH = '{{CURRENT_MODE}}'

# Paths
SETTINGS_PAGE = "resources/settings.html"
HOME_PAGE = "resources/index.html"

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
