"""
Strip non-textual RTF contents
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
Sources:
    https://stackoverflow.com/a/93029/11750328
    http://stackoverflow.com/a/188877
"""
import re


class RtfStripper:
    """Strips non-text data from an RTF string

    Properties:
    rtf (string): original string
    text (string): stripped string
    """
    __pattern = re.compile(
        r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
    # control words which specify a "destination".
    __destinations = frozenset((
        'aftncn', 'aftnsep', 'aftnsepc', 'annotation', 'atnauthor', 'atndate', 'atnicn', 'atnid',
        'atnparent', 'atnref', 'atntime', 'atrfend', 'atrfstart', 'author', 'background',
        'bkmkend', 'bkmkstart', 'blipuid', 'buptim', 'category', 'colorschememapping',
        'colortbl', 'comment', 'company', 'creatim', 'datafield', 'datastore', 'defchp', 'defpap',
        'do', 'doccomm', 'docvar', 'dptxbxtext', 'ebcend', 'ebcstart', 'factoidname', 'falt',
        'fchars', 'ffdeftext', 'ffentrymcr', 'ffexitmcr', 'ffformat', 'ffhelptext', 'ffl',
        'ffname', 'ffstattext', 'field', 'file', 'filetbl', 'fldinst', 'fldrslt', 'fldtype',
        'fname', 'fontemb', 'fontfile', 'fonttbl', 'footer', 'footerf', 'footerl', 'footerr',
        'footnote', 'formfield', 'ftncn', 'ftnsep', 'ftnsepc', 'g', 'generator', 'gridtbl',
        'header', 'headerf', 'headerl', 'headerr', 'hl', 'hlfr', 'hlinkbase', 'hlloc', 'hlsrc',
        'hsv', 'htmltag', 'info', 'keycode', 'keywords', 'latentstyles', 'lchars', 'levelnumbers',
        'leveltext', 'lfolevel', 'linkval', 'list', 'listlevel', 'listname', 'listoverride',
        'listoverridetable', 'listpicture', 'liststylename', 'listtable', 'listtext',
        'lsdlockedexcept', 'macc', 'maccPr', 'mailmerge', 'maln', 'malnScr', 'manager', 'margPr',
        'mbar', 'mbarPr', 'mbaseJc', 'mbegChr', 'mborderBox', 'mborderBoxPr', 'mbox', 'mboxPr',
        'mchr', 'mcount', 'mctrlPr', 'md', 'mdeg', 'mdegHide', 'mden', 'mdiff', 'mdPr', 'me',
        'mendChr', 'meqArr', 'meqArrPr', 'mf', 'mfName', 'mfPr', 'mfunc', 'mfuncPr', 'mgroupChr',
        'mgroupChrPr', 'mgrow', 'mhideBot', 'mhideLeft', 'mhideRight', 'mhideTop', 'mhtmltag',
        'mlim', 'mlimloc', 'mlimlow', 'mlimlowPr', 'mlimupp', 'mlimuppPr', 'mm', 'mmaddfieldname',
        'mmath', 'mmathPict', 'mmathPr', 'mmaxdist', 'mmc', 'mmcJc', 'mmconnectstr',
        'mmconnectstrdata', 'mmcPr', 'mmcs', 'mmdatasource', 'mmheadersource', 'mmmailsubject',
        'mmodso', 'mmodsofilter', 'mmodsofldmpdata', 'mmodsomappedname', 'mmodsoname',
        'mmodsorecipdata', 'mmodsosort', 'mmodsosrc', 'mmodsotable', 'mmodsoudl',
        'mmodsoudldata', 'mmodsouniquetag', 'mmPr', 'mmquery', 'mmr', 'mnary', 'mnaryPr',
        'mnoBreak', 'mnum', 'mobjDist', 'moMath', 'moMathPara', 'moMathParaPr', 'mopEmu',
        'mphant', 'mphantPr', 'mplcHide', 'mpos', 'mr', 'mrad', 'mradPr', 'mrPr', 'msepChr',
        'mshow', 'mshp', 'msPre', 'msPrePr', 'msSub', 'msSubPr', 'msSubSup', 'msSubSupPr', 'msSup',
        'msSupPr', 'mstrikeBLTR', 'mstrikeH', 'mstrikeTLBR', 'mstrikeV', 'msub', 'msubHide',
        'msup', 'msupHide', 'mtransp', 'mtype', 'mvertJc', 'mvfmf', 'mvfml', 'mvtof', 'mvtol',
        'mzeroAsc', 'mzeroDesc', 'mzeroWid', 'nesttableprops', 'nextfile', 'nonesttables',
        'objalias', 'objclass', 'objdata', 'object', 'objname', 'objsect', 'objtime', 'oldcprops',
        'oldpprops', 'oldsprops', 'oldtprops', 'oleclsid', 'operator', 'panose', 'password',
        'passwordhash', 'pgp', 'pgptbl', 'picprop', 'pict', 'pn', 'pnseclvl', 'pntext', 'pntxta',
        'pntxtb', 'printim', 'private', 'propname', 'protend', 'protstart', 'protusertbl', 'pxe',
        'result', 'revtbl', 'revtim', 'rsidtbl', 'rxe', 'shp', 'shpgrp', 'shpinst',
        'shppict', 'shprslt', 'shptxt', 'sn', 'sp', 'staticval', 'stylesheet', 'subject', 'sv',
        'svb', 'tc', 'template', 'themedata', 'title', 'txe', 'ud', 'upr', 'userprops',
        'wgrffmtfilter', 'windowcaption', 'writereservation', 'writereservhash', 'xe', 'xform',
        'xmlattrname', 'xmlattrvalue', 'xmlclose', 'xmlname', 'xmlnstbl',
        'xmlopen',
    ))
    # Translation of some special characters.
    __specialchars = {
        'par': '\n',
        'sect': '\n\n',
        'page': '\n\n',
        'line': '\n',
        'tab': '\t',
        'emdash': '\u2014',
        'endash': '\u2013',
        'emspace': '\u2003',
        'enspace': '\u2002',
        'qmspace': '\u2005',
        'bullet': '\u2022',
        'lquote': '\u2018',
        'rquote': '\u2019',
        'ldblquote': '\201C',
        'rdblquote': '\u201D',
    }

    @property
    def text(self):
        """
        :return: Text stripped from the RTF file
        """
        return self._text

    def __init__(self, rtf):
        """Initialize this class by performing the stripping and saving the result

        :param rtf: source string
        """
        self.rtf = rtf
        self.__stack = []
        self.__is_ignorable_group = False
        self.__chars_to_skip_after_unicode = 1
        self.__chars_left_to_skip = 0
        self.__out = []  # Output buffer.
        self.__strip()
        self._text = ''.join(self.__out)

    def __strip(self):
        for match in self.__pattern.finditer(self.rtf):
            word, arg, hexa, char, brace, tchar = match.groups()
            if brace:
                self.__handle_brace(brace)
            elif char:  # \x (not a letter)
                self.__handle_char(char)
            elif word:  # \foo
                self.__handle_word(arg, word)
            elif hexa:  # \'xx
                self.__handle_hexa(hexa)
            elif tchar:
                self.__handle_tchar(tchar)

    def __handle_tchar(self, tchar):
        if self.__chars_left_to_skip > 0:
            self.__chars_left_to_skip -= 1
        elif not self.__is_ignorable_group:
            self.__out.append(tchar)

    def __handle_hexa(self, hexa):
        if self.__chars_left_to_skip > 0:
            self.__chars_left_to_skip -= 1
        elif not self.__is_ignorable_group:
            char = int(hexa, 16)
            if char > 127:
                self.__out.append(chr(char))  # NOQA
            else:
                self.__out.append(chr(char))

    def __handle_word(self, arg, word):
        self.__chars_left_to_skip = 0
        if word in self.__destinations:
            self.__is_ignorable_group = True
        elif self.__is_ignorable_group:
            pass
        elif word in self.__specialchars:
            self.__out.append(self.__specialchars[word])
        elif word == 'uc':
            self.__chars_to_skip_after_unicode = int(arg)
        elif word == 'u':
            self.__handle_word_u(arg)

    def __handle_word_u(self, arg):
        char = int(arg)
        if char < 0:
            char += 0x10000
        if char > 127:
            self.__out.append(chr(char))  # NOQA
        else:
            self.__out.append(chr(char))
        self.__chars_left_to_skip = self.__chars_to_skip_after_unicode

    def __handle_char(self, char):
        self.__chars_left_to_skip = 0
        if char == '~':
            if not self.__is_ignorable_group:
                self.__out.append('\xA0')
        elif char in '{}\\':
            if not self.__is_ignorable_group:
                self.__out.append(char)
        elif char == '*':
            self.__is_ignorable_group = True

    def __handle_brace(self, brace):
        self.__chars_left_to_skip = 0
        if brace == '{':
            self.__stack.append((self.__chars_to_skip_after_unicode, self.__is_ignorable_group))
        elif brace == '}':
            self.__chars_to_skip_after_unicode, self.__is_ignorable_group = self.__stack.pop()
