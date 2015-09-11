from flask import Flask
app = Flask(__name__)

from flask import request, make_response, abort
from lib.badge import Badge

_badge_types = {
    "funded": {"background": "#A1D3E4", "text": "Funded"},
    "fundingfriday": {"background": "#A1D3E4", "text": "FUNding Friday"},
    "testbed": {"background": "#A1D3E4", "text": "Testbed"},
    "member": {"background": "#3FA1B9", "text": "Member"},
    "collaborator": {"background": "#3FA1B9", "text": "Collaborator"}
}

_esip = {"text": "ESIP"}


@app.route("/<badge>.svg")
def get_badge(badge):
    '''
    routing:
        badge: effectively the text on the right side

    query params:
        style: plastic | flat-round | flat-square (same as shields.io)
               default is flat (coded as 'flat round')
    '''
    style = request.args.get('style', 'flat-round').replace('-', ' ')

    right = _badge_types.get(badge.lower(), {})
    if not right:
        abort(404)

    badger = Badge(_esip, right, style=style)
    svg = badger.generate_badge()
    rsp = make_response(svg, 200)
    rsp.headers['Content-Type'] = 'image/svg+xml;charset=utf-8'
    rsp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'

    return rsp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
