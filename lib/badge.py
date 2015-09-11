# -*- coding: ISO-8859-15 -*-

import svgwrite
import re


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

    supports shields.io plastic, flat round and flat square styles
    and href links for left and right.
    '''

    # default sizing
    _height = 20

    def __init__(self, left, right, style="flat round"):
        self.left = left
        self.right = right
        self.style = style
        self._lw, self._rw = self._calculate_widths()

    def _text_width(self, text):
        # omg. let's weight by char in a lazy lazy way, python
        def _count(pattern, term):
            parts = re.subn(re.compile(pattern), '', term)
            return parts[0], parts[1]

        weights = [
            ('[ilj]', 0.3),
            ('[mw]', 1.4),
            ('[ABCDEFGHIJKLNOPQRSTUVXYZ]', 0.9),
            ('[MW]', 1.5)
        ]

        new_term = text
        length = 0
        for pttn, weight in weights:
            new_term, removed = _count(pttn, new_term)
            length += removed * weight
        length += len(new_term)

        return round(7 * length)

    def _calculate_widths(self):
        right_width = self._text_width(self.right.get("text")) + 10
        left_width = self._text_width(self.left.get("text")) + 10
        return left_width, right_width

    # svg fragments
    def _generate_linear_gradient(self):
        lg = svgwrite.gradients.LinearGradient(
            end=(0, "100%"),
            **{"id": "linear_gradient"}
        )
        if self.style == 'flat round':
            lg.add_stop_color(offset=0, color="#bbb", opacity=".1")
            lg.add_stop_color(offset=1, opacity=".1")
        elif self.style == 'plastic':
            lg.add_stop_color(offset=0, color="#fff", opacity=".7")
            lg.add_stop_color(offset=0.1, color="#aaa", opacity=".1")
            lg.add_stop_color(offset=0.9, opacity=".3")
            lg.add_stop_color(offset=1, opacity=".5")
        return lg

    def _generate_mask(self):
        mask = svgwrite.masking.Mask(**{"id": "background_mask"})
        mask_rect = svgwrite.shapes.Rect(
            size=(self._lw + self._rw, self._height),
            rx=3,
            **{"fill": "#fff"}
        )
        mask.add(mask_rect)
        return mask

    def _generate_background(self):
        if self.style == 'flat square':
            group = svgwrite.container.Group(
                **{"shape-rendering": "crispEdges"})
            group.add(svgwrite.shapes.Rect(
                size=(self._lw, self._height),
                **{"fill": self.left.get('background', '#555')})
            )
            group.add(svgwrite.shapes.Rect(
                size=(self._rw, self._height),
                insert=(self._lw, 0),
                **{"fill": self.right.get('background')})
            )
            return group

        # and the other two
        group = svgwrite.container.Group(**{"mask": "url(#background_mask)"})
        group.add(svgwrite.path.Path(
            d="M0 0h%(left)sv%(height)sH0z" % {
                "height": self._height, "left": self._lw},
            **{"fill": self.left.get('background', '#555')}
        ))
        group.add(svgwrite.path.Path(
            d="M%(left)s 0h%(right)sv%(height)sH%(left)sz" % {
                "height": self._height, "left": self._lw, "right": self._rw},
            **{"fill": self.right.get('background')}
        ))
        group.add(svgwrite.path.Path(
            d="M0 0h%(total)sv%(height)sH0z" % {
                "height": self._height, "total": self._lw + self._rw},
            **{"fill": "url(#linear_gradient)"}
        ))
        return group

    def _generate_text_group(self):
        '''
        NOTE: the y values are taken from the shields.io templates
        '''
        tg = {
            "fill": "#fff",
            "text-anchor": "middle",
            "font-family": "DejaVu Sans,Verdana,Geneva,sans-serif",
            "font-size": "11"
        }
        group = svgwrite.container.Group(**tg)

        if self.style == 'flat square':
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str((self._lw / 2) + 1)],
                y=['14']
            ))

            if 'href' in self.right:
                a = svgwrite.container.Hyperlink(self.right.get('href'))
                a.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(self._lw + self._rw / 2 - 1)],
                    y=['14'],
                    **{'id': 'rlink'}
                ))
                group.add(a)
            else:
                group.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(self._lw + self._rw / 2 - 1)],
                    y=['14']
                ))
        elif self.style == 'flat round':
            # left
            lx = self._lw / 2
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str(lx)],
                y=['15'],
                **{"fill": "#010101", "fill-opacity": ".3"}
            ))
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str(lx)],
                y=['14']
            ))

            # right
            lx = self._lw + self._rw / 2 - 1
            group.add(svgwrite.text.Text(
                text=self.right.get('text'),
                x=[str(lx)],
                y=['15'],
                **{"fill": "#010101", "fill-opacity": ".3"}
            ))
            if 'href' in self.right:
                a = svgwrite.container.Hyperlink(self.right.get('href'))
                a.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(lx)],
                    y=['14'],
                    **{'id': 'rlink'}
                ))
                group.add(a)
            else:
                group.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(lx)],
                    y=['14']
                ))
        elif self.style == 'plastic':
            # left
            lx = self._lw / 2 + 1
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str(lx)],
                y=['15'],
                **{"fill": "#010101", "fill-opacity": ".3"}
            ))
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str(lx)],
                y=['14']
            ))

            # right
            lx = self._lw + self._rw / 2 - 1
            group.add(svgwrite.text.Text(
                text=self.right.get('text'),
                x=[str(lx)],
                y=['15'],
                **{"fill": "#010101", "fill-opacity": ".3"}
            ))

            if 'href' in self.right:
                a = svgwrite.container.Hyperlink(self.right.get('href'))
                a.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(lx)],
                    y=['13'],
                    **{'id': 'rlink'}
                ))
                group.add(a)
            else:
                group.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(lx)],
                    y=['14']
                ))

        return group

    def generate_badge(self):
        # now with styles

        # build the svg
        extras = {"xmlns": "http://www.w3.org/2000/svg"}
        if 'href' in self.left or 'href' in self.right:
            extras["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        svg = svgwrite.container.SVG(
            size=(self._lw + self._rw, self._height),
            **extras
        )

        if 'href' in self.left or 'href' in self.right:
            # add the cdata style blob
            style_content = '''#llink:hover { fill:url(#b); stroke:#ccc; }
            #rlink:hover { fill:#ddd; }
            '''
            svg.add(svgwrite.container.Style(content=style_content))

        if self.style in ['flat round', 'plastic']:
            svg.add(self._generate_linear_gradient())

            svg.add(self._generate_mask())

        svg.add(self._generate_background())

        svg.add(self._generate_text_group())

        if 'href' in self.left:
            # we add it to the end
            a = svgwrite.container.Hyperlink(href=self.left.get('href'))
            a.add(svgwrite.shapes.Rect(
                size=(self._lw, self._height),
                **{
                    "id": "llink",
                    "fill": "url(#a)",
                    "x": ".5",
                    "y": ".5"
                }
            ))
            svg.add(a)

        return svg.tostring()
