from pathlib import Path


def rm_tree(pth: Path, rm_dir=False):
    """
    Cleans a directory for the given Path
    :param pth: The Path to the target dir
    :param rm_dir: indicate whether target dir itself should be removed
    :rtype: None
    """
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child, rm_dir=True)
    if rm_dir:
        pth.rmdir()
