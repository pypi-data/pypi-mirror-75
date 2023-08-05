from datetime import datetime


class Base(object):
    date_format = '%Y-%m-%d'
    datetime_format = date_format + 'T%H:%M:%S'
    full_datetime_format = date_format + 'T%H:%M:%S.%f'
    extended_datetime_format = date_format + 'T%H:%M:%S.%fZ'

    @classmethod
    def parse_date_time(cls, text):
        instance = None
        for format in [cls.extended_datetime_format, cls.full_datetime_format, cls.datetime_format, cls.date_format]:
            try:
                instance = datetime.strptime(text, format)
            except Exception:
                pass
            else:
                break
        return instance
