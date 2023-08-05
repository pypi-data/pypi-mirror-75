import re


def all_until(pattern: str, string: str, include_pattern: bool = False) -> str:
    """
    Return string from begining to regex pattern.
    Args:
        pattern:str: Regex pattern to find.
        string:str: Sentence to find the pattern.
        include_pattern:bool: Inclclude or not the pattern into return string.
    Returns:
        str: String found.
    Example:
        all_until('\\d', 'The 7 number.', include_pattern=True) # return: 'The 7'
        all_until('\\d', 'The 7 number.', include_pattern=False) # return: 'The '
    """
    if include_pattern:
        comp = re.compile(rf'(.*)({pattern})')
        result = comp.findall(string)
        return ''.join(result[0]) if result else None
    else:
        comp = re.compile(rf'(.*)(?={pattern})')
        result = comp.findall(string)
        return result[0] if result else None


def all_after(pattern: str, string: str, include_pattern: bool = False) -> str:
    """
    Return string from begining to regex pattern.
    Args:
        pattern:str: Regex pattern to find.
        string:str: Sentence to find the pattern.
        include_pattern:bool: Inclclude or not the pattern into return string.
    Returns:
        str: String found.
    Example:
        all_after('\\d', 'The 7 number.', include_pattern=True) # return: '7 number.'
        all_after('\\d', 'The 7 number.', include_pattern=False) # return: ' number.'
    """
    if include_pattern:
        comp = re.compile(rf'({pattern})(.*)')
        result = comp.findall(string)
        return ''.join(result[0]) if result else None
    else:
        comp = re.compile(rf'(?<={pattern})(.*)')
        result = comp.findall(string)
        return result[0] if result else None


def first_match(pattern: str, string: str) -> str:
    """
    Return the first regex match pattern found in the string.
    Args:
        pattern:str: Regex pattern to find.
        string:str: Sentence to find the pattern.
    Returns:
        str: String found.
    Example:
        first_match('\\d', 'The 7 number.', include_pattern=True) # return: '7'
    """
    comp = re.compile(rf'{pattern}')
    result = comp.findall(string)
    return result[0] if result else None


def get_full_url(string: str, domain=None) -> str:
    """
    Return full url from the first match in a string.
    Args:
        string:str: Text to find the full url.
        domain:str: Domain to find ex. 'www.falabella.com' 
    Returns:
        str: Full url found. ex: 'https://www.falabella.com/falabella-cl/product/9432811'
    """
    if domain:
        comp = re.compile(
            rf'(http|ftp|https)(://)({domain})([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    else:
        comp = re.compile(
            rf'(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    result = comp.findall(string)
    return "".join(result[0]) if result else None
