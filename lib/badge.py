# -*- coding: ISO-8859-15 -*-

import svgwrite


class Badge():
    '''
    generate a badge for some text pair

    text object (one for left, one for right) is defined by
    a string (for display), a background color, a text color,
    and a link.

    ex:
        {
            "text": "github",
            "background": "#eee",
            "href": "http://www.github.com"
        }
    '''
    _pad = 8
    _sep = 4
    _height = 20

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def _text_width(self, text):
        return 7 * len(text)

    def _calculate_widths(self, text):
        right_width = self._sep + self._text_width(text) + self._pad
        left_width = self._pad + self._text_width('ESIP') + self._sep
        return left_width, right_width, left_width + right_width

    def _generate_text(self, text, x, y):
        # return the two text svg elements, text and shadow
        # x and y as strings
        yield svgwrite.text.Text(
            text=text,
            x=[str(x)],
            y=[str(y)],
            **{"fill": "#010101", "fill-opacity": ".3"}
        )
        yield svgwrite.text.Text(text=text, x=[str(x)], y=[str(y - 1)])

    def generate_badge(self, badge_type):
        badge_type = _badge_types.get(badge_type.lower())
        badge_color = badge_type.get('color')
        badge_name = badge_type.get('title')
        lw, rw, tw = self._calculate_widths(badge_name)

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
        group.add(svgwrite.shapes.Rect(size=(lw, self._height), **{"fill": _esip}))
        group.add(svgwrite.shapes.Rect(
            size=(rw, self._height),
            insert=(lw, 0),
            **{"fill": badge_color})
        )
        group.add(svgwrite.shapes.Rect(size=(tw, self._height), **{"fill": "url(#b)"}))
        svg.add(group)

        # add the text group
        tg = {
            "fill": "#fff",
            "text-anchor": "middle",
            "font-family": "DejaVu Sans,Verdana,Geneva,sans-serif",
            "font-size": "11"
        }
        text_group = svgwrite.container.Group(**tg)
        for t in self._generate_text('ESIP', (lw / 2) + 1, 15):
            text_group.add(t)
        for t in self._generate_text(badge_name, lw + ((rw / 2) - 1), 15):
            text_group.add(t)
        svg.add(text_group)

        return svg.tostring()
