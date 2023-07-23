import datetime
import json

from django.db import connection

from rest_framework.authentication import TokenAuthentication


auth = TokenAuthentication()

def format_uuid(value):
    return value.replace("-", "")


def is_empty(value):
    if not value:
        return True
    if value and len(value) == 0:
        return True


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def raw_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row_dict = dictfetchall(cursor)

    return row_dict


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def clean_json_dump(item):
    return json.dumps(
      item,
      sort_keys=False,
      indent=1,
      default=default
    )


def authenticated(request):
    try:
        user = auth.authenticate(request)
        print(user)
        if user:
            return True
        else:
            return False
    except :
        return False

