import exifread
from collections import defaultdict

def getValue(tagObj):
    if not tagObj:
        return tagObj
    return tagObj.printable

def process_file(filename, stop_tag='UNDEF', details=True, strict=False, debug=False, truncate_tags=True, auto_seek=True, raw=False):
    """
    Wrapper for origin exifread.process_file.
    Process an image file (expects a image filename).
    This is the function that has to deal with all the arbitrary nasty bits
    of the EXIF standard.
    """

    with open(filename, "rb") as f:
        tags = exifread.process_file(f, stop_tag, details, strict, debug)

        # return the raw tags dict when raw is set to True
        if raw:
            return raw

        #  return empty default dict when it is empty
        if not tags:
            return defaultdict(str)
        
        # easy and safe to read
        ezTags = defaultdict(str)

        # get all tag printable values and divide categories to dicts
        for key, tagObj in tags.items():
            if type(tagObj) != exifread.IfdTag:
                continue

            ezTags[key] = getValue(tagObj)
        
        return ezTags