from pathlib import Path


def extract_required_fnames_part(
    fpaths: list[str],
    delimiter: str,
    part_name_idx: int,
) -> dict[str, Path]:
    """
    For each path in `fpaths`:
     - take the basename of the file name (without extension);
     - split the basename by `delimiter`;
     - take the part specified by `part_name_idx`.
    """
    result = {}
    for fpath_str in fpaths:
        fpath = Path(fpath_str)
        basename = fpath.stem
        basename_parts = basename.split(delimiter)
        track_number = basename_parts[part_name_idx]
        result[track_number] = fpath
    
    return result

