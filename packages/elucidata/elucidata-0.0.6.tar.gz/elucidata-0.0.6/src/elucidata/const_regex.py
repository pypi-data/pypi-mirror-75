'''
Fichier contenant les constantes RegEx utilisé par notre module. 
'''

REG_s = '[ \t\n\r\f\v]'  # explicitation du RegEx '\s'
REG_S = '[^ \t\n\r\f\v]'  # explicitation du RegEx '\S'
REG_d = '[0-9]'  # explicitation du RegEx '\d'
REG_D = '[^0-9]'  # explicitation du RegEx '\D'
REG_w = '[a-zA-Z0-9_]'  # explicitation du RegEx '\w'
REG_W = '[^a-zA-Z0-9_]'  # explicitation du RegEx '\W'

BALISE_SQL = '[(DECLARE)(BEGIN)(END)]*'

REGEX_MULTILIGNE = '(' + '/\\*' + '(.|[\r\n])*?' + '\\*/' + ')'
REGEX_INLINE = '(' + '--.*' + '|' + '#.*' + ')'
REGEX_LIGNE_VIDE = '^' + '(' + REG_s + '*' + BALISE_SQL + REG_s + '*' +')' + '$'
# REGEX_LIGNE_VIDE = '^' + REG_s + '*' + '$'   ---sans balise---
REGEX_TOUT = '(.|[\r\n])*?'
