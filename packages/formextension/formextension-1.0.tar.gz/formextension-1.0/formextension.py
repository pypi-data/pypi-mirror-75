#!/usr/bin/env python3
import re
from markdown import util, Extension
from markdown.inlinepatterns import Pattern
from markdown.inlinepatterns import SimpleTagPattern

class FormExtensionException(Exception):
    pass

# Regex: \[(.*):(.*)\]

class FormExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "bugzillaURL"  : [ "%s", "Bugzilla URL to use, e.g. http://bugzilla.redhat.com/%s, default None" ],
        }

        for key, value in kwargs.items():
            if (key == "bugzillaURL") and (value.count('%s') != 1):
                raise BugzillaExtensionException("Invalid format string '" + value + "' ! ONE %s needed")

        Extension.__init__(self, *args, **kwargs)

    def add_inline(self, md, name, pattern_class):
        pattern = r'\[(?P<field_type>(.*)):(?P<name_id>(.*)):(?P<class_name>(.*)):(?P<placeholder>(.*))\]'
        objPattern = pattern_class(pattern, self.config)
        objPattern.md = md
        objPattern.ext = self
        md.inlinePatterns.add(name, objPattern, "<reference")

    def extendMarkdown(self, md, md_globals):
        self.add_inline(md, "bz", FormPattern)

class FormPattern(Pattern):
    def __init__(self, pattern, config):
        Pattern.__init__(self, pattern)
        self.config = config

    def getCompiledRegExp(self):
        return re.compile("^(.*?)%s(.*)$" % self.pattern, re.DOTALL | re.UNICODE | re.IGNORECASE)

    def handleMatch(self, match):
        if match :
            field_type = match.group('field_type')
            name = match.group('name_id')
            class_name = match.group('class_name')
            placeholder = match.group('placeholder')

            element = util.etree.Element(field_type)
            element.set("name", name)
            element.set("id", name)
            element.set("class", class_name)
            element.set("placeholder", placeholder)


            return element
        else:
            return ""


def makeExtension(*args, **kwargs):
    return FormExtension(*args, **kwargs)
