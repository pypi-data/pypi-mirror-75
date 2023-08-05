#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne; Modified by Sonja Stuedli

import re
import logging
from bibtexentryparser.bibDefinitions import BibDefinitions

logger = logging.getLogger(__name__)

__all__ = ['BibTexWriter']

class BibTexWriter(object):
    """
    A writer to convert a BibTex entry stored as dictionary to a formated bibtex entry string.

    """

    def __init__(self):
        # Character(s) for indenting BibTeX field-value pairs. Default: single space.
        self.indent = ""

        # Tuple of fields for display order in a single BibTeX entry. Fields not listed here will be displayed: alphabetically at the end. Set to '[]' for alphabetical order. Default: '[]'
        self.display_order = []

        # whether the comma is written at the beginning or end of the line, i.e. , author = {} or author = {},
        self.comma_first = False

        # set containing all fields that should not be displayed
        self.do_not_display_fields = set()

        # if not none only fields in this set should be displayed
        self.do_only_display_fields = None

        # set containing all fields that should be written as bibTex strings.
        # while it works with any field it is best used with fields that are internally stored as integer
        self.write_as_string_fields = set()

        self.opening_field_character = ''
        self.closing_field_character = ''

        self.reset_to_default_settings()
        
    def is_writer(self):
        return True

    def add_do_not_display_field(self,fields):
        if type(fields) is str:
            self.do_not_display_fields.add(fields.strip())
        elif type(fields)is list:
            for field in fields:
                self.do_not_display_fields.add(field.strip())

    def set_do_not_display_field(self,fields):
        self.do_not_display_fields = set()
        if type(fields) is str:
            self.do_not_display_fields.add(fields.strip())
        elif type(fields)is list:
            for field in fields:
                self.do_not_display_fields.add(field.strip())

    def reset_to_default_settings(self):
        self.indent = '    '
        self.display_order = []
        self.comma_first = False
        self.do_not_display_fields = set()
        self.do_only_display_fields = None
        self.opening_field_character = '{'
        self.closing_field_character = '}'
        
        for entry in self.write_as_string_fields:
            self.remove_write_as_string_field(entry)

    # Add a field that should be written as bibtex string
    # field: string containing the , standard is a list
    def add_write_as_string_field(self,field, standard=None):
        self.write_as_string_fields.add(field)
        if field in BibDefinitions.not_stored_as_string:
            setattr(self,"standard_"+field, standard)

    def remove_write_as_string_field(self,field):
        if field in self.write_as_string_fields:
            self.write_as_string_fields.remove(field)
            try: 
                delattr(self,"standard_"+field)
            except:
                logger.warning("Attribute can't be deleted")
        
    def get_entry_field(self, bibentry, key):
        """
        Converts the field of a bibliographic entry to a BibTeX-formatted string.

        :param bibentry: entry
        :type bibentry: dict
        :param key: the field key
        :type key: string
        :return: BibTeX-formatted string
        :rtype: str or unicode
        """
        return self._write_field(key,bibentry[key])
    
        
    def write(self,entry):
        """
        Converts a bibliographic entry to a BibTeX-formatted string.

        :param bib_database: entry
        :type bib_database: dict
        :return: BibTeX-formatted string
        :rtype: str
        """
        logger.debug('writing a bibtex entry')
        return self._entry_to_bibtex(entry)

    
    
    def _entry_to_bibtex(self, entry):
        bibtex = ''
        # Write BibTeX key
        bibtex += '@' + entry['ENTRYTYPE'] + '{' + entry['ID']

        # create display_order of fields for this entry
        # first those keys which are both in self.display_order and in entry.keys
        display_order = [i for i in self.display_order if i in entry.keys()]
        # then all the other fields sorted alphabetically
        display_order.extend([i for i in sorted(entry) if (i not in self.display_order and i not in  ['ENTRYTYPE', 'ID'])])
        # Write field = value lines
        for key in display_order:
            # only print fields that should be displayed
            if (key not in self.do_not_display_fields) and (self.do_only_display_fields is None or key in self.do_only_display_fields):
                # write the previous comma and the newline
                if self.comma_first:
                    bibtex += "\n" + self.indent + ", " 
                else:
                    bibtex += ",\n" + self.indent 
                
                try:
                    # write the key and field
                    bibtex += key + " = "
                    bibtex += self._write_field(key,entry[key])
                           
                except TypeError:
                    logger.warning(["Writing of the bibtex did not work at: ", key, field])

        bibtex += ",\n}\n"
        return bibtex


    def _write_field(self,key,field):
        logger.debug("Start processing writable fields: ")
        
        # check whether fields should be written as string or not
        if key in self.write_as_string_fields:
            if key == 'author':
                written_fields = ''
                for entry in field:
                    written_fields += self._write_string_field(key,entry)
                    written_fields += '# "and" #'
                return written_fields[:-9]
            else:
                return self._write_string_field(key,field)
        else:
            if key == 'author':
                written_fields = self.opening_field_character
                for entry in field:
                    written_fields += self._write_normal_field(key,entry)
                    written_fields += " and "
                written_fields = written_fields[:-5]
                written_fields += self.closing_field_character
                return written_fields
            else:
                written_fields = self.opening_field_character + self._write_normal_field(key,field) + self.closing_field_character
                return written_fields

    def _write_normal_field(self,key,field):
        written_field = ''
        if key in BibDefinitions.not_stored_as_string:
            if type(field) is str:
                written_field = field
            else:
                try:
                    written_field = getattr(BibDefinitions,'default_'+ key)[field]
                except:
                    logger.warning("There is no default defined for this index.")
                    written_field = str(field)
        else:
            written_field = field
                
        # process the string as requested:
        # protect upper case in all the defined fields
        if key in BibDefinitions.protect_upper_case_fields:
            written_field = BibDefinitions.protect_upper_case(written_field)
            logger.debug("Protecting upper case words: " + written_field)
        # change latex stuff
        if key in BibDefinitions.contains_latex_expressions:
            written_field = BibDefinitions.string_to_latex(written_field)
            logger.debug("Transform string to latex: " + written_field)

        return written_field
        

    def _write_string_field(self,key,field):
        if key in BibDefinitions.not_stored_as_string:
            # write the field as a string if it is recognised else write it not as a bibtex string
            if type(field) is str:
                logger.warning("Field is not recognised. Fallback to non-string output")
                written_field = self.opening_field_character + field + self.closing_field_character
            else:
                try:
                    written_field = getattr(self,'standard_'+ key)[field]
                except:
                    logger.warning("There is no standard string defined even though it should. Fallback to non-string output.")
                    try:
                        written_field = self.opening_field_character + getattr(BibDefinitions,'default_'+ key)[field] + self.closing_field_character
                    except:
                        logger.warning("There is no default defined for this field.")
                        written_field =  self.opening_field_character + str(field) + self.closing_field_character
        else:
            # write the field as a bibtex string
            written_field = str(field)
        return written_field
