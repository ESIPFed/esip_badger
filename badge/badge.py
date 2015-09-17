# -*- coding: ISO-8859-15 -*-

import svgwrite
import re


class Badge():
    '''
    generate a badge for some text pair

    text object (one for left, one for right) is defined by
    a string (for display), a background color, a text color (LIES).

    ex:
        {
            "text": "github",
            "background": "#eee"
        }

    supports shields.io plastic, flat round and flat square styles.
    '''

    # default sizing
    _height = 20

    # logo defaults (hardcoded for design feedback)
    _logo_width = 27  # 47
    _logo_height = 16.5  # 24
    _logo_padding = 3
    _logo_filename = 'esip-logo_small_white.svg'
    _logo_inserts = (5, 2)

    def __init__(self, left, right, style="flat round", display="text"):
        self.left = left
        self.right = right
        self.style = style
        self.display = display
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
        # aaaand we just borked the little bit of generic handling for text
        left_width = self._text_width(self.left.get("text")) + 10 if \
            self.display == 'text' else self._logo_width + 10
        right_width = self._text_width(self.right.get("text")) + 10
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
            if self.display == 'logo':
                group.add(
                    self._generate_image()
                )
            else:
                group.add(svgwrite.text.Text(
                    text=self.left.get('text'),
                    x=[str((self._lw / 2) + 1)],
                    y=['14']
                ))

            group.add(svgwrite.text.Text(
                text=self.right.get('text'),
                x=[str(self._lw + self._rw / 2 - 1)],
                y=['14']
            ))
        elif self.style == 'flat round':
            # left
            if self.display == 'logo':
                group.add(
                    self._generate_image()
                )
            else:
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
            group.add(svgwrite.text.Text(
                text=self.right.get('text'),
                x=[str(lx)],
                y=['14']
            ))
        elif self.style == 'plastic':
            if self.display == 'logo':
                group.add(
                    self._generate_image()
                )
            else:
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
            group.add(svgwrite.text.Text(
                text=self.right.get('text'),
                x=[str(lx)],
                y=['14']
            ))

        return group

    def _generate_image(self):
        # github (or markdown renderers generally, looks like) does
        # not handle the externally referenced svg (via an image elem)
        # so for the design feedback we're just hardcoding this in.
        group = svgwrite.container.Group(**{"transform": "translate(5,2)"})
        group.add(svgwrite.path.Path(
            d="m-0.115,1l27.11502,0l0,5.11493c-0.11423,-0.87114 -0.68653,-1.65921 -1.49767,-2.00767c-1.19075,-0.52499 -2.5292,-0.41537 -3.79726,-0.43269c-0.00115,2.84535 0.03346,5.69069 -0.02538,8.53604c0.35307,0.00116 0.70614,0.00231 1.05922,0.00116c0.01038,-0.89768 0.00461,-1.79536 0.00346,-2.69304c1.00153,-0.01731 2.06997,-0.04731 2.95035,-0.58961c0.64845,-0.38769 1.07768,-1.05114 1.30729,-1.75844l0,7.67527l-27.11502,0l0,-13.84596z",
            **{"fill": "none"}
        ))
        group.add(svgwrite.path.Path(
            d="m3.36958,3.20959c1.39152,-1.28306 3.23765,-2.18074 5.16339,-2.09305c0.96229,0.03346 1.94767,-0.105 2.88573,0.17654c0.73383,0.195 1.52767,0.43269 2.03535,1.03384c-2.05266,-0.31154 -4.22879,-0.37384 -6.17645,0.45345c-1.37537,0.59768 -2.70804,1.57152 -3.28726,3.00342c-0.83768,0.12576 -1.65921,0.33461 -2.49804,0.44999l0.015,-0.135c0.01154,-0.05192 0.03346,-0.15577 0.045,-0.20769c0.44076,-0.98999 1.03268,-1.9269 1.81729,-2.6815z",
            **{"fill": "#ffffff"}
        ))
        group.add(svgwrite.path.Path(
            d="m13.1656,3.81534c0.91729,-0.31269 1.90381,-0.24346 2.85342,-0.17884c0.03115,0.3023 0.05769,0.6046 0.08423,0.90691c-0.92191,-0.03116 -1.91536,-0.21346 -2.77612,0.21692c-0.3773,0.17077 -0.60345,0.54345 -0.70498,0.93229c-0.32885,-0.03692 -0.66115,-0.03923 -0.98883,-0.08192c-0.00462,-0.05654 -0.0127,-0.16731 -0.01731,-0.22269c0.19268,-0.74999 0.83076,-1.32806 1.54959,-1.57267z",
            **{"fill": "#ffffff"}
        ))
        group.add(svgwrite.path.Path(
            d="m18.34514,3.67919c0.33923,0.00462 0.67845,0.00693 1.01768,0.00577c-0.0127,2.83842 -0.03115,5.678 0.00693,8.51642c-0.34846,0.01269 -0.69692,0.015 -1.04538,0.00808c0.02423,-2.84304 -0.01616,-5.68839 0.02077,-8.53027z",
            **{"fill": "#ffffff"}
        ))
        group.add(svgwrite.path.Path(
            d="m21.70509,3.67458c1.26806,0.01731 2.60651,-0.0923 3.79725,0.43269c0.81115,0.34846 1.38344,1.13653 1.49768,2.00767l0,1.05575c-0.22962,0.70729 -0.65884,1.37075 -1.30729,1.75844c-0.88038,0.5423 -1.94882,0.5723 -2.95035,0.58961c0.00115,0.89768 0.00692,1.79536 -0.00346,2.69304c-0.35308,0.00115 -0.70614,0 -1.05922,-0.00116c0.05885,-2.84534 0.02423,-5.69069 0.02539,-8.53604z",
            **{"fill": "#ffffff"}
        ))
        group.add(svgwrite.path.Path(
            d="m22.73777,4.52841c0.80191,-0.03461 1.67306,-0.03346 2.36535,0.43615c1.1146,0.68076 1.1146,2.56035 0.00231,3.24342c-0.69576,0.46846 -1.5669,0.46384 -2.37112,0.4973c-0.06,-1.39151 -0.00808,-2.78534 0.00346,-4.17686z",
            **{"fill": "#555555"}
        ))
        group.add(svgwrite.path.Path(
            d="m11.51447,5.58648c0.02538,-0.04961 0.07615,-0.14884 0.10153,-0.19846c0.00462,0.05538 0.01269,0.16615 0.01731,0.22269c0.32769,0.04269 0.65999,0.045 0.98883,0.08192c0.96922,0.21577 2.02728,0.29192 2.8765,0.84115c-0.79499,0.07731 -1.59921,0.02999 -2.38958,0.16961c-0.46153,0.03 -0.95652,-0.105 -1.39267,0.09692c-0.555,-0.11884 -1.11806,0.01385 -1.67882,0.00116c-1.40421,0.00808 -2.80496,0.14077 -4.18956,0.3773c-0.76499,0.15115 -1.55075,0.17308 -2.30651,0.36577c-0.00808,0.25038 -0.01039,0.50076 -0.01846,0.75115c-0.02192,-0.24807 -0.03115,-0.49615 -0.045,-0.74422c-0.7696,0.13384 -1.55421,0.28038 -2.24882,0.65422c-0.16962,0.08769 -0.33807,0.18 -0.50884,0.26769c-0.36692,-0.49038 -0.85037,-1.0096 -0.70845,-1.67766c0.47076,-0.29769 1.10422,-0.28038 1.49537,-0.69691l-0.015,0.135c0.83884,-0.11538 1.66037,-0.32423 2.49805,-0.44999c2.5015,-0.19269 5.01569,-0.33116 7.52412,-0.19731l0.00001,0z",
            **{"fill": "#ffffff"}
        ))
        group.add(svgwrite.path.Path(
            d="m11.71638,6.8003c0.43615,-0.20192 0.93114,-0.06692 1.39267,-0.09692c0.82961,0.70614 1.99959,0.91153 2.72766,1.75382c0.51691,0.56538 0.60922,1.41575 0.37269,2.12536c-0.22846,0.65422 -0.79383,1.13536 -1.42383,1.39036c-1.08114,0.44999 -2.28343,0.39692 -3.42456,0.28961c-0.00808,-0.29884 -0.01961,-0.59653 -0.03346,-0.89421c1.00037,0.08192 2.04343,0.14769 3.00688,-0.19269c0.53076,-0.18923 0.99921,-0.68999 0.9046,-1.28998c-0.02308,-0.68076 -0.65422,-1.07884 -1.19883,-1.34883c-0.85384,-0.44076 -1.88075,-0.80999 -2.32381,-1.73651z",
            **{"fill": "#ffffff"}
        ))
        group.add(svgwrite.path.Path(
            d="m1.22922,8.20567c0.69461,-0.37384 1.47921,-0.52038 2.24882,-0.65422c0.01385,0.24807 0.02307,0.49615 0.045,0.74422c0.01615,0.16731 0.045,0.3323 0.07269,0.49846c2.07805,0.5446 4.24609,0.51576 6.37722,0.61037c-0.19269,0.20885 -0.49268,0.21922 -0.74999,0.28499c-1.75382,0.32308 -3.54918,0.25154 -5.318,0.10847c0.09461,0.20423 0.26769,0.35653 0.46846,0.4523c1.31767,0.52153 2.75996,0.63807 4.16533,0.55153c0.58153,-0.00808 1.16421,0.03231 1.74343,0.07962c-0.34038,0.22269 -0.75691,0.24922 -1.14575,0.32307c-1.43306,0.20539 -2.89381,0.17308 -4.33494,0.07385c0.09461,0.22615 0.28615,0.38769 0.51807,0.46038c0.89883,0.32884 1.86344,0.3923 2.80842,0.48461c0.99114,0.07038 1.98343,0.12461 2.97803,0.12c-1.30729,0.6473 -2.81534,0.44423 -4.22533,0.5273c0.26885,0.50192 0.86537,0.66576 1.34306,0.90461c0.95076,0.34845 1.93843,0.60691 2.93534,0.7846c-0.00115,0.02885 -0.0023,0.08423 -0.00346,0.11308c-0.29653,0.01846 -0.58845,0.07384 -0.88268,0.09923c-1.08114,-0.12231 -2.17728,0.04731 -3.25496,-0.105c-0.83422,-0.17423 -1.6569,-0.44884 -2.40112,-0.86883c-0.7973,-0.43499 -1.42729,-1.11114 -1.99728,-1.80574c-0.8596,-1.07075 -1.32921,-2.41958 -1.39036,-3.78687z",
            **{"fill": "#ffffff"}
        ))
        return group

    def generate_badge(self):
        # now with styles

        # build the svg
        extras = {"xmlns": "http://www.w3.org/2000/svg"}
        if self.display in ['logo']:
            extras['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'
        svg = svgwrite.container.SVG(
            size=(self._lw + self._rw, self._height),
            **extras
        )

        if self.style in ['flat round', 'plastic']:
            svg.add(self._generate_linear_gradient())

            svg.add(self._generate_mask())

        svg.add(self._generate_background())

        if self.display in ['logo']:
            pass

        svg.add(self._generate_text_group())

        return svg.tostring()
