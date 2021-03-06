﻿

from django.forms.widgets import Widget, Select
from django.utils import datetime_safe
from django.utils.dates import MONTHS
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.utils.formats import get_format
from django.utils import six
from django.conf import settings
import re
import datetime

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)-(\d\d?)$')



def _parse_date_fmt():
    fmt = get_format('DATE_FORMAT')
    escaped = False
    output = []
    for char in fmt:
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif char in 'Yy':
            output.append('year')
            #if not self.first_select: self.first_select = 'year'
        elif char in 'bEFMmNn':
            output.append('month')
            #if not self.first_select: self.first_select = 'month'
        elif char in 'dj':
            output.append('day')
            #if not self.first_select: self.first_select = 'day'
    return output



class solr_SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = (0, '---')
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'
    hour_field = '%s_hour'
    is_required = False

    def __init__(self, attrs=None, years=None, months=None):
        self.attrs = attrs or {}

        # Optional list or tuple of years to use in the "year" select box.
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

        # Optional dict of months to use in the "month" select box.
        if months:
            self.months = months
        else:
            self.months = MONTHS

        self.hours = range(0, 24)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, six.string_types):
                if settings.USE_L10N:
                    try:
                        input_format = get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime.strptime(force_str(value), input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = [int(v) for v in match.groups()]
        choices = [(i, i) for i in self.years]
        year_html = self.create_select(name, self.year_field, value, year_val, choices) + u'年'
        choices = list(six.iteritems(self.months))
        month_html = self.create_select(name, self.month_field, value, month_val, choices) + u'月'
        choices = [(i, i) for i in range(1, 32)]
        day_html = self.create_select(name, self.day_field, value, day_val, choices) + u'日'

        output = []
        for field in _parse_date_fmt():
            if field == 'year':
                # output.append(year_html)
                output = [year_html] + output
            elif field == 'month':
                output.append(month_html)
            elif field == 'day':
                output.append(day_html)
        # return mark_safe('aa'.join(output))
        # output.append(hour_html)
        return mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        first_select = None
        field_list = _parse_date_fmt()
        if field_list:
            first_select = field_list[0]
        if first_select is not None:
            return '%s_%s' % (id_, first_select)
        else:
            return '%s_month' % id_

    def value_from_datadict(self, data, files, name):
        print data
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        # print y, m, d
        if y == m == d == "0":
            # print '-----------------1--------'
            return None
        if y and m and d:
            # print '-------------------------'
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(int(y), int(m), int(d))
                except ValueError:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

    def create_select(self, name, field, value, val, choices):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        if not self.is_required:
            choices.insert(0, self.none_value)
        # choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=field % id_)
        s = Select(choices=choices)
        select_html = s.render(field % name, val, local_attrs)
        return select_html








