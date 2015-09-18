from flask import Flask
app = Flask(__name__)

from flask import request, make_response, abort
from badge.badge import Badge

_badge_types = {
    # supported
    "funded": {"background": "#A1D3E4", "text": "Funded"},
    "fundingfriday": {"background": "#A1D3E4", "text": "FUNding Friday"},
    "testbed": {"background": "#A1D3E4", "text": "Testbed"},
    # membership
    "member": {"background": "#3FA1B9", "text": "Member"},
    "collaborator": {"background": "#3FA1B9", "text": "Collaborator"},
    # clusters
    "agclimate": {"background": "#A1D3E4", "text": "Agriculture & Climate"},
    "climateed": {"background": "#A1D3E4", "text": "Climate Education"},
    "cloud": {"background": "#A1D3E4", "text": "Cloud Computing"},
    "datasteward": {"background": "#A1D3E4", "text": "Data Stewardship"},
    "datastudy": {"background": "#A1D3E4", "text": "Data Study"},
    "disasters": {"background": "#A1D3E4", "text": "Disasters"},
    "discovery": {"background": "#A1D3E4", "text": "Discovery"},
    "documentation": {"background": "#A1D3E4", "text": "Documentation"},
    "drones": {"background": "#A1D3E4", "text": "Drones"},
    "drupal": {"background": "#A1D3E4", "text": "Drupal"},
    "esda": {"background": "#A1D3E4", "text": "Earth Science Data Analytics"},
    "education": {"background": "#A1D3E4", "text": "Education"},
    "energyclimate": {"background": "#A1D3E4", "text": "Energy & Climate"},
    "envirosensing": {"background": "#A1D3E4", "text": "Envirosensing"},
    "infoquality": {"background": "#A1D3E4", "text": "Information Quality"},
    "infotech": {"background": "#A1D3E4", "text": "Information Technology & Interoperability"},
    "libraries": {"background": "#A1D3E4", "text": "Libraries"},
    "products": {"background": "#A1D3E4", "text": "Products & Services"},
    "sciencesoftware": {"background": "#A1D3E4", "text": "Science Software"},
    "semanticweb": {"background": "#A1D3E4", "text": "Semantic Web"},
    "visioneers": {"background": "#A1D3E4", "text": "Visioneers"},
    "webservices": {"background": "#A1D3E4", "text": "Web Services"}
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
    rsp.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'

    return rsp


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
