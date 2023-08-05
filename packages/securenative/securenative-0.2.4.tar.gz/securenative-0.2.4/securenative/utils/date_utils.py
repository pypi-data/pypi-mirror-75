from datetime import datetime


class DateUtils(object):

    @staticmethod
    def to_timestamp(date):
        if not date:
            return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f'[:-3] + 'Z')
