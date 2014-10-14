from parser import parse_toml


def parse(value):
    parsed = parse_toml(value)
    prepared = []

    prepared = prepare_values(parsed)

    data = {}

    for entry in prepared:
        add_value(data, entry[0], entry[1])

    return data


def prepare_values(values):
    group = None

    for entry in values:
        key, value = entry

        if key == "keygroup":
            group = value
            yield [value, {}]

        else:
            if group:
                k = "%s.%s" % (group, key)
            else:
                k = key

            yield [k, value]


def add_value(data, key, value):
    keys = key.split(".")

    t = data
    for key in keys[:-1]:
        t = t.setdefault(key, {})

    t[keys[-1]] = value
