=====
jsonxdm
=====

Convert between JSON and XML following the XDM schema of XSLT 3.0; facilitates use of XSLT with JSON

Description
===========

The *jsonxdm* library provides Python functions to convert JSON data to XML following a simple XML schema called XDM.  
XDM is a low-level intermediate XML-based format that can be used for up-conversion of JSON to other XML formats 
that conform to higher-level XML schemas for specific domains or applications.  It can also be used in the reverse 
direction as intermediate format in down-conversion to JSON.  

The XDM format is defined in the XSLT 3.0 W3C recommendation,  https://www.w3.org/TR/xslt-30/#schema-for-json. Native
XSLT 3.0 processors like Saxon have functions *fn:json-to-xml* and *fn-xml-to-json* that can be invoked from XSLT 3.0 
stylesheets.  The widely used *lxml* library provides XSLT support for Python,  but it does not support XSLT 3.0. The
*jsonxdm* library allows users of lxml to convert between JSON and XDM XML.  That XDM XML can then be transformed using
the templates and other features of the older version of XSLT supported in *lxml*.. 

Currently, four functions are provided:

 * loads(s)  parses a JSON string and converts it to an XDM instance as lxml *Element* class object
 * load(fd)  similar to *loads* but reads from a file object
 * dumps(x)  converts an XDM instance (again as lxml object) to a JSON string
 * dump(x)   similar to *dumps* but write to a file object

History
=======

v0.1   First release, 2020-07-12 

v0.2   Second release, 2020-07-28




