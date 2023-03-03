def update_parent_semver(parent_semver, *product_semvers):
    """Takes a variable number of tuples containing old and new semvers from multiple products and updates their parent semver.

    Parameters
    ----------
    parent_semver
        The SemVer2 version of the parent that contains the child products.
    product_semvers
        A variable number of product tuples containing old and new SemVer2 versions e.g. ('1.2.3', '1.2.4')
    
    Returns
    -------
    Updated SemVer2 version for the parent.
    
    Raises
    ------
    TypeError if any semver is invalid or a product semver is not a tuple of two elements (old semver, new semver).
    
    Notes
    -----
    Any extension to the core SemVer2 standard is ignored e.g. build numbers, pre-release tags etc.
    For the SemVer2 standard, see https://semver.org/
    
    Examples
    --------
    >>> update_parent_semver('3.3.3', ('1.2.3', '1.2.6+123'), ('2.1.0-1.2.3', '2.1.2-beta+exp.sha.5114f85'))
    '3.3.4'
    
    >>> update_parent_semver('3.3.3', ('1.2.3', '1.3.0'), ('2.1.0-alpha', '2.1.0-beta'))
    '3.4.0'
    
    >>> update_parent_semver('3.3.3', ('1.2.3', '1.3.0'), ('2.1.0', '3.0.0'))
    '4.0.0'

    >>> update_parent_semver('3.3.3')
    '3.3.3'

    >>> update_parent_semver('3.3.3', ('1.2.3', '1.3.0'), ('2.1.0', '2.2.0'), ('1.4.1', '1.6.0'))
    '3.4.0'
    """
    import re
    
    # SemVer2 standard regular expression (from https://semver.org/)
    sv2 = re.compile(r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')
    
    # validate all semvers
    if not sv2.match(parent_semver):
        raise TypeError("parent_semver not a valid SemVer2 string")

    for versions in product_semvers:
        if len(versions) != 2:
            raise TypeError("product_semvers must be two-element tuples (old semver, new semver)")
        for version in versions:
            if not sv2.match(version):
                raise TypeError("a product_semvers tuple element is not a valid SemVer2 string")

    # find differential between old and new versions across all products
    # note: this ignores differential build numbers and pre-release tags
    differential = None
    for versions in product_semvers:
        old = sv2.match(versions[0])
        new = sv2.match(versions[1])

        if old.group('major') != new.group('major') and differential != 'major':
            differential = 'major'
        elif old.group('minor') != new.group('minor') and differential != 'minor':
            differential = 'minor'
        elif old.group('patch') != new.group('patch') and not differential:
            differential = 'patch'

    # apply differential to parent semver
    parent = sv2.match(parent_semver)
    major = int(parent.group('major'))
    minor = int(parent.group('minor'))
    patch = int(parent.group('patch'))

    if differential == 'major':
        major += 1
        minor = patch = 0
    elif differential == 'minor':
        minor += 1
        patch = 0
    elif differential == 'patch':
        patch += 1

    return f'{major}.{minor}.{patch}'
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()    








