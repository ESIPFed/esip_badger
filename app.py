from flask import Flask
app = Flask(__name__)

from flask import make_response
import svgwrite


_badge_types = {
    "funded": {"color": "#A1D3E4", "title": "Funded"},
    "funding friday": {"color": "#A1D3E4", "title": "FUNding Friday"},
    "testbed": {"color": "#A1D3E4", "title": "Testbed"},
    "member": {"color": "#388477", "title": "Member"},
    "collaborator": {"color": "#388477", "title": "Collaborator"}
}

_esip = "#3FA1B9"
_pad = 8
_sep = 4
_height = 20


def text_width(text):
    return 7 * len(text)


def calculate_widths(text):
    right_width = _sep + text_width(text) + _pad
    left_width = _pad + text_width('ESIP') + _sep
    return left_width, right_width, left_width + right_width


def generate_text(text, x, y):
    # return the two text svg elements, text and shadow
    # x and y as strings
    yield svgwrite.text.Text(
        text=text,
        x=[str(x)],
        y=[str(y)],
        **{"fill": "#010101", "fill-opacity": ".3"}
    )
    yield svgwrite.text.Text(text=text, x=[str(x)], y=[str(y - 1)])


def generate_badge(badge_type):
    badge_type = _badge_types.get(badge_type.lower())
    badge_color = badge_type.get('color')
    badge_name = badge_type.get('title')
    lw, rw, tw = calculate_widths(badge_name)

    # build the svg
    svg = svgwrite.container.SVG(
        size=(tw, 20),
        **{"xmlns": "http://www.w3.org/2000/svg"}
    )

    # add the linear gradient
    linear_gradient = svgwrite.gradients.LinearGradient(
        end=(0, "100%"), **{"id": "b"}
    )
    linear_gradient.add_stop_color(offset=0, color="#bbb", opacity=".1")
    linear_gradient.add_stop_color(offset=1, opacity=".1")
    svg.add(linear_gradient)

    # add the mask
    mask = svgwrite.masking.Mask(**{"id": "a"})
    mask_rect = svgwrite.shapes.Rect(size=(tw, 20), rx=3, **{"fill": "#fff"})
    mask.add(mask_rect)
    svg.add(mask)

    # and the group, with mask
    group = svgwrite.container.Group(**{"mask": "url(#a)"})
    group.add(svgwrite.shapes.Rect(size=(lw, _height), **{"fill": _esip}))
    group.add(svgwrite.shapes.Rect(
        size=(rw, _height),
        insert=(lw, 0),
        **{"fill": badge_color})
    )
    group.add(svgwrite.shapes.Rect(size=(tw, _height), **{"fill": "url(#b)"}))
    svg.add(group)

    # add the text group
    tg = {
        "fill": "#fff",
        "text-anchor": "middle",
        "font-family": "DejaVu Sans,Verdana,Geneva,sans-serif",
        "font-size": "11"
    }
    text_group = svgwrite.container.Group(**tg)
    for t in generate_text('ESIP', (lw / 2) + 1, 15):
        text_group.add(t)
    for t in generate_text(badge_name, lw + ((rw / 2) - 1), 15):
        text_group.add(t)
    svg.add(text_group)

    return svg.tostring()


@app.route("/<badge>")
def get_badge(badge):
    svg = generate_badge(badge)
    rsp = make_response(svg, 200)
    rsp.headers['Content-Type'] = 'image/svg+xml'
    return rsp


if __name__ == "__main__":
    app.run()
