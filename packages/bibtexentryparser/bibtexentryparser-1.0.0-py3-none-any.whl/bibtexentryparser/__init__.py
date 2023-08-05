"""
`BibTeX <http://en.wikipedia.org/wiki/BibTeX>`_ is a bibliographic data file format.

The :mod:`bibtexparser` module can parse a BibTeX entry and write it. The parsed data is returned as a simple :class:`BibEntry` object representing the bibliographic source such as books and journal articles.

The following functions provide a quick and basic way to manipulate a BibTeX file.
More advanced features are also available in this module.

This package is heavily based on the bibtexparser version 0.6.2 module and modified by S. Stuedli.

"""

__all__ = [
    'load', 'write',
    'getString', 'setString',
    'bibparser', 'bibwriter'
]
__version__ = '1.0.0'


from bibtexentryparser import bibparser
from bibtexentryparser import bibwriter
from bibtexentryparser.bibDefinitions import BibDefinitions

# Load default settings for all global choices
def reset_to_default_settings():
    BibDefinitions.reset()
    BibDefinitions.add_protected_upper_case_fields(['journal','title','booktitle'])
    BibDefinitions.add_protected_upper_case_words(["Markov","Lyapunov"])

    BibDefinitions.add_containing_latex_fields(['title','author','publisher'])

    recognised_month = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11,'december':12, 'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11,'dec':12, 'sept':9, '1':1, '2':2, '3':3,'4':4,'5':5,'6':6, '7':7,'8':8,'9':9,'10':10,'11':11,'12':12,}
    default_month = ['','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
    BibDefinitions.add_stored_as_integer('month',recognised_month,default_month)

def load(bibtex_str, parser=None):
    """
    Load :class:`BibEntry` object from a string

    :param bibtex_str: input BibTeX string to be parsed
    :type bibtex_str: str or unicode
    :param parser: custom parser to use (optional)
    :type parser: BibTexParser
    :returns: bibliographic expression object
    :rtype: dictionary
    """
    if parser is None:
        parser = bibparser.BibTexParser()
    return parser.parse(bibtex_str)


def write(bibentry, writer=None):
    """
    Dump :class:`BibEntry` object to a BibTeX string

    :param bib_database: dictionary
    :type bib_database: BibDatabase
    :param writer: custom writer to use (optional) (not yet implemented)
    :type writer: BibTexWriter
    :returns: BibTeX string
    :rtype: unicode
    """
    if writer is None:
        writer = bibwriter.BibTexWriter()
    return writer.write(bibentry)


def getString(bibentry,key,writer=None):
    """
    getString: from a bibtex entry return the field of the given key as string

    :param bibentry: dictionary
    :type bibentry: dictionary
    :param key: key that should be extracted
    :type key: String
    :param writer: custom writer to use (optional) (not yet implemented)
    :type writer: BibTexWriter
    :returns: string
    :rtype: unicode
    """
    if writer is None:
        writer = bibwriter.BibTexWriter()
    return writer.get_entry_field(bibentry,key)
    
    
def setString(bibentry,key,text,parser=None):
    """
    setString: sets the field of the given key of the bibentry

    :param bibentry: dictionary
    :type bibentry: dictionary
    :param key: key that should be set
    :type text: String
    :param text: text that should be set
    :type key: String
    :param parser: custom writer to use (optional) (not yet implemented)
    :type parser: BibTexWriter
    :returns: string
    :rtype: unicode
    """
    if parser is None:
        parser = bibparser.BibTexParser()
    return parser.set_entry_field(bibentry,key,text)

