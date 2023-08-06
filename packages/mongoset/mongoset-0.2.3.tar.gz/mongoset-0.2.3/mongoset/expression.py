from mongoset.database import Expression


def gt(val):
    return Expression("$gt", val)


def gte(val):
    return Expression("$gte", val)


def lt(val):
    return Expression("$lt", val)


def lte(val):
    return Expression("$lte", val)


def ne(val):
    return Expression("$ne", val)


def in_list(*elements):
    return Expression("$in", elements)


def not_in_list(*elements):
    return Expression("$nin", elements)
