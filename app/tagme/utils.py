from django.utils.functional import wraps
import pdb
import re
import copy


def require_instance_manager(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.instance is None:
            raise TypeError("Can't call %s with a non-instance manager" % func.__name__)
        return func(self, *args, **kwargs)
    return inner        


def tag_parser(tags):
    """
    Function to parse a string into valid tags
    Tags should only contain alphanumeric, space, _,- characters
    Tags should always be in lower case
    Function should always return a list
    Words within single quotes is preserved first
    Words within double quotes are preserved next 
    And then words are split on comma or spaces
    Multiple spaces are condensed into 1
    
    """
    return_tags = []
    if not tags:
        return_tags
        
    #shallow copy
    working_tagstr = copy.copy(tags)
    
    
    """
    lower case everything
    @todo: Need to check if/how locale will get affected
            when using string.lower()
    """
    working_tagstr = working_tagstr.lower()
    """
    ' single quote get first preference
    " double quote gets second preference
    comma ,gets 3rd preference
    space \s gets 4th preference
    http://stackoverflow.com/questions/2973436/regex-lookahead-lookbehind-and-atomic-groups
    """         
    
    """
    Find all words within single quotes
    """
    pattern = re.compile(r"\'(.+?)\'")
    words_within_quotes_single = re.findall(pattern,working_tagstr)
    working_tagstr = re.sub(pattern,'',working_tagstr)
    #print words_within_quotes_single 
    #print 'Words within single quotes: ','~'.join(words_within_quotes_single) 
    #print 'remaining String is ',working_tagstr
    return_tags.extend(words_within_quotes_single)
    
    """
    Find all words within double quotes
    """
    pattern = re.compile(r'\"(.+?)\"')
    words_within_quotes_double = re.findall(pattern,working_tagstr)
    working_tagstr = re.sub(pattern,'',working_tagstr)
    #print words_within_quotes_double 
    #print 'Words within double quotes: ','~'.join(words_within_quotes_double) 
    #print 'remaining String is ',working_tagstr
    return_tags.extend(words_within_quotes_double)
    
    """
    Remaining characters can just be split with spaces or comma
    """
    pattern = re.compile(r'\s+|,')
    words_separated_by_spaces_comma = pattern.split(working_tagstr)
    #print words_separated_by_spaces_comma
    #print 'Words separated by spaces and comma: ','~'.join(words_separated_by_spaces_comma)
    return_tags.extend(words_separated_by_spaces_comma)
    
    """
    Clean the words and replace multiple spaces into one
    """
    for i in range(0,len(return_tags)):
        return_tags[i] = re.sub(r'\ {2,}',' ',(re.sub(r'[^\w\ \d\_\-]','',return_tags[i])))
    
    """
    only non empty and non None words
    """    
    return_tags = [ tag for tag in return_tags if tag]
    """
    Only unique values
    """
    return_tags = list(set(return_tags))   
        
    return return_tags