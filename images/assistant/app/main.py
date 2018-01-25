#!/usr/bin/env python3
"""
whoami service authentication with the Hub
"""

from functools import wraps
import json
import os
from urllib.parse import quote

from flask import Flask, redirect, request, Response

from jupyterhub.services.auth import HubAuth

# will end with /
prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')

auth = HubAuth(
    api_token=os.environ['JUPYTERHUB_API_TOKEN'],
    cache_max_age=60,
)

app = Flask(__name__)


def authenticated(f):
    """Decorator for authenticating with the Hub"""
    @wraps(f)
    def decorated(*args, **kwargs):
        cookie = request.cookies.get(auth.cookie_name)
        token = request.headers.get(auth.auth_header_name)
        if cookie:
            user = auth.user_for_cookie(cookie)
        elif token:
            user = auth.user_for_token(token)
        else:
            user = None
        if user:
            return f(user, *args, **kwargs)
        else:
            # redirect to login url on failed auth
            return redirect(auth.login_url + '?next=%s' % quote(request.path))
    return decorated




import os
def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        # Removed this line because it was redundant the while will catch
        # it, I left it for history
        # if len(lines_found) > lines:
        #    break

        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    return lines_found[-lines:]


"""
{
    admin: true,
    groups: [ ],
    kind: "user",
    last_activity: "2018-01-14T04:42:32.221000",
    name: "erik.sundell",
    pending: null,
    server: "/user/erik.sundell/"
}
"""

from datetime import datetime

@app.route(prefix + "ping")
@authenticated
def ping(user):
    with open("/data/output.txt", "w") as text_file:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping from user: {user['name']}", file=text_file)

    return Response(
        json.dumps(user, indent=1, sort_keys=True),
        mimetype='application/json',
    )

@app.route(prefix + "pong")
def hello():
    with open("/data/output.txt", "r") as text_file:
        return text_file.read()

@authenticated
@app.route(prefix + "demo")
def fin():
    return "FIN!"

@authenticated
@app.route(prefix + "fisk")
def fisk():
    return "FISK!"




if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)