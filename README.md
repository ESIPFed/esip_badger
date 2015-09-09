ESIP Badger
===========

##ESIP Badge Design

This is the initial round of possible badges for the ESIP community. The structure and styles are based on the shields.io project (public domain) and a de facto standard for Github badging. 

We have two collections, one for getting at ESIP funded things and one for the relationship to ESIP. For funding, the tags are Funded, FUNding Friday and Testbed. For the relationships, it's Member and Collaborator. 

The API is very simple. There's a single URL with the structure:

> http://someurl.com/funded.svg?style=plastic

where `funded` is one of the supported badge types and `style` is plastic, flat-round (default) or flat-square.

Using it in one's documentation is as simple as adding:

```
<img src="http://someurl.com/funded.svg">
```

to the Markdown (as an `img` element or through another available SVG rendering method).

####Examples

| Rounded | Plastic | Flat |
|:--------|:--------|:-----|
| <img style="float:left;" src="http://127.0.0.1:5000/funded.svg"> | <img style="float:left;" src="http://127.0.0.1:5000/funded.svg?style=plastic"> | <img style="float:left;" src="http://127.0.0.1:5000/funded.svg?style=flat-square"> |
| <img style="float:left;" src="http://127.0.0.1:5000/testbed.svg"> | <img style="float:left;" src="http://127.0.0.1:5000/testbed.svg?style=plastic"> | <img style="float:left;" src="http://127.0.0.1:5000/testbed.svg?style=flat-square"> |
| <img style="float:left;" src="http://127.0.0.1:5000/fundingfriday.svg"> | <img style="float:left;" src="http://127.0.0.1:5000/fundingfriday.svg?style=plastic"> | <img style="float:left;" src="http://127.0.0.1:5000/fundingfriday.svg?style=flat-square"> |
| <img style="float:left;" src="http://127.0.0.1:5000/member.svg"> | <img style="float:left;" src="http://127.0.0.1:5000/member.svg?style=plastic"> | <img style="float:left;" src="http://127.0.0.1:5000/member.svg?style=flat-square"> |
| <img style="float:left;" src="http://127.0.0.1:5000/collaborator.svg"> | <img style="float:left;" src="http://127.0.0.1:5000/collaborator.svg?style=plastic"> | <img style="float:left;" src="http://127.0.0.1:5000/collaborator.svg?style=flat-square"> |


Installation
============

Coming soon.


Acknowledgements
================

Based on badges/shields and rausch/slackin


License
=======
MIT