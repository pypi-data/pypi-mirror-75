#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on
# Original source: github.com/sciunto-org/python-bibtexparser
# Authors:
# markmacgillivray
# Etienne Posthumus (epoz)
# Francois Boulogne <fboulogne at april dot org>
# Modified by Sonja Stuedli

import sys
import re
import logging
logger = logging.getLogger(__name__)

from bibtexentryparser.bibDefinitions import BibDefinitions

__all__ = ['BibTexParser']

class BibTexParser(object):
    """
    A parser for reading BibTeX bibliographic data entries.

    """

    def __init__(self):
        """
        Creates a parser for parsing BibTeX entries

        :return: parser
        :rtype: `BibTexParser`
        """
        self.reset_to_default_settings()
    
    def is_parser(self):
        return True


    def reset_to_default_settings(self):
        self.entry_key_replacements = {
            'keyw': "keyword",
            'keywords': "keyword",
            'authors': "author",
            'editors': "editor",
            'url': "link",
            'urls': "link",
            'links': "link",
            'eprint': "link",
            'subjects': "subject"
        }

        
    """
    Parse a string containing a bibtex entry.
    
    :return: bibtex entry
    :rtype: 'BibTexEntry'
    """
    def parse(self,bibstring):

        # locate the entry type
        logger.debug("Decoding bibtex entry:")
        logger.debug(bibstring)
        bibtex_expression = re.search('@(.+?)[{](.+?),(.+)[}]',bibstring,re.DOTALL)

        d = {}
        try:
            logger.debug(bibtex_expression.group(1))
            logger.debug(bibtex_expression.group(2))
            logger.debug(bibtex_expression.group(3))

            # get the entry_type: 
            entry_type = self._process_entry_type(bibtex_expression.group(1))
            d['ENTRYTYPE'] = entry_type
            
            # get the entry_id
            entry_id = bibtex_expression.group(2)
            d['ID'] = entry_id

            # find keys and fields using regular expressions.
            # find first all key = {field} and key = "field"
            for match in re.finditer('\s*?([a-zA-Z0-9]+?)\s*?=\s*?[{"](.*?)[}"]\s*?,',bibtex_expression.group(3),re.DOTALL):
                logger.debug("Match found:" + match.group(1) + " and " + match.group(2))

                processed_key = self._process_key(match.group(1))
                d[processed_key] = self._get_processed_field(processed_key,match.group(2))
            # find all key = string
            for match in re.finditer('\s*?([a-zA-Z0-9]+?)\s*?=\s*?([^"{}]*?)\s*?,',bibtex_expression.group(3),re.DOTALL):
                logger.debug("Match found:" + match.group(1) + " and " + match.group(2))

                processed_key = self._process_key(match.group(1))
                d[processed_key] = self._get_processed_field(processed_key,match.group(2))

        except:
            logger.warning("Entry not properly decoded.")
            logger.warning(bibstring)

            return None
        return d

    def _process_entry_type(self,entry_type):
        """ Processes a bibtex entry type. This makes it lower case. 
        :param key: a entry type
        :type key: string
        :returns: string
        """
        entry_type = entry_type.lower()
        return entry_type

    
    def _process_key(self, key):
        """ Processes a bibtex field key. This makes it lower case and does key changes such that all equivalent keys are equal
        :param key: a key
        :type key: string
        :returns: string 
        """
        key = key.lower()
        if key in self.entry_key_replacements:
            key = self.entry_key_replacements[key]

        logger.debug("Key processed: " + key)
        return key

    def _get_index_of_closing_bracket(self, text, start):
        if text[start] == '[':
            opening_character = "["
            closing_character = "]"
        elif text[start] == '{':
            opening_character = "{"
            closing_character = "}"
        elif text[start] == '(':
            opening_character = "("
            closing_character =")"
        else:
            return None
        d = 0
        for idx, character in enumerate(text[start:]):
            if character == opening_character:
                d = d+1
            elif character == closing_character:
                d = d -1
            if d == 0:
                return idx+start
        return start
                
    # this function processes the field of a given key.
    def _get_processed_field(self,key,field):

        if not field or field == "{}":
            logger.debug(f'field is empty')
            field = ''

        logger.debug("Start field processing: " + field)
        processed_field=field.strip()
        
        # if (processed_field.startswith('{') and self._get_index_of_closing_bracket(processed_field,0) == len(processed_field)-1):
        #     processed_field = processed_field[1:len(processed_field)-1]
        #     logger.debug("Found brackets to strip: " + processed_field)

        # while (processed_field.startswith('"') and processed_field.endswith('"')):
        #     processed_field = processed_field[1:len(processed_field)-1]
        #     logger.debug("Found brackets to strip: " + processed_field)
            
        # processed_field = processed_field.strip()

        if key in BibDefinitions.contains_latex_expressions:
            processed_field = BibDefinitions.latex_to_string(processed_field)
            logger.debug("Transformed latex to string: " + processed_field)
            
        if key in BibDefinitions.protect_upper_case_fields:
            processed_field = BibDefinitions.unprotect_upper_case(processed_field)
            logger.debug("Unprotect upper case: " + processed_field)

        if key == "author":
            processed_field = self._process_authors(processed_field)

        if key in BibDefinitions.not_stored_as_string:
            processed_field = self._process_string_field(key,processed_field)
            logger.debug("Process non-string fields:" + str(processed_field))

        return processed_field

    def _process_authors(self,field):
        fields = field.split(' and ')
        processed_authors = list()
        concatenate_entry = None
        for idx,entry in enumerate(fields):
            entry = entry.strip()
            if concatenate_entry is not None:
                if entry.endswith('}'):
                    entry = " and ".join([concatenate_entry,entry[:-1]])
                    concatenate_entry = None
                else:
                    concatenate_entry = " and ".join([concatenate_entry,entry])
            elif entry.startswith('{') and self._get_index_of_closing_bracket(entry,0) == 0:
                concatenate_entry = entry[1:]
            elif (entry.startswith('{') and self._get_index_of_closing_bracket(entry,0) == len(entry)-1):
                entry = entry[1:-1]
                
            if concatenate_entry is None:
                processed_authors.append(entry.strip())
        return processed_authors
    
    def set_entry_field(self,bibentry,key,text):
        processed_key = self._process_key(key)
        bibentry[processed_key] = self._get_processed_field(processed_key,text)
        return  bibentry    

    # preprocess special fields that are internally not stored as a string
    def _process_string_field(self, key, field):
        """ processes a string field, this field is internally not stored as a string but an int
        :param field: the field
        :type field: string 
        :returns: integer / string
        """
        if field == '':
            return 0
        if type(field) is str:
            try:
                return getattr(BibDefinitions,'recognised_'+ key)[field.lower()]
        
            except KeyError:
                getattr(BibDefinitions, 'non_recognised_'+key).add(field.lower())
                logger.error(f'For the key {key}, the field {field} is not recognised')
                return field
            
        elif type(field) is list:
            processed_field = list()
            for entry in field:
                try:
                    processed_field.append(getattr(BibDefinitions,'recognised_'+ key)[entry.lower()])
                except KeyError:
                    getattr(BibDefinitions, 'non_recognised_'+key).add(entry.lower())
                    processed_field.append(entry)
            return processed_field

    #
    def clear_all_key_replacements(self):
        """ clears all key replacements such that no keys are replaced
        """
        self.entry_key_replacements.clear()

    def add_key_replacement(self,original_keys,replaced_keys):
        """ clears all key replacements such
        :param original_key: list containing keys that should be replaced 
        :type original_key: string or list
        :param replaced_key: keys that the originals should be replaced with (if string all keys are replaced with the same key)
        :type replaced_key: string or list
        """
        if type(original_keys) is str and type(replaced_keys) is str:
            self.entry_key_replacements[original_keys] = replaced_keys
        elif len(original_keys) != len(replaced_keys) and type(replaced_keys) is str:
            for i in range(len(original_keys)):
                self.entry_key_replacements[original_keys[i]] = replaced_keys
        elif len(original_keys) == len(replaced_keys):
            for i in range(len(original_keys)):
                self.entry_key_replacements[original_keys[i]] = replaced_keys[i]
        else:
            logger.warning("Can't add replacements. From: ")
            logger.warning(original_keys)
            logger.warning("to:")
            logger.warning(replaced_keys)
            logger.warning("replaced_keys should be a string or a list with equal many entries as original_keys.")
    def remove_key_replacement(self,keys):
        if type(keys) is str:
            self.entry_key_replacements.pop(keys)
        else:
            for key in keys:
                self.entry_key_replacements.pop(key)

    def overwrite_key_replacements(self,new_dict):
        self.entry_key_replacements = new_dict
