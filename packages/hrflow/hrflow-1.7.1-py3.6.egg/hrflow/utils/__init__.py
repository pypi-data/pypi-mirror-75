

STAGE_VALUES = [None, "new", "yes", "later", "no"]
SORT_BY_VALUES = ["created_at", "updated_at", "location", "location_experience", "location_education", "searching",
                  "scoring"]
ORDER_BY_VALUES = [None, "desc", "asc"]
VALID_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.doc', '.docx', '.rtf', '.dotx', '.odt', '.odp', '.ppt',
                    '.pptx', '.rtf', '.msg']
INVALID_FILENAME = ['.', '..']


def get_item(item, provider_key, key, reference=None, email=None):

    provider = "source_key" if item == "profile" else "board_key"

    query_params = {provider: validate_key(provider_key)}
    if key:
        query_params["key"] = validate_key(key)
    if reference:
        query_params["reference"] = validate_reference(reference)
    if email:
        query_params["profile_email"] = email

    return query_params


def validate_key(obj, value):
    if not isinstance(value, str) and value is not None:
        raise TypeError(obj + " key must be string")

    return value


def validate_order_by(value):
    if value not in ORDER_BY_VALUES:
        raise ValueError("order_by value must be in {}".format(str(ORDER_BY_VALUES)))

    return value


def validate_sort_by(value):
    if value not in SORT_BY_VALUES:
        raise ValueError("sort_by value must be in {}".format(str(SORT_BY_VALUES)))

    return value


def validate_reference(value):
    if value is None:
        return value
    if not isinstance(value, str) and value is not None:
        raise TypeError("reference must be string not {}".format(value))

    return value


def validate_page(value):
    if not isinstance(value, int):
        raise TypeError("page must be 'int'")

    return value


def validate_limit(value):
    if not isinstance(value, int):
        raise TypeError("limit must be 'int'")

    return value


def validate_stage(value):
    if value is None:
        return value
    if value not in STAGE_VALUES:
        raise ValueError("stage value must be in {} not {}".format(str(STAGE_VALUES), value))

    return value


def validate_provider_keys(value):
    if not value or not all(isinstance(elt, str) for elt in value):
        raise TypeError("provider_ids must contain list of strings")
    return value