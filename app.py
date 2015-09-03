from flask import Flask
app = Flask(__name__)

from flask import make_response
from lib.badge import Badge


_badge_types = {
    "funded": {"color": "#A1D3E4", "title": "Funded"},
    "fundingfriday": {"color": "#A1D3E4", "title": "FUNding Friday"},
    "testbed": {"color": "#A1D3E4", "title": "Testbed"},
    "member": {"color": "#388477", "title": "Member"},
    "collaborator": {"color": "#388477", "title": "Collaborator"}
}

_esip = "#3FA1B9"


@app.route("/<badge>")
def get_badge(badge):
    svg = Badge.generate_badge(badge)
    rsp = make_response(svg, 200)
    rsp.headers['Content-Type'] = 'image/svg+xml'
    return rsp


if __name__ == "__main__":
    app.run()
