import inspect


def promote_base_exception(exception: BaseException) -> Exception:
    """
    Promote a BaseException subclass to an Exception subclass.
    """
    if isinstance(exception, Exception):
        return exception
    elif isinstance(exception, BaseException):
        promoted_exception = Exception(repr(exception))
        # copy over all attributes (apart from class!)
        for attr_name, attr in inspect.getmembers(exception):
            if attr_name == "__class__":
                continue
            setattr(promoted_exception, attr_name, attr)
        return promoted_exception
    else:
        raise Exception(f"Got a {type(exception)} instance.")
