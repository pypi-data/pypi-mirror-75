#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on
# Original source: github.com/sciunto-org/python-bibtexparser
# Authors:
# markmacgillivray
# Etienne Posthumus (epoz)
# Francois Boulogne <fboulogne at april dot org>
# Modified by Sonja Stuedli

import re 
import itertools

import logging

log = logging.getLogger(__name__)

# This only works for Python 3 or higher
class BibDefinitions(type): 
    """
    Class containing global definitions, functions, and dictionaries for converting a BibTeX entry and properly parse it.
    """

    @classmethod
    def reset(cls):
        
        cls.protected_upper_case_words = dict()
        cls.protect_upper_case_fields = set()
        cls.contains_latex_expressions = set()
        
        for field in cls.not_stored_as_string:
            delattr(cls,"recognised_"+field)
            delattr(cls,"default_"+field)
            delattr(cls,"non_recognised_"+field)
        cls.not_stored_as_string = set()

    ####################################################################3
    # Proctecting upper case

    # dictionary containing special words that should be protected in fields that need protection. 
    protected_upper_case_words = dict()
    
    # list that contains all fields that may need upper case protection:
    protect_upper_case_fields = set()

    @classmethod
    def add_protected_upper_case_fields(cls,fields):
        if type(fields) is str:
            cls.protect_upper_case_fields.add(fields.strip())
        elif type(fields) is list or type(fields) is set:
            for field in fields:
                cls.protect_upper_case_fields.add(field.strip())
        else:
            log.error("fields should be provided as list, set, or string")
                        
    @classmethod
    def add_protected_upper_case_words(cls,protected_upper_case_words):
        """
        Function to add protected upper case words to the internal dictionary
        :param protected_upper_case_words: words that should be protected should be formatted in the correct capitalisation 
        :type: list,set or str
        """
        if(type(protected_upper_case_words) is list or type(protected_upper_case_words) is set):
            for word in protected_upper_case_words:
                cls.protected_upper_case_words[word.strip()] = re.sub('([A-Z]+)','{\g<1>}',word.strip())
        elif(type(protected_upper_case_words) is str):
            cls.protected_upper_case_words[protected_upper_case_words.strip()] = re.sub('([A-Z]+)','{\g<1>}',protected_upper_case_words.strip())
        else:
            log.error("protected_upper_case_words should be provided as list or string" )
            log.error(type(protected_upper_case_words))
        return

    ################################################
    # Some fields contain latex expressions that should be changed to unicode

    # list of all fields that can contain latex code
    contains_latex_expressions = set()

    @classmethod
    def add_containing_latex_fields(cls,fields):
        if type(fields) is str:
            cls.contains_latex_expressions.add(fields.strip())
        elif type(fields) is list or type(fields) is set:
            for field in fields:
                cls.contains_latex_expressions.add(field.strip())
        else:
            logger.warning("fields should be provided as list, set, or string")

    #################################################
    # Some fields can internally be handeled as intergers rather than strings and need special treatment.
    # The fields that are handle this way are stored in the list. 
    not_stored_as_string = set()
    
    @classmethod
    def add_stored_as_integer(cls,field,recognised_dict,standard_list):
        """
        Function to add fields that should be internally treated as integer
        :param field: the field that should be handeled internally
        :type: str
        :param recognised_dict: dictionary containing all recognised strings to a number
        :type: dict
        :param default_replacement_list: numbered list that assigns a word to the number
        :type: list
        """
        cls.not_stored_as_string.add(field.strip())
        setattr(cls,"recognised_"+field.strip(), recognised_dict)
        setattr(cls,"default_"+field.strip(), standard_list)
        setattr(cls,"non_recognised_"+field.strip(),set())

    # get all non-recognised entries that have been encountered by parser for the field 
    @classmethod
    def get_non_recognised_string_fields(cls,field):
        return getattr(cls,"non_recognised_"+field)

    @classmethod
    def unprotect_upper_case(cls,string):
        string = re.sub("{([A-Z]+)}","\g<1>",string)
        return string

    @classmethod
    def protect_upper_case(cls, string):

        string = re.sub('([A-Z][A-Z]+)','{\g<1>}',string)
        string = re.sub('(:)([A-Z]+)','\g<1>{\g<2>}',string)
        string = re.sub('(: )([A-Z]+)','\g<1>{\g<2>}',string)

        for key in cls.protected_upper_case_words:
            string = string.replace(key,cls.protected_upper_case_words[key])
        
        return string
    
    @classmethod
    def latex_to_string(cls,field):
        log.debug("Change LaTex to a normal string")
        latex_to_string_map=dict((y, x) for x, y in cls._string_latex_tuppels)       
        for key in latex_to_string_map:
            log.debug("Replace " + key + " with " + latex_to_string_map[key])
            log.debug("string becomes " + field.replace(key,latex_to_string_map[key]))
            field = field.replace(key,latex_to_string_map[key])
        return field

 
    @classmethod
    def string_to_latex(cls,field):
        log.debug("Change string to latex")       
        string_to_latex_map=dict(cls._string_latex_tuppels)
        for key in string_to_latex_map:
            log.debug("Replace " + key + " with " + string_to_latex_map[key])
            field = field.replace(key,string_to_latex_map[key])
        return field
        
    # contains all latex to unicode converstions: should be extended 
    _string_latex_tuppels = (
        ('ä','\\"{a}'),
        ('å','\\r{a}'),
        ("á","\\'{a}"),
        ("à","\\`{a}"),
        ('ë','\\"{e}'),
        ("í","\\'{\\i}"),
        ('ø','\\o'),
        ('ö','\\"{o}'),
        ('ò',"\\'{o}"),
        ('ü','\\"{u}'),
        ('ç','\\c{c}'),
        ('š','\\v{s}'),
        ('&','\\&'),
    )
