ESIP Badger
===========

<a href="http://esipfed.org">![](http://52.11.105.140/roomthily/esip_badger/fundingfriday.svg)</a>

##ESIP Badge Design

This is the initial round of possible badges for the ESIP community. The structure and styles are based on the shields.io project (public domain) and a de facto standard for Github badging. 

We have two collections, one for getting at ESIP funded things and one for the relationship to ESIP. For funding, the tags are Funded, FUNding Friday and Testbed. For the relationships, it's Member and Collaborator. 

The API is very simple. There's a single URL with the structure:

> http://52.11.105.140/{badge-type}.svg?style={display-style}

**OR**

> http://52.11.105.140/{user}/{repository}/{badge-type}.svg?style={display-style}

where `funded` is one of the supported badge types, `user` is the Github account and `repository` is the repository name. 

Using it in one's documentation is as simple as adding:

```
<img src="http://52.11.105.140/funded.svg">
```

to the Markdown (as an `img` element or through another available SVG rendering method).

That method will only render the image without any links. To include a link to the ESIP site, use:

```
<a href="http://esipfed.org">![](http://52.11.105.140/roomthily/esip_badger/funded.svg)</a>
```

modifying the SVG request as necessary. That displays as: <a href="http://esipfed.org">![](http://52.11.105.140/roomthily/esip_badger/funded.svg)</a>

The `display` query parameter provides the option to display the ESIP logo on the left side:

```
<img src="http://52.11.105.140/funded.svg?display=logo">
```

generating: <a href="http://esipfed.org">![](http://52.11.105.140/funded.svg?display=logo)</a>


####Parameter Options

**badge-type:** funded | testbed | fundingfriday | member | collaborator

**display-style:** flat-round (default) | plastic | flat-square

**display-option:** logo | text (default)

**user:** Github user name

**repository:** repository name

`account` and `repo` are accepted for basic analytic purposes only, ex:

> http://52.11.105.140/roomthily/esip_badger/fundingfriday.svg


####Text Examples

| Rounded | Plastic | Flat |
|:--------|:--------|:-----|
| <img style="float:left;" src="http://52.11.105.140/funded.svg"> | <img style="float:left;" src="http://52.11.105.140/funded.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/funded.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/testbed.svg"> | <img style="float:left;" src="http://52.11.105.140/testbed.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/testbed.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg"> | <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/member.svg"> | <img style="float:left;" src="http://52.11.105.140/member.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/member.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/collaborator.svg"> | <img style="float:left;" src="http://52.11.105.140/collaborator.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/collaborator.svg?style=flat-square"> |


####Logo Examples

| Rounded | Plastic | Flat |
|:--------|:--------|:-----|
| <img style="float:left;" src="http://52.11.105.140/funded.svg?display=logo"> | <img style="float:left;" src="http://52.11.105.140/funded.svg?style=plastic&display=logo"> | <img style="float:left;" src="http://52.11.105.140/funded.svg?style=flat-square&display=logo"> |
| <img style="float:left;" src="http://52.11.105.140/testbed.svg?display=logo"> | <img style="float:left;" src="http://52.11.105.140/testbed.svg?style=plastic&display=logo"> | <img style="float:left;" src="http://52.11.105.140/testbed.svg?style=flat-square&display=logo"> |
| <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?display=logo"> | <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?style=plastic&display=logo"> | <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?style=flat-square&display=logo"> |
| <img style="float:left;" src="http://52.11.105.140/member.svg?display=logo"> | <img style="float:left;" src="http://52.11.105.140/member.svg?style=plastic&display=logo"> | <img style="float:left;" src="http://52.11.105.140/member.svg?style=flat-square&display=logo"> |
| <img style="float:left;" src="http://52.11.105.140/collaborator.svg?display=logo"> | <img style="float:left;" src="http://52.11.105.140/collaborator.svg?style=plastic&display=logo"> | <img style="float:left;" src="http://52.11.105.140/collaborator.svg?style=flat-square&display=logo"> |


####Notes

It is not pixel-perfect compared to the shields.io badges (server-side python estimation without typeface info). Nor is it pixel-perfect between terms.

The URL in the provided examples are volatile while testing. Use at your own risk (or, better, not at all just yet).


Installation
============

Refer to [INSTALL](INSTALL.md) for the details.


Acknowledgements
================

This project is supported by an ESIP Federation FUNding Friday award, Summer Meeting 2015. 

Based on [badges/shields](https://github.com/badges/shields) and [rauchg/slackin](https://github.com/rauchg/slackin).


License
=======
MIT
