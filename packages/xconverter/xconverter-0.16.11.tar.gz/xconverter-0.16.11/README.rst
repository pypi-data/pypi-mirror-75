Érudit Converter
================

.. image:: https://gitlab.erudit.org/erudit/production/converter/badges/master/pipeline.svg
`See Build details <https://gitlab.erudit.org/erudit/production/converter/commits/master>`_


Python library to convert XML files.

Available converters:

* Érudit Article to Érudit Publishing Schema (JATS)
* Érudit Article to HTML
* Érudit Article to PDF (WeasyPrint or PagedJS)
* Érudit Publishing Schema (JATS) to Érudit Article
* Érudit Publishing Schema (JATS) to HTML
* Érudit Publishing Schema (JATS) to PDF (WeasyPrint or PagedJS)
* Texture (DAR) to Érudit Article
* Texture (DAR) to HTML
* Texture (DAR) to PDF (WeasyPrint or PagedJS)

The HTML produced by the converter, is a HTML file optimized to produce PDF
files using the PagedMedia W3C standard and the libraries WeasyPrint or PagedJS.

External requirements
=====================

To produce PDF files using PagedJS, it is mandatory to have pagedjs-cli installed.

How to install pagedjs-cli is available at: https://www.npmjs.com/package/pagedjs-cli

How to Install
==============

#> pip install xconverter

How to use the console app
==========================

#> converter --help

::

    usage: converter [-h] [--converters]
                     [--from_source {erudit_ps,erudit_article,texture}] [--to TO]
                     [--output_dir OUTPUT_DIR] [--suffix SUFFIX]
                     [--custom_templates [CUSTOM_TEMPLATES [CUSTOM_TEMPLATES ...]]]
                     [--list_templates] [--pagedjs_support]
                     [--log_level {ERROR,WARNING,INFO,DEBUG}]
                     [source [source ...]]

    positional arguments:
      source

    optional arguments:
      -h, --help            show this help message and exit
      --converters, -c      display available converters
      --from_source {erudit_ps,erudit_article,texture}, -f {erudit_ps,erudit_article,texture}
                            from source could be .xml or .dar files
      --to TO, -t TO        the output format. It could be an XML or HTML
                            according to the conversor selected
      --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                            directory where the derivated XML files will be stored
      --suffix SUFFIX, -s SUFFIX
                            suffix to be concatenated to the output XML files. If
                            notspecified, it will assume the value of --to_xml
      --custom_templates [CUSTOM_TEMPLATES [CUSTOM_TEMPLATES ...]], -x [CUSTOM_TEMPLATES [CUSTOM_TEMPLATES ...]]
                            built-in template or path to a CSS file to customize
                            the default PDF Cascading Style Sheets.It is relevant
                            only while producing PDF or HTML outputsIt is also
                            posible to mix built-in templates with custom CSS
                            files
      --list_templates, -a  List available templates.
      --pagedjs_support, -p
                            apply pagedjs support for HTML outputs incluind
                            paged.js and preview.css in the head of the html
      --log_level {ERROR,WARNING,INFO,DEBUG}, -l {ERROR,WARNING,INFO,DEBUG}
                            Logging level


-------------------
Available Templates
-------------------

#> converter -a


::

    clean-one-column
    tested : True
    General purpose template, clean appearence with one column.

    clean-two-columns
    tested : True
    General purpose template, clean appearence with two columns.

    documentation
    tested : False
    Two column temmplate produced for the journal Documentation.

clean-one-column
----------------

**WeasyPrint**

#> converter XML_FILE -f erudit_article -t pdf -s test_weasyprint -x clean-one-column

**PagedJS**

#> converter XML_FILE -f erudit_article -t pdf -s test_pagedjs -x clean-one-column -p

clean-two-columns
-----------------

**WeasyPrint**

#> converter XML_FILE -f erudit_article -t pdf -s test_weasyprint -x clean-two-columns

**PagedJS**

#> converter XML_FILE -f erudit_article -t pdf -s test_pagedjs -x clean-two-columns -p

documentation
-------------

**WeasyPrint**

#> converter XML_FILE -f erudit_article -t pdf -s test_weasyprint -x documentation

**PagedJS**

#> converter XML_FILE -f erudit_article -t pdf -s test_pagedjs -x documentation -p

How to use the converter in your python APP
===========================================

from converter import converters

Convertion Examples
===================

A complete corpus with the most important use cases is available at: https://gitlab.erudit.org/erudit/production/converter/tree/master/tests/fixtures/sample_corpus





