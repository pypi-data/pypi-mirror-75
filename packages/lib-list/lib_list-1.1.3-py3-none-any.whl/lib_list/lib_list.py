# STDLIB
import fnmatch
import sys
from typing import Any, List, Union


def str_in_list_non_case_sensitive(string: str, list_of_strings: List[str]) -> bool:
    """
    >>> str_in_list_non_case_sensitive('aba',['abc','cde'])
    False
    >>> str_in_list_non_case_sensitive('aBa',['abc','Aba'])
    True
    """
    string = string.lower()
    list_of_strings = [my_string.lower() for my_string in list_of_strings]
    if string in list_of_strings:
        return True
    else:
        return False


def del_double_elements(list_elements: List[Any]) -> List[Any]:
    """
    >>> del_double_elements([])
    []
    >>> sorted(del_double_elements(['c','b','a']))
    ['a', 'b', 'c']
    >>> sorted(del_double_elements(['b','a','c','b','a']))
    ['a', 'b', 'c']
    """

    if not list_elements:  # leere Liste oder None wieder unverändert retournieren
        return list_elements
    return list(set(list_elements))


def str_in_list_to_lower(list_of_strings: List[str]) -> List[str]:
    """
    >>> str_in_list_to_lower(['A','b','C'])
    ['a', 'b', 'c']

    """
    if not list_of_strings:  # leere Liste oder None wieder unverändert retournieren
        return list_of_strings

    return [string.lower() for string in list_of_strings]


def str_in_list_lower_and_de_double(list_of_strings: List[str]) -> List[str]:
    if not list_of_strings:  # leere Liste oder None wieder unverändert retournieren
        return list_of_strings
    list_of_strings_lower = str_in_list_to_lower(list_of_strings=list_of_strings)
    list_of_strings_lower_and_de_double = del_double_elements(list_elements=list_of_strings_lower)
    return list_of_strings_lower_and_de_double


def ls_strip_elements(ls_elements: List[str], chars: Union[None, str] = None) -> List[str]:
    """
    >>> ls_strip_elements(['  a','bbb','   '])
    ['a', 'bbb', '']
    >>> ls_strip_elements([])
    []

    """

    if (not ls_elements) or (ls_elements is None):  # leere Liste oder None wieder unverändert retournieren
        return list()
    return [s_element.strip(chars) for s_element in ls_elements]


def ls_rstrip_elements(ls_elements: List[str], chars: Union[None, str] = None) -> List[str]:
    """
    >>> ls_rstrip_elements(['  a','bbb','c   '])
    ['  a', 'bbb', 'c']
    >>> ls_rstrip_elements([])
    []

    """

    if (not ls_elements) or (ls_elements is None):  # leere Liste oder None wieder unverändert retournieren
        return list()
    return [s_element.rstrip(chars) for s_element in ls_elements]


def ls_strip_list(list_of_strings: List[str], chars: str = '') -> List[str]:
    """
    strips list elements of a list, were the value is chars
    >>> testlist = ['','','a','b','c','','']
    >>> ls_strip_list(testlist)
    ['a', 'b', 'c']

    """

    list_of_strings = ls_lstrip_list(list_of_strings, chars)
    list_of_strings = ls_rstrip_list(list_of_strings, chars)
    return list_of_strings


def ls_lstrip_list(list_of_strings: List[str], chars: str = '') -> List[str]:
    """
    strips list elements on the beginning of a list, were the value is chars
    >>> testlist = ['','','a','b','c','','']
    >>> ls_lstrip_list(testlist)
    ['a', 'b', 'c', '', '']
    >>> testlist = []
    >>> ls_lstrip_list(testlist)
    []
    """
    while list_of_strings and list_of_strings[0] == chars:
        list_of_strings = list_of_strings[1:]
    return list_of_strings


def ls_rstrip_list(list_of_strings: List[str], chars: str = '') -> List[str]:
    """
    strips list elements on the beginning of a list, were the value is chars
    >>> testlist = ['','','a','b','c','','']
    >>> ls_rstrip_list(testlist)
    ['', '', 'a', 'b', 'c']
    >>> testlist = []
    >>> ls_rstrip_list(testlist)
    []

    """
    while list_of_strings and list_of_strings[-1] == chars:
        list_of_strings = list_of_strings[:-1]
    return list_of_strings


def ls_del_empty_elements(ls_elements: List[Any]) -> List[Any]:
    """
    >>> ls_del_empty_elements([])
    []
    >>> ls_del_empty_elements(['',''])
    []
    >>> ls_del_empty_elements(['','','a',None,'b'])
    ['a', 'b']
    >>> ls_del_empty_elements(['   ','','a',None,'b'])
    ['   ', 'a', 'b']
    >>> ls_del_empty_elements(['   ','','a',None,'b',0])
    ['   ', 'a', 'b']

    """

    return list(filter(None, ls_elements))


def ls_strip_afz(ls_elements: List[str]) -> List[str]:
    # Entfernt die Anführungszeichen für alle Elemente einer Liste mit Strings.
    # ['"  a"',"'bbb'",'ccc'] --> ['  a','bbb','ccc']

    if (not ls_elements) or (ls_elements is None):  # leere Liste oder None wieder unverändert retournieren
        return []

    ls_newelements = []
    for s_element in ls_elements:
        # Anführungszeichen aus dem Value entfernen
        s_element = s_element.strip()
        if (s_element.startswith('"') and s_element.endswith('"')) or (s_element.startswith("'") and s_element.endswith("'")):
            s_element = s_element[1:-1]
        ls_newelements.append(s_element)
    return ls_newelements


def ls_double_quote_if_contains_blank(ls_elements: List[str]) -> List[str]:
    if (not ls_elements) or (ls_elements is None):  # leere Liste oder None wieder unverändert retournieren
        return []

    ls_newelements = []
    for s_element in ls_elements:
        if ' ' in s_element:
            s_element = '"' + s_element + '"'
        ls_newelements.append(s_element)
    return ls_newelements


def is_str_in_list_elements(ls_elements: List[str], s_search_string: str) -> bool:
    """ delivers true, if one of the strings in the list contains (or is equal) the searchstring """

    if not ls_elements:   # leere Liste no match, return False
        return False

    for s_element in ls_elements:
        if type(s_element) == str:
            if s_search_string in s_element:
                return True
    return False


def ls_del_elements_containing(ls_elements: List[str], s_search_string: str) -> List[str]:
    """
    entferne jene Elemente deren Typ str ist und die s_search_string enthalten.
    gib alle anderen Elemente unverändert retour.

    :param ls_elements:                 eine Liste mit Elementen
    :param s_search_string:             der Suchstring

    :return:                            eine Liste mit den Resultaten
    """
    if (not ls_elements) or (not s_search_string):  # leere Liste oder None wieder unverändert retournieren
        return ls_elements

    ls_results = []
    for s_element in ls_elements:
        if s_search_string not in s_element:
            ls_results.append(s_element)
    return ls_results


def get_list_elements_containing(ls_elements: List[str], s_search_string: str) -> List[str]:
    """
    liefere jene Elemente deren Typ str ist und s_search_string enthalten.

    :param ls_elements:                 eine Liste mit Elementen
    :param s_search_string:             der Suchstring

    :return:                            eine Liste mit den Resultaten
    """
    if (not ls_elements) or (not s_search_string):  # leere Liste oder None wieder unverändert retournieren
        return ls_elements

    ls_results = []
    for s_element in ls_elements:
        if type(s_element) == str:
            if s_search_string in s_element:
                ls_results.append(s_element)
            else:
                continue
    return ls_results


def ls_elements_replace_strings(ls_elements: List[str], s_old: str, s_new: str) -> List[str]:
    """
    führe ein <str>.replace(s_old, s_new) in allen Elementen der Liste durch, welche vom Typ str sind

    :param ls_elements:                 eine Liste mit Elementen
    :param s_old:                       die zu Ersetzenden Zeichen
    :param s_new:                       die neuen Zeichen

    :return:                            eine Liste mit den Resultaten

    """

    if not ls_elements:  # leere Liste oder None wieder unverändert retournieren
        return ls_elements

    ls_results = []
    for s_element in ls_elements:
        if type(s_element) == str:
            s_element = s_element.replace(s_old, s_new)
        ls_results.append(s_element)
    return ls_results


def is_list_element_fnmatching(ls_elements: List[str], s_fnmatch_searchpattern: str) -> bool:
    """
    liefere True wenn einer der Elemente den s_searchstring (fnmatch) enthält

    :param ls_elements:                 eine Liste mit Elementen
    :param s_fnmatch_searchpattern:     der Suchstring

    :return:                            b_ls_fnmatching_searchstring
    """

    if (not ls_elements) or (ls_elements is None):  # leere Liste no match, return False
        return False

    b_ls_fnmatching_searchstring = False
    for s_element in ls_elements:
        if type(s_element) == str:
            if fnmatch.fnmatch(s_element, s_fnmatch_searchpattern):
                b_ls_fnmatching_searchstring = True
                break

    return b_ls_fnmatching_searchstring


def get_elements_fnmatching(ls_elements: List[str], s_fnmatch_searchpattern: str) -> List[str]:
    """
    liefere jene Elemente deren Typ str ist und s_fnmatch_searchpattern enthalten.

    :param ls_elements:                 eine Liste mit Elementen
    :param s_fnmatch_searchpattern:     der Suchstring

    :return:                            eine Liste mit den Resultaten

    """
    if not ls_elements:  # leere Liste oder None wieder unverändert retournieren
        return ls_elements

    ls_results = []
    for s_element in ls_elements:
        if type(s_element) == str:
            if fnmatch.fnmatch(s_element, s_fnmatch_searchpattern):
                ls_results.append(s_element)
            else:
                continue
    return ls_results


def is_list_element_l_fnmatching(ls_elements: List[str], ls_fnmatch_searchpattern: List[str]) -> bool:
    """
    liefere True wenn eines der ls_elements einen der ls_searchstrings (fnmatch) enthält

    :param ls_elements:                 eine Liste mit Elementen
    :param ls_fnmatch_searchpattern:   eine Liste von Suchstrings

    :return:    True, wenn eines der Listenelemente einen der searchpatterns enthält.
    :raises:    None

    """

    if not ls_elements:                 # leere Liste no match, return False
        return False

    if not ls_fnmatch_searchpattern:   # leere Liste no match, return False
        return False

    for s_fnmatch_searchpattern in ls_fnmatch_searchpattern:
        if fnmatch.filter(ls_elements, s_fnmatch_searchpattern):
            return True

    return False


def strip_and_add_non_empty_args_to_list(*args: Any) -> List[Any]:
    """
    erzeuge eine Liste von Argumenten, leere Argumente werden nicht in die Liste aufgenommen
    Status:        Production
    Input :        eine beliebige Anzahl von Argumenten z.Bsp. "a","b","c","","d"
    Output:        ["a","b","c","d"]
    Exceptions:    Exception bei Fehler
    """

    if (not args) or (args is None):  # leere Liste oder None wieder unverändert retournieren
        return list()

    ls_args = []
    for s_arg in args:
        s_arg = s_arg.strip()
        if s_arg:
            ls_args.append(s_arg)
    return ls_args


def ls_substract(ls_minuend: List[Any], ls_subtrahend: List[Any]) -> List[Any]:
    """
    subtrahiere Liste l_subtrahend von Liste l_minuend
    wenn ein Element in Liste l_minuend mehrfach vorkommt, so wird nur ein Element abgezogen :

    >>> l_minuend = ['a','a','b']
    >>> l_subtrahend = ['a','c']
    >>> ls_substract(l_minuend, l_subtrahend)
    ['a', 'b']

    """
    for s_element in ls_subtrahend:
        if s_element in ls_minuend:
            ls_minuend.remove(s_element)
    return ls_minuend


def l_substract_all_keep_sorting(l_minuend: List[Any], l_subtrahend: List[Any]) -> List[Any]:
    """
    subtrahiere Liste l_subtrahend von Liste l_minuend
    wenn ein Element in Liste l_minuend mehrfach vorkommt, so werden alle Elemente abgezogen :
    die Sortierung wird beibehalten !
    >>> l_minuend = ['a','a','b']
    >>> l_subtrahend = ['a','c']
    >>> l_substract_all_keep_sorting(l_minuend, l_subtrahend)
    ['b']

    """
    l_subtrahend = list(set(l_subtrahend))
    for s_element in l_subtrahend:
        while s_element in l_minuend:
            l_minuend.remove(s_element)
    return l_minuend


def l_substract_unsorted_fast(ls_minuend: List[Any], ls_subtrahend: List[Any]) -> List[Any]:
    """
    subtrahiere Liste ls_subtrahend von Liste ls_minuend
    wenn ein Element in Liste ls_minuend mehrfach vorkommt, so werden alle Elemente abgezogen
    die Sortierung wird NICHT beibehalten !
    >>> ls_minuend = ['a','a','b']
    >>> ls_subtrahend = ['a','c']
    >>> l_substract_unsorted_fast(ls_minuend, ls_subtrahend)
    ['b']

    """
    l_result = list(set(ls_minuend) - set(ls_subtrahend))
    return l_result


def split_list_into_junks(source_list: List[Any], junk_size: int = sys.maxsize) -> List[List[Any]]:
    """
    divides a List into Junks

    >>> result = split_list_into_junks([1,2,3,4,5,6,7,8,9,10],junk_size=11)
    >>> assert result == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]

    >>> result = split_list_into_junks([1,2,3,4,5,6,7,8,9,10],junk_size=3)
    >>> assert result == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    >>> result = split_list_into_junks([1,2,3,4,5,6,7,8,9,10])
    >>> assert result == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]

    """
    l_lists = []
    remaining_list = source_list

    while len(remaining_list) > junk_size:
        part_list = remaining_list[:junk_size]
        l_lists.append(part_list)
        remaining_list = remaining_list[junk_size:]
    l_lists.append(remaining_list)
    return l_lists
