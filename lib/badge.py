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

    supports shields.io plastic, flat round and flat square styles
    and href links for left and right.
    '''

    # default sizing
    _pad = 8
    _sep = 4
    _height = 20

    def __init__(self, left, right, style="flat round"):
        self.left = left
        self.right = right
        self.style = style

        if style == 'plastic':
            self._height = 18

    def _text_width(self, text):
        return 7 * len(text)

    def _calculate_widths(self):
        right_width = self._sep + \
            self._text_width(self.right.get("text")) + \
            self._pad
        left_width = self._pad + \
            self._text_width(self.left.get("text")) + \
            self._sep
        return left_width, right_width, left_width + right_width

    # svg fragments
    def _generate_linear_gradient(self):
        lg = svgwrite.gradients.LinearGradient(
            end=(0, "100%"),
            **{"id": "b"}
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

    def _generate_mask(self, tw):
        mask = svgwrite.masking.Mask(**{"id": "a"})
        mask_rect = svgwrite.shapes.Rect(
            size=(tw, self._height),
            rx=4 if self.style == 'plastic' else 3,
            **{"fill": "#fff"}
        )
        mask.add(mask_rect)
        return mask

    def _generate_background(self, lw, rw, tw):
        if self.style == 'flat square':
            group = svgwrite.container.Group(
                **{"shape-rendering": "crispEdges"})
            group.add(svgwrite.shapes.Rect(
                size=(lw, self._height),
                **{"fill": self.left.get('background', '#555')})
            )
            group.add(svgwrite.shapes.Rect(
                size=(rw, self._height),
                insert=(lw, 0),
                **{"fill": self.right.get('background')})
            )
            return group

        # and the other two
        group = svgwrite.container.Group(**{"mask": "url(#a)"})
        group.add(svgwrite.path.Path(
            d="M0 0h%(left)sv%(height)sH0z" % {"height": self._height, "left": lw},
            **{"fill": self.left.get('background', '#555')}
        ))
        group.add(svgwrite.path.Path(
            d="M%(left)s 0h%(right)sv%(height)sH%(left)sz" % {"height": self._height, "left": lw, "right": rw},
            **{"fill": self.right.get('background')}
        ))
        group.add(svgwrite.path.Path(
            d="M0 0h%(total)sv%(height)sH0z" % {"height": self._height, "total": tw},
            **{"fill": "url(#b)"}
        ))

        # group.add(svgwrite.shapes.Rect(
        #     size=(lw, self._height),
        #     **{"fill": self.left.get('background', '#555')})
        # )
        # group.add(svgwrite.shapes.Rect(
        #     size=(rw, self._height),
        #     insert=(lw, 0),
        #     **{"fill": self.right.get('background')})
        # )
        # group.add(
        #     svgwrite.shapes.Rect(
        #         size=(tw, self._height),
        #         **{"fill": "url(#b)"}
        #     )
        # )
        return group

    def _generate_text_group(self, lw, rw):
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
                x=[str((lw / 2) + 1)],
                y=['14']
            ))

            if 'href' in self.right:
                a = svgwrite.container.Hyperlink(self.right.get('href'))
                a.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(lw + (rw / 2) - 1)],
                    y=['14'],
                    **{'id': 'rlink'}
                ))
                group.add(a)
            else:
                group.add(svgwrite.text.Text(
                    text=self.right.get('text'),
                    x=[str(lw + (rw / 2) - 1)],
                    y=['14']
                ))
        elif self.style == 'flat round':
            # left
            lx = (lw / 2)  # + 1
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
            lx = lw + (rw / 2) - 1
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
            lx = (lw / 2) + 1
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str(lx)],
                y=['14'],
                **{"fill": "#010101", "fill-opacity": ".3"}
            ))
            group.add(svgwrite.text.Text(
                text=self.left.get('text'),
                x=[str(lx)],
                y=['13']
            ))

            # right
            lx = lw + (rw / 2) - 1
            group.add(svgwrite.text.Text(
                text=self.right.get('text'),
                x=[str(lx)],
                y=['14'],
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
                    y=['13']
                ))

        return group

    def generate_badge(self):
        # now with styles
        lw, rw, tw = self._calculate_widths()

        # build the svg
        extras = {"xmlns": "http://www.w3.org/2000/svg"}
        if 'href' in self.left or 'href' in self.right:
            extras["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        svg = svgwrite.container.SVG(
            size=(tw, self._height),
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

            svg.add(self._generate_mask(tw))

        svg.add(self._generate_background(lw, rw, tw))

        svg.add(self._generate_text_group(lw, rw))

        if 'href' in self.left:
            # we add it to the end
            a = svgwrite.container.Hyperlink(href=self.left.get('href'))
            a.add(svgwrite.shapes.Rect(
                size=(lw, self._height),
                **{
                    "id": "llink",
                    "fill": "url(#a)",
                    "x": ".5",
                    "y": ".5"
                }
            ))
            svg.add(a)

        return svg.tostring()
