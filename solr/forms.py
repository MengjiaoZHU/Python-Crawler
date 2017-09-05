
from django import forms
from django.contrib.auth.models import User
# from django.forms.extras.widgets import SelectDateWidget
from solr.widgets import solr_SelectDateWidget

class basicForm(forms.Form):
    key_word = forms.CharField(max_length=128, help_text="关键字：")

class SearchForm(forms.Form):
    error_message = {'required':u'请输入搜索关键字'}
    choices = [(0, u'全部'), (1, u'标题'), (2, u'地点')]
    search_range = forms.CharField(widget=forms.Select(choices = choices), help_text="搜索范围：")
    key_word = forms.CharField(max_length=128, help_text="关键字：", error_messages = error_message)
    
    # 以下为非必填选项
    error_message = {'invalid':u'请输入完整起始的日期'}
    YEARS = range(2015, 2018)
    MONTHS = {
              1:('1'), 2:('2'), 3:('3'), 4:('4'),
              5:('5'), 6:('6'), 7:('7'), 8:('8'),
              9:('9'), 10:('10'), 11:('11'), 12:('12'),
             }
    HOURS = [str(i)+':00' for i in range(0, 24)]
    datetime_s = forms.DateField(widget=solr_SelectDateWidget(years=YEARS, months=MONTHS, attrs={'align':'left'}), help_text="开始日期：", required=False, error_messages = error_message)
    choices = [(i, str(i)+':00') for i in range(0, 24)]
    choices.insert(0, '--')
    time_range_s = forms.CharField(widget=forms.Select(choices = choices, attrs={'align':'left'}), help_text="开始时间：", required=False)
  
    error_message = {'invalid':u'请输入完整截止的日期'}
    datetime_e = forms.DateField(widget=solr_SelectDateWidget(years=YEARS, months=MONTHS, attrs={'align':'left'}), help_text="结束日期：", required=False, error_messages = error_message)
    time_range_e = forms.CharField(widget=forms.Select(choices = choices, attrs={'align':'left'}), help_text="结束时间：", required=False)
    
    # time_range_s = forms.TimeField(widget=forms.SplitDateTimeWidget(), help_text="请输入查询时间范围：")
    # datetime = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), help_text="请输入查询日期：", input_formats = '%Y-%m-%d')
    # time_range_s = forms.TimeField(widget=forms.TimeInput(), help_text="请输入查询时间范围：", input_formats = '%H:%M')
    # time_range_e = forms.TimeField(widget=forms.TimeInput(), input_formats = '%H:%M')