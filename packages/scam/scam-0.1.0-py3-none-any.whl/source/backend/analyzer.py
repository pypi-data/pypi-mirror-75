import re
import string
import tokenize
import collections
import javalang

# These classes and functions are used to analyze the different types of files
# all of these classes have parsed code and the read code. These functions also
# have the ability to convert a position and k length to the necessary substring
# for finding it in a file.


# This class is used to analyze python files
class PyAnalyzer:
    # initialize the tokens and parsed code
    def __init__(self, source):
        source.seek(0)
        tokens = tokenize.generate_tokens(source.readline)
        self._parser_tokens = self.__init_tokens(tokens)
        self._parsed_code = self.__get_parsed_code(self._parser_tokens)
        self._code = self.__get_code(self._parser_tokens)

    # create and load the parser tokens
    def __init_tokens(self, tokens):
        # create the new named tuple for the new modified tokens to be loaded into and the list they will be loaded into
        ParserTokenInfo = collections.namedtuple("ParserTokenInfo", ['type', 'string', 'start', 'end', 'line',
                                                                     'old_string'], rename=False, defaults=[None])
        parser_tokens = []
        pos = 0
        loop_line = False
        boiler_plate = ['(', ')', ':', 'def', 'class', 'self']
        indent_next = False

        try:
            for token in tokens:
                # set original replace value
                replace = re.sub(r"\s+", "", token.string.lower())

                start = pos
                end = pos + (diff := token.end[1] - token.start[1])
                # increment absolute position accordingly
                pos += diff

                try:
                    # if the token is an indent
                    if token.type == 5:
                        parser_tokens.append(ParserTokenInfo(token.type, "", start, end, token.line, ""))
                        continue
                    # if the token is a newline
                    elif token.type in [4, 61]:
                        # the nex line is an indent
                        indent_next = True
                        parser_tokens.append(ParserTokenInfo(token.type, replace, start, end, token.line,
                                                             find_end_spaces(token.line, token.end[1] - 1) + token.string))
                        continue
                    # if the token is comment/boilerplate/import or loopline is active
                    elif loop_line or token.type == 60 or token.string in boiler_plate or "import" in token.line:
                        # if the end of a loop
                        if token.string == ':' and token.type == 54:
                            loop_line = False
                        replace = ""
                    # if the comment is a name (identifier)
                    elif token.type == 1:
                        # if the name is a conditional
                        if token.string == 'if' or token.string == 'elif' or token.string == 'else':
                            replace = "c"
                        # if the name is a loop
                        elif token.string == 'for' or token.string == 'while':
                            # start loopline
                            if ':' in token.line:
                                loop_line = True
                            replace = 'l'
                        # if the name is a class
                        elif token.line[token.start[1]-6:token.start[1]-1] == 'class':
                            replace = '@'
                        # if the name is a function
                        elif token.line[token.end[1]] == '(':
                            if token.string == 'print':
                                replace = 'p'
                            else:
                                replace = 'f'
                        # if the name is a variable or other
                        else:
                            replace = 'v'
                    # find the indent and create the new tuple with (type, parsed code, start, end, string line, and code)
                    indent = len(token.line) - len(token.line.lstrip(" "))
                    parser_tokens.append(ParserTokenInfo(token.type, replace, start, end, token.line,
                                                         ((" " * indent) if indent_next else "") +
                                                         token.string + (" " if token.line[token.end[1]] == " " else "")))
                    if indent_next:
                        indent_next = False
                except IndexError:  # EOF is indexed
                    if token.string == ')':
                        parser_tokens.append(ParserTokenInfo(token.type, '', start,
                                                             end, token.line, token.string))
                    else:
                        parser_tokens.append(ParserTokenInfo(token.type, re.sub(r"\s+", "", token.string.lower()), start,
                                                             end, token.line, token.string))
        except Exception:
            pass
        return parser_tokens

    # get the parsed code from the parser tokens
    def __get_parsed_code(self, parser_tokens):
        parsed_code = ""
        for token in parser_tokens:
            parsed_code += token.string
        return parsed_code

    # get the code from the tokens
    def __get_code(self, parser_tokens):
        code = ""
        for token in parser_tokens:
            code += token.old_string
        return code

    @property
    def parsed_code(self):
        return self._parsed_code

    @property
    def code(self):
        return self._code

    # return a substring after being given a k and a position
    def get_code_from_parsed(self, k, pos):
        index = 0
        for token in self._parser_tokens:
            # when index is behind the starting position
            if index < pos:
                # if a token is a string and the desired starting position is in the string
                if token.type == 3 and pos < index + len(token.string):
                    # analyze the string character by character
                    for ch in token.old_string:
                        # if the character is whitespace and the index is behind the starting position
                        if ch == string.whitespace and index <= pos:
                            pos += 1
                            index += 1
                        # if the character is whitespace and the index is in front of the starting position
                        # and behind the ending position
                        elif ch == string.whitespace and index <= pos+k:
                            k += 1
                            index += 1
                        # else increment the index
                        else:
                            index += 1
                # for all other types just use the code to calculate the length difference
                else:
                    pos += len(token.old_string) - len(token.string)
                    index += len(token.old_string)
            # else starting position is behind index
            elif pos <= index < pos + k:
                # if a token is a string and the desired ending position is in the string
                if token.type == 3 and pos + k < index + len(token.string):
                    for ch in token.old_string:
                        if ch == string.whitespace and index <= pos+k:
                            k += 1
                            index += 1
                        else:
                            index += 1
                # else we can use the difference in the code and the parsed code
                else:
                    k += len(token.old_string) - len(token.string)
                    index += len(token.old_string)
            # else we have found our positions
            else:
                break
        return self._code[pos:pos+k]


# This class is used to analyze java files
class JavaAnalyzer:
    # initialize the tokens and parsed code
    def __init__(self, source):
        source.seek(0)
        self._code = source.read()
        self._code = remove_comments(self._code)
        tokens = javalang.tokenizer.tokenize(self._code)
        try:
            tree = javalang.parse.parse(self._code)
        except Exception:
            tree = []
        self._parser_tokens = self.__init_tokens(tokens, tree)
        self._parsed_code = self.__get_parsed_code(self._parser_tokens)

    # create and load the parser tokens
    def __init_tokens(self, tokens, tree):
        ParserTokenInfo = collections.namedtuple("ParserTokenInfo", ['type', 'string', 'position',
                                                                     'old_string'], rename=False, defaults=[None])
        parser_tokens = []
        """pos = 0
        loop_line = False
        boiler_plate = ['(', ')', ':', 'def']
        indent_next = False"""
        is_class = False
        index = 0
        try:
            for token in tokens:
                replace = re.sub(" ", "", token.value).lower()
                # print(token)
                # if the previous token was 'class'
                if is_class:
                    replace = '@'
                    is_class = False
                # if the token is a keyword
                elif type(token) == javalang.tokenizer.Keyword:
                    # conditionals
                    if token.value in ['if', 'else', 'switch', 'case']:
                        replace = 'c'
                    # if the value is 'class'
                    elif token.value == "class":
                        replace = ''
                        is_class = True
                # if separator
                elif type(token) == javalang.tokenizer.Separator:
                    # don't include
                    replace = ''
                # if modifier
                elif type(token) == javalang.tokenizer.Modifier:
                    # public
                    if token.value == 'public':
                        replace = 'u'
                    # private
                    elif token.value == 'private':
                        replace = 'r'
                    # static
                    elif token.value == 'static':
                        replace = 't'
                # if the token is an identifier
                elif type(token) == javalang.tokenizer.Identifier:
                    # if the value is a print
                    if token.value == 'print' or token.value == 'println':
                        replace = 'p'
                    # if the value is a string type
                    elif token.value == 'String':
                        replace = 's'
                    else:
                        replace = 'i'
                # else just return the original value
                parser_tokens.append(ParserTokenInfo(type(token), replace, token.position, re.sub(" ", "", token.value)))
                index += 1
        except Exception:
            pass
        return parser_tokens

    # get the parsed code by iterating through parser tokens
    def __get_parsed_code(self, parser_tokens):
        parsed_code = ""
        for token in parser_tokens:
            parsed_code += token.string
        return parsed_code

    @property
    def parsed_code(self):
        return self._parsed_code

    @property
    def code(self):
        return self._code

    # get the code given a k and position
    # the text has comments removed
    def get_code_from_parsed(self, k, pos):
        index = 0
        for token in self._parser_tokens:
            if index < pos:
                pos += len(token.old_string) - len(token.string)
                index += len(token.old_string)
            elif pos <= index < pos + k:
                k += len(token.old_string) - len(token.string)
                index += len(token.old_string)
            else:
                break

        return get_java_substring(pos, k, self._code)


# find the accurate substring for a text with spaces given the position and k of a text without spaces
def get_text_substring(pos, k, text):
    i = 0
    spaces_pos = []
    # for character in text
    for ch in text:
        # check if whitespace and if it is append the position to the array
        if ch == ' ' or ch == '\n':
            spaces_pos.append(i)
        i += 1
    # for the positions in the array modify position and k based on detected whitespace
    for space_pos in spaces_pos:
        if space_pos < pos:
            pos += 1
        if pos <= space_pos < pos + k:
            k += 1
    return text[pos:pos+k]


# find the accurate substring for a text with spaces given the position and k of a text without spaces
def get_java_substring(pos, k, text):
    i = 0
    spaces_pos = []
    # for character in text
    for ch in text:
        # check if whitespace and if it is append the position to the array
        if ch == ' ' or ch == '\n':
            spaces_pos.append(i)
        i += 1
    # for the positions in the array modify position and k based on detected whitespace
    for space_pos in spaces_pos:
        if space_pos < pos:
            pos += 1
        if pos <= space_pos < pos + k:
            k += 1
    return text[pos:pos+k]

# remove comments from java/c/c++ string
def remove_comments(text):
    def replacing_string(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)

    return re.sub(pattern, replacing_string, text)


def find_end_spaces(line, end):
    num_spaces = 0
    while line[end] == ' ':
        num_spaces += 1
        end -= 1
    return (num_spaces - 1) * " "

