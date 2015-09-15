from flask import Flask
app = Flask(__name__)

from flask import request, make_response, abort
from badge.badge import Badge

_badge_types = {
    "funded": {"background": "#A1D3E4", "text": "Funded"},
    "fundingfriday": {"background": "#A1D3E4", "text": "FUNding Friday"},
    "testbed": {"background": "#A1D3E4", "text": "Testbed"},
    "member": {"background": "#3FA1B9", "text": "Member"},
    "collaborator": {"background": "#3FA1B9", "text": "Collaborator"}
}

_esip = {"text": "ESIP"}


@app.route("/<badge>.svg")
@app.route("/<user>/<repository>/<badge>.svg")
def get_badge(badge, user=None, repository=None):
    '''
    routing:
        badge: effectively the text on the right side

    query params:
        style: plastic | flat-round | flat-square (same as shields.io)
               default is flat (coded as 'flat round')

        # for the default basic badge request
        user: account alias (non-functional, analytics only)
        repository: code repository name (non-functional, analytics only)

        # for the lefthand style options (logo, esip)
        display: logo | text (default is text)
    '''
    style = request.args.get('style', 'flat-round').replace('-', ' ')
    display = request.args.get('display', 'text').lower()

    right = _badge_types.get(badge.lower(), {})
    if not right:
        abort(404)

    badger = Badge(_esip, right, style=style, display=display)
    svg = badger.generate_badge()
    rsp = make_response(svg, 200)
    rsp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
    rsp.headers['Cache-Control'] = 'no-cache'

    return rsp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
