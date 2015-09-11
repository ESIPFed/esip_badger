ESIP Badger
===========

##ESIP Badge Design

This is the initial round of possible badges for the ESIP community. The structure and styles are based on the shields.io project (public domain) and a de facto standard for Github badging. 

We have two collections, one for getting at ESIP funded things and one for the relationship to ESIP. For funding, the tags are Funded, FUNding Friday and Testbed. For the relationships, it's Member and Collaborator. 

The API is very simple. There's a single URL with the structure:

> http://52.11.105.140/{badge-type}.svg?style={display-style}

where `funded` is one of the supported badge types.

Using it in one's documentation is as simple as adding:

```
<img src="http://52.11.105.140/funded.svg">
```

to the Markdown (as an `img` element or through another available SVG rendering method).

That method will only render the image wihout any links. To include a link to the ESIP site, use:

```
<a href="http://esipfed.org">![](http://52.11.105.140/funded.svg)</a>
```

modifying the SVG request as necessary.

####Parameter Options

**badge-type:** funded | testbed | fundingfriday | member | collaborator

**display-style:** flat-round | plastic | flat-square


####Examples

| Rounded | Plastic | Flat |
|:--------|:--------|:-----|
| <img style="float:left;" src="http://52.11.105.140/funded.svg"> | <img style="float:left;" src="http://52.11.105.140/funded.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/funded.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/testbed.svg"> | <img style="float:left;" src="http://52.11.105.140/testbed.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/testbed.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg"> | <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/fundingfriday.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/member.svg"> | <img style="float:left;" src="http://52.11.105.140/member.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/member.svg?style=flat-square"> |
| <img style="float:left;" src="http://52.11.105.140/collaborator.svg"> | <img style="float:left;" src="http://52.11.105.140/collaborator.svg?style=plastic"> | <img style="float:left;" src="http://52.11.105.140/collaborator.svg?style=flat-square"> |

####Notes

It is not pixel-perfect compared to the shields.io badges (server-side python estimation without typeface info). 

The ESIP side does include a link. This doesn't appear in the IPy or, often, in Chrome. 

The URL in the provided examples are volatile while testing. Use at your own risk (or, better, not at all just yet).


Installation
============

Coming soon.


Acknowledgements
================

Based on badges/shields and rausch/slackin


License
=======
MIT