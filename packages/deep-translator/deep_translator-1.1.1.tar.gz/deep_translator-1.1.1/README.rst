===============
deep_translator
===============


.. image:: https://img.shields.io/pypi/v/deep_translator.svg
        :target: https://pypi.python.org/pypi/deep_translator
.. image:: https://img.shields.io/travis/nidhaloff/deep_translator.svg
        :target: https://travis-ci.com/nidhaloff/deep_translator
.. image:: https://readthedocs.org/projects/deep-translator/badge/?version=latest
        :target: https://deep-translator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://img.shields.io/pypi/l/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/pypi/dm/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator
.. image:: https://img.shields.io/pypi/status/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator
.. image:: https://img.shields.io/pypi/wheel/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/github/last-commit/nidhaloff/gpx_converter
        :alt: GitHub last commit
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FNidhalBaccouri
        :alt: Twitter URL
        :target: https://twitter.com/NidhalBaccouri

.. image:: https://img.shields.io/badge/$-buy%20me%20a%20coffee-ff69b4.svg?style=social
   :target: https://www.buymeacoffee.com/nidhaloff?new=1



Translation for humans
-----------------------

A flexible python tool to translate between different languages in a simple way.


* Free software: MIT license
* Documentation: https://deep-translator.readthedocs.io.

Motivation
-----------
I needed to translate a text using python. It was hard to find a simple way to do it.
There are other libraries that can be used for this task, but somehow,most of them
are buggy, not supported anymore or complex.

Therefore, I decided to build this simple tool, it is clean and easy to use and provide
support for all languages since it uses google translate under the hood.
More features are coming soon, mainly support for the PONS translator and others.

Basically, my goal is to integrate support for multiple famous translators
in this tool.

When you should use it
-----------------------
- If you want to translate text using python
- If you want to translate from a file
- If you want to get translations from many sources and not only one
- If you want to automate translations
- If you want to compare different translations

Why you should use it
----------------------
- High level of abstraction
- Easy to use and extend
- It's the only python tool that integrates many translators
- Stable

Features
--------

* Support for google translate
* Support for Pons translator (pons.com)
* Support for the Linguee translator
* Translate directly from a text file
* Get multiple translation for a word
* Automate the translation of different paragraphs in different languages
* Translate directly from terminal (version >= 1.1.0)

Installation
=============

Install the stable release:

.. code-block:: console

    $ pip install -U deep_translator

take a look at the docs if you want to install from source.

Usage
=====

.. code-block:: python

    from deep_translator import GoogleTranslator, PonsTranslator, LingueeTranslator, MyMemoryTranslator

    english_text = 'happy coding'

    result_german = GoogleTranslator(source='auto', target='de').translate(text=english_text)

    # Alternatively, you can pass languages by their name:
    translated = GoogleTranslator(source='english', target='german').translate(text=english_text)

    # or maybe you want to translate a text file ?
    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')

    # or maybe you have many sentences in different languages and want to automate the translation process
    translated = GoogleTranslator(source='auto', target='de').translate_sentences(your_list_of_sentences)


or maybe you would like to use the Pons translator: Pons.com


.. code-block:: python

    word = 'good'
    translated_word = PonsTranslator(source='english', target='french').translate(word)

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = PonsTranslator(source='english', target='french').translate(word, return_all=True)


Alternatively deep_translator (version >= 1.0.0) supports the Linguee translator:


.. code-block:: python

    word = 'good'
    translated_word = LingueeTranslator(source='english', target='french').translate(word)

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = LingueeTranslator(source='english', target='french').translate(word, return_all=True)

The mymemory translator is also supported for version >= 1.0.2:

.. code-block:: python

    word = 'good'
    translated_word = MyMemoryTranslator(source='english', target='french').translate(word)

Usage from Terminal
====================

For a quick access, you can use the deep_translator from terminal. For this to work, you need to provide
the right arguments, which are the translator you want to use, source language, target language and the text
you want to translate.

For example, provide "google" as an argument to use the google translator. Alternatively you can use
the other supported translators. Just read the documentation to have an overview about the supported
translators in this library.

.. code-block:: console

    $ deep_translator --translator "google" --source "english" --target "german" --text "happy coding"

Or you can go for the short version:

.. code-block:: console

    $ deep_translator -trans "google" -src "english" -tg "german" -txt "happy coding"

If you want, you can also pass the source and target language by their abbreviation

.. code-block:: console

    $ deep_translator -trans "google" -src "en" -tg "de" -txt "happy coding"

========
Links
========
Check this article on medium to know why you should use the deep-translator package and how to translate text using python.
https://medium.com/@nidhalbacc/how-to-translate-text-with-python-9d203139dcf5

==========
Next Step
==========

Take a look in the examples folder for more :)
Contributions are always welcome. Feel free to make a pull request and give me a feedback if you found the package useful/helpful or you are using it :)
