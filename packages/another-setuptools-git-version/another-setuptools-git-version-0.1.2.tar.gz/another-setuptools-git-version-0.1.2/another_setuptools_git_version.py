import subprocess
import collections


def get_tag() -> str:
    return subprocess.getoutput('git describe HEAD --abbrev=0 --tags')


def is_head_at_tag() -> bool:
    """Return True or False depending on whether the given tag is pointing to HEAD"""
    return not subprocess.getoutput('git describe --exact-match HEAD').startswith('fatal: no tag exactly matches')


def get_count_commit() -> int:
    """
    Get count of commits since the last tag. This may not work properly if there are side branches.
    :return:
    """
    return int(subprocess.getoutput('git rev-list $(git describe --abbrev=0)..HEAD --count'))


def get_version(template="{tag}.{cc}", starting_version="0.1.0", **kwargs) -> str:
    tag = get_tag()
    if not tag:
        return starting_version
    elif is_head_at_tag():
        return tag
    else:
        return template.format(tag=tag, cc=get_count_commit())


def validate_version_config(dist, _, config):
    if not isinstance(config, collections.Mapping):
        raise TypeError("Config should be a dictionary with `version_format` and `starting_version` keys.")

    dist.metadata.version = get_version(**config)


# explicitly define the outward facing API of this module
__all__ = [
    get_tag.__name__,
    is_head_at_tag.__name__,
    get_count_commit.__name__,
    get_version.__name__,
    validate_version_config.__name__,
]
