# numtxt - gives full and approximate written forms of numbers
# Copyright (C) 2017 - 2020, Philip Herd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import log
VERSION = '1.2.0'

# prefixes, suffixes and other words -----------------------
_noll_prefixes = {0: '',  # noll prefix definitions
  1: 'un',       10: 'dec',        100: 'cen',
  2: 'duo',      20: 'vigin',      200: 'duocen',
  3: 'tre',      30: 'trigin',     300: 'trecen',
  4: 'quattuor', 40: 'quadragin',  400: 'quadringen',
  5: 'quin',     50: 'quinquagin', 500: 'quingen',
  6: 'sex',      60: 'sexagin',    600: 'sescen',
  7: 'septen',   70: 'septuagin',  700: 'septingen',
  8: 'octo',     80: 'octogin',    800: 'octingen',
  9: 'novem',    90: 'nonagin',    900: 'nongen',}

_conway_prefixes = {0: ('', ''),  # conway-wechsler prefix definitions
  1: ('un', ''),       10: ('deci', 'n'),          100: ('centi', 'nx'),
  2: ('duo', ''),      20: ('viginti', 'ms'),      200: ('ducenti', 'n'),
  3: ('tre', 'sx'),    30: ('triginta', 'ns'),     300: ('trecenti', 'ns'),
  4: ('quattuor', ''), 40: ('quadraginta', 'ns'),  400: ('quadringenti', 'ns'),
  5: ('quin', ''),     50: ('quinquaginta', 'ns'), 500: ('quingenti', 'ns'),
  6: ('se', 'sx'),     60: ('sexaginta', 'n'),     600: ('sescenti', 'n'),
  7: ('septe', 'mn'),  70: ('septuaginta', 'n'),   700: ('septingenti', 'n'),
  8: ('octo', ''),     80: ('octoginta', 'mx'),    800: ('octingenti', 'mx'),
  9: ('nove', 'mn'),   90: ('nonaginta', ''),      900: ('nongenti', ''),}

# prefixes for noll and conway below 1000^10
_unts = ('n', 'm', 'b', 'tr', 'quadr', 'quint', 'sext', 'sept', 'oct', 'non')

_rowlett_prefixes = {0: '',  # rowlett prefix definitions (best guess)
  1: 'hen',   10: 'deka',       100: 'hecato',  # these prefixes should be
  2: 'do',    20: 'icosi',      200: 'diacosioi',  # checked
  3: 'tri',   30: 'triaconta',  300: 'triacosioi',
  4: 'tetra', 40: 'tetraconta', 400: 'tetracosioi',
  5: 'penta', 50: 'pentaconta', 500: 'pentacosioi',
  6: 'hexa',  60: 'hexaconta',  600: 'hexacosioi',
  7: 'hepta', 70: 'heptaconta', 700: 'heptacosioi',
  8: 'okta',  80: 'octaconta',  800: 'octacosioi',
  9: 'ennea', 90: 'enneaconta', 900: 'enneacosioi',}

_suffixes = {'noll': ('illion', 'tillion', 'illard', 'tillard'),
             'conway-wechsler': ('illion', 'illard'),
             'rowlett': ('illion',), 'knuth': ('yllion',)}

# SI prefixes in terms of powers of 1000
_si_prefixes = { 1: 'k',  2: 'M',  3: 'G',  4: 'T',
          0: '', 5: 'P',  6: 'E',  7: 'Z',  8: 'Y',
                -1: 'm', -2: 'u', -3: 'n', -4: 'p',
                -5: 'f', -6: 'a', -7: 'z', -8: 'y',}
_si_prefixes[-2] = '\u03bc' if type(3/2).__name__ == 'float' else 'u'
# * in terms of powers of ten
_si_prefixes_10 = {1: 'da', 2: 'h', -1: 'd', -2: 'c',}
_si_prefixes_10.update({i * 3: j for i, j in _si_prefixes.items()})

# SI prefix names in terms of powers of 1000
_si_pfx_names = { 1: 'kilo',   2: 'mega',   3: 'giga',   4: 'tera',
           0: '', 5: 'peta',   6: 'exa',    7: 'zetta',  8: 'yotta',
                 -1: 'milli', -2: 'micro', -3: 'nano',  -4: 'pico',
                 -5: 'femto', -6: 'atto',  -7: 'zepto', -8: 'yocto',}
# * in terms of powers of ten
_si_pfx_names_10 = {1: 'deca', 2: 'hecto', -1: 'deci', -2: 'centi'}
_si_pfx_names_10.update({i * 3: j for i, j in _si_pfx_names.items()})

# 0-99 names - used in _tens function
_tn_ones =  ('', 'one', 'two', 'three', 'four', 'five', 'six',
            'seven', 'eight', 'nine')
_tn_tees = {10: 'ten', 11: 'eleven', 12: 'twelve',
           13: 'thir', 15: 'fif', 18: 'eigh'}
_tn_tens =  {2: 'twen', 3: 'thir', 5: 'fif', 8: 'eigh'}
_tn_teesuf, _tn_tensuf= 'teen', 'ty'

# ordinals - used in ordinal function
_sh_ords = {0: 'th', 1: 'st', 2: 'nd', 3: 'rd'}
_lg_ords = {1: 'first', 2: 'second', 3: 'third', 5: 'fifth',
            8: 'eighth', 9: 'ninth', 12: 'twelfth', }

# other names - used in multiple functions
_zero, _hun, _thous = 'zero', 'hundred', 'thousand'
_neg = 'negative'#'minus'

# preset names - used in precedence and tuple functions
_pced = {0: 'nullary', 1: 'primary', 2: 'secondary', 3: 'tertiary',
         4: 'quaternary', 6: 'senary', 7: 'septenary', 8: 'octonary', }
_tupl = {0: 'empty', 1: 'single', 2: 'double', 3: 'triple'}
# not every word is defined here, some are in the functions that use them

# quick lookup tables --------------------------------------
_qk_tens = {}; _qk_noll = {}  # these are populated as needed
_qk_conw = {}; _qk_rowt = {}
_qk_pced = {}; _qk_tupl = {}
_qk_pced.update(_pced); _qk_tupl.update(_tupl)
_max_table_size = 2500  # don't let the quick lookup tables get too large

# methods and rules ----------------------------------------
methods = ('conway-wechsler', 'noll', 'rowlett', 'knuth')
current_method = methods[0]

suffix_styles = ('short', 'long', 'british')
current_style = suffix_styles[0]
_short_suf = True  # True for short style suffix, False for long style
_sub_long_suf = False  # True for old British style (_short_suf must be False)

# other ----------------------------------------------------
refs = ('References and related',
        '\'The Mathematical Gardner\' published 1981, pg 310-325',
        '\'The Book of Numbers\' published 1996, pg 15-16',
        'http://www.isthe.com/chongo/tech/math/number/number.html',
        'http://www.unc.edu/~rowlett/units/large.html',
        'http://www.mrob.com/pub/math/largenum.html#conway-wechsler',
        'http://www.mrob.com/pub/math/largenum-2.html#yllion',
        'https://en.wikipedia.org/wiki/Numeral_prefix',
        'https://en.wikipedia.org/wiki/Names_of_large_numbers',
        'https://en.wikipedia.org/wiki/Ordinal_number_%28linguistics%29',
        'http://verbmall.blogspot.com/2007/01/ordinal-numbers-revisited.html',
        'https://english.stackexchange.com/q/352146',
        'https://en.wikipedia.org/wiki/Arity',
        'https://en.wikipedia.org/wiki/Metric_prefix#List_of_SI_prefixes',
        )

__doc__ = """
number naming module
gives full and approximate written forms of numbers

There are currently four methods for naming numbers which can be set
 by setMethod. see 'methods' for a list of available methods to use.

 Default is 'conway-wechsler'.

Additionally, there are three styles for suffixes which can be set
 by setStyle. See 'suffix_styles' for a list of available styles.
 Note that not all naming methods adhere to these styles as some
 were made to remove the confusion the different styles can cause.

 Default is 'short'.
"""

__all__= ['approx', 'name', 'cardinal', 'ordinal', 'precedence', 'prefix',
          'uple', 'setMethod', 'setStyle', 'methods', 'current_method',
          'suffix_styles', 'current_style', 'VERSION', 'si', 'table',
          'gen10_dict', 'gen1k_dict', ]

# supporting functions and naming systems ------------------
def _ln(x, base=None):
    "adapter, allows log to be overridden by gmpy2/mpmath/whatever"
    if base is None: return log(x)
    else: return log(x) / log(base)

def _noll(n, suffix=True):
    "noll naming system\nreturns name of 1000^n"
    # http://www.isthe.com/chongo/tech/math/number/number.html
    # published 1994? (earliest date on website)
    if not n: return ''
    if n == 1: return _thous
    card = int(abs(n)) - 1  # cardinal is always one less

    prfs, unts = _noll_prefixes, _unts  # prefixes

    # suffix handling
    if current_method == 'knuth':  # knuth's method can be dependent on
        th, sfx = '', _suffixes['knuth'][0]  # noll's (default: conway's)
    else:
        sufs = _suffixes['noll']
        th, suf1, suf2 = '', sufs[0], sufs[1]
        if not _short_suf:  # long style
            if card % 2 or _sub_long_suf: pass
            else: suf1, suf2 = sufs[2], sufs[3]
            if _sub_long_suf and not card % 2 and card > 1:
                th = _thous + ' '  # old British style
            card = card // 2 + card % 2
        sfx = suf1 if 20 > (card % 100) > 9 or card < 11 else suf2

    name, mil = '', 0  # prefix construction
    if card < 10: return th + unts[card] + sfx
    while card:
        card, r = divmod(card, 1000)
        one, ten, hun = r % 10, ((r % 100) // 10) * 10, (r // 100) * 100
        sect = prfs[hun] + prfs[one] + prfs[ten]
        name = sect + ('milli' * mil if r else '') + name
        mil += 1

    un = prfs[1]  # name does not start with this when above 1000^1000
    if mil > 1 and name.startswith(un): name = name.replace(un, '', 1)
    if suffix: return th + name + sfx
    else: return th + name

def _conway(n, suffix=True):
    "conway-wechsler naming system\nreturns name of 1000^n"
    # http://www.mrob.com/pub/math/largenum.html#conway-wechsler
    # published 1996, pg 15-16 in 'The Book of Numbers'
    if not n: return ''
    if n == 1: return _thous
    card = int(abs(n)) - 1  # cardinal is always one less
    prfs, unts = _conway_prefixes, _unts  # prefixes

    # suffix handling
    if current_method == 'knuth':
        th, suf = '', _suffixes['knuth'][0]
    else:
        sufs = _suffixes['conway-wechsler']
        th, suf = '', sufs[0]
        if not _short_suf:  # suffix handling
            if card % 2 or _sub_long_suf: pass
            else: suf = sufs[1]
            if _sub_long_suf and not card % 2 and card > 1:
                th = _thous + ' '
            card = card // 2 + card % 2

    name = ''  # prefix construction
    while card:
        card, r = divmod(card, 1000)
        if r < 10: sect = unts[r]
        else:
            one, ten, hun = r % 10, ((r % 100) // 10) * 10, (r // 100) * 100
            ost, tst, hst = prfs[one], prfs[ten], prfs[hun]

            # check for matching joining letter (1 and 10 or 1 and 100 only)
            if one and ten: let = set(ost[1]) & set(tst[1])
            elif one and hun: let = set(ost[1]) & set(hst[1])
            else: let = set()

            ter = let.pop() if let else ''
            if one == 3 and ter: ter = 's'  # special case rule for 3
            sect = ost[0] + ter + tst[0] + hst[0]

        if sect[-1] in 'aeiou': sect = sect[:-1]  # strip last vowel
        name = sect + 'illi' + name if name else sect + name
    if suffix: return th + name + suf
    else: return th + name

def _rowlett(n, suffix=True):
    "rowlett naming system\nreturns name of 1000^n"
    # http://www.unc.edu/~rowlett/units/large.html - published 2001
    n = int(abs(n))

    # this method does not have short/long style suffixes
    suf, prfs = _suffixes['rowlett'][0], _rowlett_prefixes
    if n < 4: return ('', _thous, 'm' + suf, 'g' + suf)[n]  # special cases

    if n > 999:
        v = ValueError('input is too large')
        raise v  # rowlett did not give details for going above 1000^999

    mil, name = 0, ''  # prefix construction
    while n:
        n, r = divmod(n, 1000)

        one, ten, hun = r % 10, ((r % 100) // 10) * 10, (r // 100) * 100
        if r < 20: sect = prfs[one] + prfs[ten]  # guessing
        else: sect = prfs[ten] + prfs[one]

        sect = prfs[hun] + sect

        # my extension to this system (otherwise would stop at 1000^999)
        name = sect + ('chilia' * mil if r else '') + name
        mil += 1

    un = prfs[1]  # name does not start with this when above 1000^1000
    if mil > 1 and name.startswith(un): name = name.replace(un, '', 1)

    name = name.rstrip('aeiou')  # strip ending vowels (guessing)
    if suffix: return name + suf
    else: return name

def _knuth(n, condensed=False, lvl=0, comma=False, is_log=False):
    "knuth naming system"
    #last three variables are not for user use!
    # lvl - tracker for recursion level, used by self
    # is_log - flag for if n is the power of 1e4, 10000^n; used in approx func
    # comma - when to add a comma to the name, used by self
    # http://www.mrob.com/pub/math/largenum-2.html#yllion
    # published 1981, pg 310-325 in 'The Mathematical Gardner'
    if not n: return ''
    if n < 10000 and not is_log:
        if condensed:
            return str(n)
        else:
            a = _tens(n // 100) if n // 100 else ''
            b = _tens(n % 100) if n % 100 else ''
            if a: a += (' ' + _hun) + (' ' if b else '')
            return a + b

    if is_log:
        p = int(_ln(n, 2))
        base = 2 ** p
    else:  # p is also the deepest the recursion can go
        p = int(_ln(_ln(n, 10000), 2))
        base = 10000 ** (2 ** p)
    d, r = divmod(n, base)

    # if called directly but method was not set to knuth
    prior_setting = None
    if not lvl and setMethod() != 'knuth':
        prior_setting = setMethod()
        setMethod('knuth')

    # knuth's method can use either noll's or conway's
    # but should use conway's as that follows
    # Roman syntax more closely than noll's
    if p: pfx = _conway(p+1)#_noll(p+1)
    else: pfx = 'myriad'
    if not is_log: pfx += (', ' if not comma else ' ')

    recur = _knuth
    if is_log:
        if n == 1: return pfx
        frnt = recur(r, 0, lvl+1, 0, is_log)
        back = ''
    else:
        frnt = recur(d, condensed, lvl+1, comma+1)
        back = recur(r, condensed, lvl+1, comma)

    name = filter(None, (frnt, ' ' + pfx, back))
    if not lvl and prior_setting: setMethod(prior_setting)
    return ''.join(name).strip(', ')

def _tens(n):
    "converts 0 to 99 to their names"
    name, n = '', abs(n) % 100
    if not n: return _zero
    elif n < 10: return _tn_ones[n]
    elif 9 < n < 20:
        if n in [13, 15, 18]: return _tn_tees[n] + _tn_teesuf
        elif n > 13: return _tn_ones[n-10] + _tn_teesuf
        else: return _tn_tees[n]
    else:
        if n // 10 in [2, 3, 5, 8]: name = _tn_tens[n // 10] + _tn_tensuf
        else: name =_tn_ones[n // 10] + _tn_tensuf
        if not n % 10: return name
        else: return name + '-' + _tn_ones[n % 10]

# main functions -------------------------------------------
def approx(n, fmt=None):
    """approximates n
    if n is a string, returns the name of 1000^n instead*

    approx(2.12345e+48) ----------------> '2.123 quindecillion'
    approx(2.12345e+48, fmt='{:7.3f}') -> '  2.123 quindecillion'

    if working with another module (gmpy2, mpmath, Decimal)
    the log function may be overridden for compatibility:
    >>> import numtxt
    >>> import gmpy2 as gm
    >>> x = gm.mpfr('123.456e+7890')
    >>> numtxt.approx(x)
    OverflowError: cannot convert float infinity to integer
    >>> numtxt.log = gm.log
    >>> numtxt.approx(x)
    '123.456 billinovemvigintisescentillion'

    *returns name of 10000^n if naming method is knuth
    """
    sgn, mthd = '', current_method
    base = 10000 if mthd == 'knuth' else 1000  # in order to be correct

    # parse input
    if type(n).__name__ in ('str', 'unicode'):  # power of 1000
        n = n.replace(',', '.')
        if '-' in n:  # negative power, return with ordinal
            n = n.replace('-', '')
            return approx(n) + _sh_ords[0]
        if '.' in n:  # floating power
            c, a = n.split('.')
            pwr = int(c)
            # what to do to remove the footnote in the docstring above
            #if mthd == 'knuth':
            #    a = float('0.' + a) * .75 + (pwr * .75) % 1
            #    pwr = int(pwr * .75 + a % 1)
            #    a = '{:.9f}'.format(a).split('.')[-1]
            apx = base ** float('0.' + a)
        else:  # whole power
            pwr = int(n)
            apx = 1
            #if mthd == 'knuth':  # to remove the footnote above
            #    p, a = '{:.9f}'.format(pwr * 0.75).split('.')
            #    pwr = int(p)
            #    apx = base ** float('0.' + a)
    elif not n or abs(n) < base:  # small value
        return str(int(round(n)))
        #if abs(n) < 10.0 / base:  # for really small values
        #    lgg = _ln(n, base)
        #    # decimal module just has to be so off from everything else
        #    if type(lgg).__name__ == 'Decimal':  # decimal floor
        #        lgg = int(lgg - lgg % 1 - (1 if lgg < 0 else 0))
        #    else: lgg -= (lgg % 1)  # flooring anything else
        #    return approx(n * base ** (2 * abs(lgg))) + _sh_ords[0]
        #    # or get power of lowest digit?: 1.25e-12 -> b = -14
        #    # then a = int(round(1.25e-12 * 10 ** abs(b)))
        #    # return name(a) + ' ' + name(10 ** abs(b)) + 'ths' ?
        #else: return str(int(round(n)))
    else:  # ints, floats, longs
        if n < 0: sgn, n = '-', abs(n)
        lgg = round(_ln(n, base), 9)
        pwr = int(lgg)
        apx = base ** (lgg - pwr)

    # select method and use
    apx_fmt = '{:0.3f} '#'{:7.3f} '
    if mthd == 'noll':
        try:
            nme = _qk_noll[pwr]  # lookup table
        except KeyError:
            nme = _noll(pwr)  # fallback
            if len(_qk_noll) < _max_table_size:
                _qk_noll[pwr] = nme  # store for next time

    elif mthd in ('conway', 'conway-wechsler'):
        try:
            nme = _qk_conw[pwr]
        except KeyError:
            nme = _conway(pwr)
            if len(_qk_conw) < _max_table_size:
                _qk_conw[pwr] = nme

    elif mthd == 'rowlett':
        try:
            nme = _qk_rowt[pwr]
        except KeyError:
            nme = _rowlett(pwr)
            if len(_qk_rowt) < _max_table_size:
                _qk_rowt[pwr] = nme

    elif mthd == 'knuth':
        nme = _knuth(pwr, is_log=True)
        apx_fmt = '{:0.4f} '

    else:  # any undefined method defaults to conway
        nme = _conway(pwr)

    apx_fmt = apx_fmt if fmt is None else fmt
    if apx_fmt[-1] != ' ': apx_fmt = apx_fmt + ' '

    return sgn + apx_fmt.format(apx) + nme

def name(n, condensed=False):
    """returns the cardinal name of n
    12000000 -> 'twelve million' (condensed=False)
    12000000 -> '12 million' (condensed=True)
    """
    if not n: return _zero
    sgn = '' if n > 0 else ('- ' if condensed else _neg + ' ')
    n, nam, pwr = abs(int(n)), '', 0
    mthd = current_method

    # select method
    if mthd == 'noll':
        func = _noll
        tabl = _qk_noll
    elif mthd in ('conway', 'conway-wechsler'):
        func = _conway
        tabl = _qk_conw
    elif mthd == 'rowlett':
        func = _rowlett
        tabl = _qk_rowt
    elif mthd == 'knuth':  # this method's build is in the func, so return it
        return sgn + _knuth(n, condensed).strip(' ,')
    else: func = _conway  # any undefined method defaults to conway

    while n:  # build name
        n, r = divmod(n, 1000)

        # don't have 'zero -illion' names
        if not r and pwr:
            pwr += 1
            continue

        # section name
        if condensed:
            sect = str(r) + ' ' if r else ''
        else:
            t, h = r // 100, r % 100
            try:  # lookup table
                tn = _qk_tens[t]
                hu = _qk_tens[h]
            except KeyError:  # fallback
                tn = _tens(t)
                hu = _tens(h)
                _qk_tens[t] = tn  # store for next time
                _qk_tens[h] = hu

            hun = (tn + ' ' + _hun + ' ') if t else ''
            ten = (hu + ' ') if h else ''
            sect = hun + ten

        # power name
        try:
            tho = tabl[pwr]
        except KeyError:
            tho = func(pwr)
            if len(tabl) < _max_table_size:
                tabl[pwr] = tho  # store for later use

        nam = sect + tho + ', ' + nam
        pwr += 1

    return (sgn + nam).strip(' ,')

def cardinal(n, condensed=False): return name(n, condensed)
cardinal.__doc__ = name.__doc__

def ordinal(n, short=False):
    """returns the ordinal name of n
    3 -> 'third' (short=False)
    3 -> '3rd' (short=True)
    """
    so, lo = _sh_ords, _lg_ords
    if short:
        th = so[0] if 9 < abs(n) % 100 < 14 else so.get(abs(n) % 10, so[0])
        nme = str(n) + th
    else:
        nme, lst = name(n), abs(n) % 100

        if lst > 19 and lst % 10: lst %= 10

        if lst in lo:  # special cases
            nme = nme.rsplit(name(lst), 1)[0]
            nme += lo[lst]
        elif not lst % 10 and lst > 19:  # 20, 30, 40, ...
            nme = nme.replace('y', 'ieth')
        else: nme += so[0]
    return nme

def precedence(n):
    """returns the precedence name of n
    1 -> 'primary'
    2 -> 'secondary'
    """
    cur_sty = setStyle()
    setStyle('short')
    n = abs(int(n))

    try:  # lookup table
        pcd = _qk_pced[n]
    except KeyError:  # fallback
        pcd = _conway(n + 1, False)
        # naming rules for precedence
        if pcd[-1] == 'c': pcd = pcd[:-1] + 'n'
        if pcd[-1] == 't': pcd = pcd[:-1]
        # the above rules allows the fewest preset names
        # matched with known spellings
        pcd = pcd + 'ary'

        if len(_qk_pced) < _max_table_size:
            _qk_pced[n] = pcd  # store for next time

    setStyle(cur_sty)
    return pcd

def uple(n):
    """returns the tuple name of n
    1 -> 'single'
    2 -> 'double'
    """
    n = abs(int(n))
    cur_sty = setStyle()
    setStyle('short')

    try:  # lookup table
        tup = _qk_tupl[n]
    except KeyError:  # fallback
        tup = _conway(n + 1, False)
        tup = tup + 'uple'

        if len(_qk_tupl) < _max_table_size:
            _qk_tupl[n] = tup  # store for next time

    setStyle(cur_sty)
    return tup

def prefix(n, suffix=''):
    "generates the prefix of n"
    suf = str(suffix)
    if current_method == 'noll': func = _noll
    elif current_method == 'rowlett': func = _rowlett
    else: func = _conway
    # knuth's method doesn't lend itself to prefixes well, as it's not
    # building the name itself (it uses conway's) but rather it builds
    # how the names are organized. As such, it's left of out this func
    return func(n + 1, False) + suf

def si(n, unit=None, **kwargs):
    """approximates n with SI prefixes
    si(299792458/475e-09, 'Hz') -> '631.142 THz'

    to use power of ten prefixes (hecto, deca, deci, centi), set base to 10:
    si(123) ----------> '123.000'
    si(123, base=10) -> '1.230 h'

    to use full prefix name (tera instead of T), set name to True:
    si(5.137e12) ------------> '5.137 T'
    si(5.137e12, name=True) -> '5.137 tera'
    si(5.137e12, Name=True) -> '5.137 Tera'  # Capitalized

    to change number formatting, set fmt to custom float format:
    si(9876543210) ----------------> '9.877 G'
    si(9876543210, fmt='{:6.2f}') -> '  9.88 G'
    """
    base = kwargs.get('base', 1e3)
    pfx = _si_prefixes_10 if base == 10 else _si_prefixes
    if kwargs.get('name') or kwargs.get('Name'):
        pfx = _si_pfx_names_10 if base == 10 else _si_pfx_names
        if 'Name' in kwargs: pfx = {i: j.capitalize() for i, j in pfx.items()}
    fmt = kwargs.get('fmt', '{:0.3f}')#'{:7.3f}'

    lg = _ln(abs(n) or 1, base)
    pw = int(lg - lg % 1)  # floor, without importing
    mx = max(pfx.keys())  # if SI adds more, update the prefix dict

    sgn = '' if n >= 0 else '-'
    unit = str(unit) if unit is not None else ''
    if abs(pw) > mx: pw = pw // abs(pw) * mx  # don't pass pfx limits
    pw = max(filter(lambda z: z <= pw, pfx))  # floor to nearest pfx

    si_str = fmt.format(float(base) ** float(lg - pw) if n else 0)
    return (sgn + si_str + ' ' + pfx[pw] + unit).rstrip()

# settings functions ---------------------------------------
def setMethod(method=None):
    """sets the naming method
    pass None to see current method
    """
    global current_method, methods
    mthds = methods + ('conway', )  # shortened form for conway-wechsler

    if str(method).lower() not in mthds and method != None:
        v = TypeError('invalid method')
        raise v

    if method != None: current_method = method.lower()
    return current_method

def setStyle(style=None):
    """sets the suffix style
    pass None to see current style

    'short' -> million, billion, trillion, quadrillion...
    'long' -> million, milliard, billion, billiard...
    'british' -> million, thousand million, billion, thousand billion...
    """
    global _short_suf, _sub_long_suf, suffix_styles, current_style
    global _qk_noll, _qk_conw  # these change based on the style

    if str(style).lower() not in suffix_styles and style != None:
        v = TypeError('invalid style')
        raise v

    if style is None or style.lower() == current_style:
        return current_style
    elif style.lower() == 'short':
        _short_suf = True
        _sub_long_suf = False
    elif style.lower() == 'long':
        _short_suf = False
        _sub_long_suf = False
    elif style.lower() == 'british':
        _short_suf = False
        _sub_long_suf = True

    _qk_noll = {}; _qk_conw = {}  # must be cleared to match new style
    current_style = style.lower()
    return current_style

# additional functions -------------------------------------
def gen10_dict(n):
    "generate powers of ten names; {10^i: ith-illion}"
    return {i: approx(10 ** i).strip('1.0 ') for i in range(0, (n+1)*3, 3)}

def gen1k_dict(n):
    "generate powers of thousand names; {1000^i: ith-illion}"
    return {i: approx(str(i)).strip('1.0 ') for i in range(n + 1)}

def table(n):
    "generate & print a word table"
    heads = ['n', 'cardinal', 'ordinal', 'precedence', 'tuple']#, '1000^n']
    funcs = [str, cardinal, ordinal, precedence, uple]#, _conway]

    h = len(heads); ln = '|'.join([' {:^{}} '] * h)
    ls = [[f(i) for f in funcs] for i in range(n + 1)]
    mx = [len(max([q[j] for q in ls] + [heads[j]],key=len)) for j in range(h)]

    print(ln.format(*[q for u in zip(heads, mx) for q in u]))
    print('+'.join(['-' * (i + 2) for i in mx]))  # +2 for spacing
    for i in ls: print(ln.format(*[q for u in zip(i, mx) for q in u]))


# flooring with gmpy2.mpfr, mpmath.mpf and decimal.Decimal
#  floor division (//) is not supported by mpf, nor does it work right with Decimal (-1.2345//1 should be -2 but it gives -1)
#  modulo operation(%) (as in x - x%1 to floor) works with mpfr and mpf, but not with Decimal (it keeps the numerator sign)
#  int(x - abs(x) % 1) - (1 if x < 0 and int(x) != x else 0) works with all three
# ceiling is floor + 1
