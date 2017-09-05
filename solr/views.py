from django.shortcuts import render

# Create your views here.

import datetime
import copy
from django.http import HttpResponse
from cw import settings
from solr.forms import SearchForm, basicForm
from solr.solr_utils import solr_search, solr_md5_search

def index(request):
    return render(request, 'solr/index.html', {'adv_form':SearchForm(), 'error_flag':False})
    return render(request, 'solr/index.html', {'basic_form':basicForm(), 'adv_form':SearchForm()})

def about(request):
    return HttpResponse('about')

def detail(request, md5):
    result = solr_md5_search(md5)
    print '-------------------daad'''
    print result
    form = SearchForm()
    # return render(request, 'solr/detail.html', {'adv_form': form, 'error_flag':False})
    return render(request, 'solr/detail.html', {'adv_form': form, 'error_flag':False, 'result':result})
    return HttpResponse('ok' + md5)

def jumppage(request, page_info):
                # next_url[0] = u'range={}'.format(search_params[0])
                # next_url[1] = u'kw={}'.format(search_params[1])
                # next_url[2] = u'fq1={}'.format(search_params[2][0])
                # next_url[3] = u'fq2={}'.format(search_params[2][1])
    get_params = page_info.split('&')
    search_params = range(0, 3)
    fq = range(0, 2)
    start = ''
    for i in get_params:
        if i.find('range') == 0:
            search_params[0] = i[i.index('=')+1:]
        if i.find('kw') == 0:
            search_params[1] = i[i.index('=')+1:]
        if i.find('fq1') == 0:
            fq[0] = i[i.index('=')+1:]
        if i.find('fq2') == 0:
            fq[1] = i[i.index('=')+1:]
        if i.find('start') == 0:
            start = i[i.index('=')+1:]
    search_params[2] = fq
    print '------------------sgf3-----------------'
    # print search_params
    results, start_next = solr_search(search_params, start)
    print start, start_next
    next_url = range(1, 6)
    next_url[0] = u'range={}'.format(search_params[0])
    next_url[1] = u'kw={}'.format(search_params[1])
    next_url[2] = u'fq1={}'.format(search_params[2][0])
    next_url[3] = u'fq2={}'.format(search_params[2][1])
    next_url[4] = u'start={}'.format(start_next)
    print next_url
    print u'&'.join(next_url)
    form = SearchForm()
    if int(start) > 9:
        last_url = copy.copy(next_url)
        last_url[4] = u'start={}'.format(str(int(start)-10))
        return render(request, 'solr/index.html', {'adv_form': form, 'result':results, 'num':len(results), 'next':u'&'.join(next_url), 'last':u'&'.join(last_url)})

    return render(request, 'solr/index.html', {'adv_form': form, 'result':results, 'num':len(results), 'next':u'&'.join(next_url)})
    return HttpResponse(page_info)

def search(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            form_data = form.cleaned_data
            # print '-----------------------------------'
            # print form_data['search_range']
            # print form_data['key_word']
            # print form_data['datetime_s']
            # print form_data['time_range_s']
            # print form_data['datetime_e']
            # print form_data['time_range_e']
            fq = search_condition_analysis(form_data)
            if not fq:
                return render(request, 'solr/index.html', {'adv_form': form, 'error_flag':True})
            else:
                # print fq
                # print '------------------fq-----------------'
                search_params = fq
                results, start_next = solr_search(search_params, '0')
                if len(results) == 0:
                    return render(request, 'solr/index.html', {'adv_form': form, 'result':results, 'num':len(results)})
                next_url = range(1, 6)
                next_url[0] = u'range={}'.format(search_params[0])
                next_url[1] = u'kw={}'.format(search_params[1])
                next_url[2] = u'fq1={}'.format(search_params[2][0])
                next_url[3] = u'fq2={}'.format(search_params[2][1])
                next_url[4] = u'start={}'.format(start_next)
                # print next_url
                return render(request, 'solr/index.html', {'adv_form': form, 'result':results, 'num':len(results), 'next':u'&'.join(next_url)})
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SearchForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'solr/index.html', {'adv_form': form, 'error_flag':False})
    return HttpResponse('search')


# years: 1900 to 2000
# date:[* TO *]
# date:[* TO 2015-09-02T00:00:00Z]
def search_condition_analysis(form_data):
    s_range = ''
    if form_data['search_range'] == '0':
        s_range = 'all'
    elif form_data['search_range'] == '1':
        s_range = 'title'
    else:
        s_range = 'place'

    s_word = form_data['key_word']

    fq = ['', '']
    s_date_s = form_data['datetime_s']
    fq_date_s = ''
    if s_date_s == None:
        fq_date_s = '*'
    else:
        fq_date_s = str(s_date_s) + 'T00:00:00Z'

    s_date_e = form_data['datetime_e']
    fq_date_e = ''
    if s_date_e == None:
        fq_date_e = '*'
    else:
        fq_date_e = str(s_date_e) + 'T00:00:00Z'

    fq_date = '[%s TO %s]' % (fq_date_s, fq_date_e)
    fq[0] = 'date:'+fq_date


    s_time_s = form_data['time_range_s']
    s_time_e = form_data['time_range_e']
    time_s = '0%s:00:00'[1:] % s_time_s if s_time_s!='-' else '*'
    time_e = '0%s:00:00'[1:] % s_time_e if s_time_e!='-' else '*'
    fq_time = '[%s TO %s]' % (time_s, time_e)
    fq_time = 'time:'+fq_time
    fq[1] = fq_time
    if s_date_s!=None and s_date_e!=None:
        if s_date_s > s_date_e:
            return False

    if s_time_s!='-' and s_time_e!='-':
        if int(s_time_s) > int(s_time_e):
            return False
    return [s_range, s_word, fq]





