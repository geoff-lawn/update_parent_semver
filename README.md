# update_parent_semver.py
Update an "owning" parent's SemVer2 version from a group of child item's versions.

Useful for situations where you have the need for SemVer2 version management for a group of items each with their own SemVer2 versions.

## Example
You have three items each with their own SemVer2 versions:
- Item1 previous version: '1.2.3-beta', current version: '1.2.4'
- Item2 previous version: '2.1.1+123', current version: '2.2.0'
- Item3 previous version: '1.5.0', current version: '1.6.1'

The parent that owns these items has its own current SemVer2 version '3.4.5'

The parent version will be updated to '3.5.0' as the differential across all three items is a minor release (both Item2 and Item3).

## Tests
Run the module directly:
```
>>> python update_parent_semver.py
```

If all tests pass, there will be no output.

## Help
```
>>> python -c 'import update_parent_semver as ups; help(ups)'
```
