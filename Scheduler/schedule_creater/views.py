from django.shortcuts import render
import datetime, os
from django.db import models
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django import forms
from django.views.generic import TemplateView, ListView, DetailView
from shops.models import Shop
from employee.models import Employee
from employee_experience.models import Employee_Experience
from employee_availability.models import Employee_Availability
from datetime import datetime
from datetime import date
import calendar, pandas as pd, json, math
from django.shortcuts import redirect
from django.core.cache import cache

avail_emp = {}
date_ = ''
day = ''
shop_list = []
schedule_ready = False
select_date = True

# Create your views here.
def home_view(request, *args, **kwargs):
    global select_date
    if request.method == "POST":
        data = request.POST
        action = data.get("create-schedule")
        context = {
            'data': data,
            'action': action
        }
        if action == 'create':
            response = redirect('/schedule/')
            # return HttpResponseRedirect('/test/')
            return  response
    else:
        context = {}
    select_date = True
    return render(request, 'base.html', context)

def print_schedule_view(request, *args, **kwargs):
    day = cache.get('day')
    date = cache.get('date')
    schedule = cache.get('schedule')

    context = {'schedule': schedule, 'date': date, 'day': day}

    # print(context)

    return render(request, 'print_schedule.html', context)

def schedule_view(request, *args, **kwargs):
    # Variables
    global avail_emp, date, shop_list, day, schedule_ready, select_date
    selected_date = 0
    context = {}
    context['date_selected'] = False
    context['select_date'] = select_date
    context['date'] = '2000/01/01'
    context['day'] = 'Sunday'
    context['show_availability'] = False
    context['availability'] = avail_emp
    context['schedule_ready'] = schedule_ready
    context['schedule'] = {}

    schedule = {}

    # Get the required tables
    shop_data = pd.DataFrame(Shop.objects.all().values())
    emp_exp_data = pd.DataFrame(Employee_Experience.objects.all().values())
    emp_data = pd.DataFrame(Employee.objects.all().values())
    emp_avail_data = pd.DataFrame(Employee_Availability.objects.all().values())
    supervisors = emp_data.loc[emp_data['is_supervisor'] == 1]['initials']

    shop_data['shop_name'] = shop_data['initials'] + ' ' + shop_data['name']
    availability = {}
    #     print(supervisors)


    # Ask for date (i/p)

    if (request.method == 'POST') and ('submit-date' in request.POST):

        select_date = request.POST.get('party')
        print(select_date)
        selected_date = datetime.strptime(select_date, '%Y-%m-%d').date()
        selected_day = calendar.day_name[selected_date.weekday()]
        date = selected_date
        day = selected_day
        select_date = False

    if selected_date != 0:
        available_emp = list(emp_avail_data.loc[emp_avail_data['available_' + str(selected_date)[-2:]] == 1]['initials'])
        supervisors_avail = [x for x in supervisors if x in available_emp]
        for iter ,i in enumerate(emp_avail_data['available_' + str(selected_date)[-2:]]):
            emp = emp_avail_data.iloc[iter]['initials']
            availability[emp] = emp_avail_data.iloc[iter]['available_' + str(selected_date)[-2:]]

        context['date_selected'] = True
        context['shops'] = list(shop_data['shop_name'])
        avail_emp = availability
        print(context)

    # print('\n', shop_data['shop_name'])

    # get shop inputs
    selected_shops = []
    if (request.method == 'POST') and ('submit-shops' in request.POST):
        for i in request.POST:
            if 'sample' in i:
                selected_shops.append(request.POST.get(i))
        context['show_availability'] = True
        shop_list = selected_shops
        # context['availability'] = availability

    if (request.method == 'POST') and ('submit-availability' in request.POST):
        print(context['availability'])
        availability = {}
        for i in request.POST:
            if 'key_' in i:
                availability[i[4:]] = request.POST.get(i)
        avail_emp = availability
        schedule_ready = True
        context['schedule_ready'] = schedule_ready
        print(availability)

        if schedule_ready:
            schedule = getschedule(shop_data, emp_exp_data, emp_data, emp_avail_data, supervisors, avail_emp, date, shop_list, day)
            context['schedule'] = schedule
            context['date'] = date
            context['day'] = day

            cache.set('schedule', schedule, 60)
            cache.set('day', day, 60)
            cache.set('date', date, 60)

            response = redirect('/print_schedule/')
            return response

    context['selected_shops'] = selected_shops


    # print(selected_shops)

    return render(request, 'day_schedule.html', context)


def getschedule(shop_data, emp_exp_data, emp_data, emp_avail_data, supervisors, avail_emp, date, shop_list, day):
    supervisors_leading = []

    available_emp = list(avail_emp.keys())
    supervisors_avail = [x for x in supervisors if x in available_emp]

    selected_shops = shop_list
    print(selected_shops)

    shop_dict = {}
    for shop in selected_shops:
        shop_dict[shop] = {}
        shop_dict[shop]['shop_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]]['shop_size'].item()
        shop_dict[shop]['deli_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]]['deli_size'].item()
        shop_dict[shop]['stockroom_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'stockroom_size'].item()
        shop_dict[shop]['has_off_licence'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'has_off_licence'].item()
        shop_dict[shop]['off_licence_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'off_licence_size'].item()
        shop_dict[shop]['behind_till_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'behind_till_size'].item()
        shop_dict[shop]['toiletries_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'toiletries_size'].item()
        shop_dict[shop]['crew'] = []

    print()

    # Lead_Supervisor assignment
    sorted_shop_size = sorted(shop_dict, key=lambda x: (shop_dict[x]['shop_size']))
    for shop in sorted_shop_size:
        shop_dict[shop]['lead_supervisor'] = supervisors_avail.pop(0)
        shop_dict[shop]['crew'].append(shop_dict[shop]['lead_supervisor'])
        supervisors_leading.append(shop_dict[shop]['lead_supervisor'])

    #     print(supervisors_leading)

    # Deli size
    # If Big then deli_count => 30
    # If Mid then deli_count => 10
    # Else < 10
    sorted_deli = sorted(shop_dict, key=lambda x: (shop_dict[x]['deli_size']))

    big_deli_crew = [x for x in list(
        emp_exp_data[~emp_exp_data.loc[emp_exp_data['deli_count'] > 29].isin(supervisors_leading)]['initials']) if
                     pd.isnull(x) == False]
    mid_deli_crew = [x for x in list(
        emp_exp_data[~emp_exp_data.loc[emp_exp_data['deli_count'] > 9].isin(supervisors_leading)]['initials']) if
                     pd.isnull(x) == False]
    all_deli_crew = [x for x in list(
        emp_exp_data[~emp_exp_data.loc[emp_exp_data['deli_count'] > 0].isin(supervisors_leading)]['initials']) if
                     pd.isnull(x) == False]
    #     newlist = [x for x in mylist if math.isnan(x) == False]

    big_deli_crew_avail = [x for x in big_deli_crew if x in available_emp]
    mid_deli_crew_avail = [x for x in mid_deli_crew if x in available_emp]
    all_deli_crew_avail = [x for x in all_deli_crew if x in available_emp]

    for shop in sorted_deli:
        print(all_deli_crew_avail)
        if shop_dict[shop]['deli_size'] == 'Big':
            shop_dict[shop]['deli_taker'] = big_deli_crew_avail[0]
            shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
            big_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            all_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
        elif shop_dict[shop]['deli_size'] == 'Mid':
            if len(big_deli_crew_avail) != 0:
                shop_dict[shop]['deli_taker'] = big_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
                big_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            else:
                shop_dict[shop]['deli_taker'] = mid_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])

            mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            all_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
        elif shop_dict[shop]['deli_size'] == 'Small':
            if len(big_deli_crew_avail) != 0:
                shop_dict[shop]['deli_taker'] = big_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
                big_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
                mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            elif len(big_deli_crew_avail) == 0 and len(mid_deli_crew_avail) != 0:
                shop_dict[shop]['deli_taker'] = mid_deli_crew_avail[0]
                mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
            else:
                shop_dict[shop]['deli_taker'] = all_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])

            all_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
    #     print(json.dumps(shop_dict, indent=3))

    # Stockroom size
    # Big then allocate => 5
    # Mid then allocate 3-4
    # Else allocate 1-2

    sorted_stockroom = sorted(shop_dict, key=lambda x: (shop_dict[x]['stockroom_size']))
    stockroom_crew = list(
        emp_exp_data.loc[emp_exp_data['do_stockroom'] == True].sort_values(by='stockroom_count', ascending=False)[
            'initials'])

    stockroom_crew_avail = [x for x in stockroom_crew if x in available_emp]

    # this is available stockroom crew.
    stockroom_crew = pd.DataFrame(stockroom_crew_avail, columns=['SR_crew'])

    # for one shop discard crew from rest other shops.

    already_occupied_crew = []  # Update already occupied crew.

    for shop_i in shop_dict:
        already_occupied_crew = already_occupied_crew + shop_dict[shop_i]['crew']

    for shop in sorted_stockroom:

        #         print(remaining_stockroom_crew)
        remaining_stockroom_crew = [x for x in list(
            set(list(stockroom_crew[~stockroom_crew.isin(already_occupied_crew)]['SR_crew']))) if pd.isnull(x) == False]

        #         print('Crew: ', shop_dict[shop]['crew'])

        #         print('Remaining Crew: ', remaining_stockroom_crew)

        if shop_dict[shop]['stockroom_size'] == 'Big':
            shop_dict[shop]['stockroom_crew'] = remaining_stockroom_crew[0:5]
        elif shop_dict[shop]['stockroom_size'] == 'Mid':
            shop_dict[shop]['stockroom_crew'] = remaining_stockroom_crew[0:3]
        elif shop_dict[shop]['stockroom_size'] == 'Small':
            shop_dict[shop]['stockroom_crew'] = remaining_stockroom_crew[0:2]
        shop_dict[shop]['crew'] = shop_dict[shop]['crew'] + shop_dict[shop]['stockroom_crew']
        already_occupied_crew = already_occupied_crew + shop_dict[shop]['stockroom_crew']

    # Off_licence (if Off_licence is Yes)
    # Big then 1-2
    # Else 1-2
    sorted_off_l = sorted(shop_dict, key=lambda x: (shop_dict[x]['off_licence_size']))
    off_l_crew = list(
        emp_exp_data.loc[emp_exp_data['do_off_licence'] == True].sort_values(by='off_licence_count', ascending=False)[
            'initials'])
    # print(emp_exp_data[['initials', 'do_off_licence']])

    off_l_crew_avail = [x for x in off_l_crew if x in available_emp]

    # off license crew availabe
    off_l_crew = pd.DataFrame(off_l_crew_avail, columns=['OL_crew'])

    for shop in sorted_off_l:
        occupied_crew = []
        for shop_i in shop_dict:
            if shop != shop_i:
                occupied_crew = occupied_crew + shop_dict[shop_i]['crew']

        remaining_off_l_crew = [x for x in list(set(list(off_l_crew[~off_l_crew.isin(occupied_crew)]['OL_crew']))) if
                                pd.isnull(x) == False]

        for i in shop_dict[shop]['stockroom_crew']:  # Removing all stockroom crew as they won't do off licence after SR
            if i in remaining_off_l_crew:
                remaining_off_l_crew.remove(i)

        remaining_off_l_crew.remove(shop_dict[shop]['lead_supervisor'])  # LS won't do off_l

        if shop_dict[shop]['off_licence_size'] == 'Big':
            shop_dict[shop]['off_l_crew'] = remaining_off_l_crew[0:2]
        else:
            shop_dict[shop]['off_l_crew'] = [remaining_off_l_crew[0]]
        shop_dict[shop]['crew'] = list(set(shop_dict[shop]['crew'] + shop_dict[shop]['off_l_crew']))

    # Behind the till
    # Big then behind_till_count => 50
    # Else < 50
    for shop in shop_dict:
        shop_dict[shop]['behind_till_crew'] = shop_dict[shop]['lead_supervisor']

    # Toiletries
    # Big then toiletries_count => 60
    # Mid then toiletries_count => 25
    # Else < 25

    already_occupied_crew = []  # Update already occupied crew.

    for shop_i in shop_dict:
        already_occupied_crew = already_occupied_crew + shop_dict[shop_i]['crew']

    # Shop_floor rest crew
    # If shop_size is Big Then crew_size => 9-10
    # If Mid Then crew_size 7-9
    # Else < 7

    print('\nDetailed Plan for the day:')
    for shop in shop_dict:
        crew_size = len(shop_dict[shop]['crew'])

        remaining_crew = [x for x in list(
            set(list(emp_exp_data[~emp_exp_data['initials'].isin(already_occupied_crew)]['initials']))) if
                          pd.isnull(x) == False]
        remaining_crew_avail = [x for x in remaining_crew if
                                x in available_emp]  # optimize by removing the kinda repetitive above statement

        if shop_dict[shop]['shop_size'] == 'Big':
            required_no = 10 - crew_size
        elif shop_dict[shop]['shop_size'] == 'Mid':
            required_no = 8 - crew_size
        else:
            required_no = 6 - crew_size
        shop_dict[shop]['crew'] = shop_dict[shop]['crew'] + remaining_crew_avail[0:required_no]
        already_occupied_crew = already_occupied_crew + shop_dict[shop]['crew']

        crew = [member for member in shop_dict[shop]['crew'] if
                member not in [shop_dict[shop]['lead_supervisor']]]
        shop_dict[shop]['crew'] = crew # Removing leadsupervisor from crew

        print('\nFor shop: ', shop, ' | Lead Supervisor: ', shop_dict[shop]['lead_supervisor'])
        print('Deli_Crew: ', shop_dict[shop]['deli_taker'])
        print('Stockroom_Crew: ', shop_dict[shop]['stockroom_crew'])
        print('Off_licence_Crew: ', shop_dict[shop]['off_l_crew'])
        print('Behind_till_Crew: ', shop_dict[shop]['behind_till_crew'])
        print('Entire_Crew: ', shop_dict[shop]['crew'])
        print()

    return shop_dict




def print_time_table(date, day, schedule_info):
    print('\n\n---------------------------------------------------------------\n\n')
    print('*', day, '::', date.day, calendar.month_name[date.month], '*\n')

    for shop in schedule_info:
        print('_' + shop + '_')
        print('Lead: ', schedule_info[shop]['lead_supervisor'])
        crew = [member for member in schedule_info[shop]['crew'] if
                member not in [schedule_info[shop]['lead_supervisor']]]
        print('Crew: ', crew)

        print('\n\n')

    print('---------------------------------------------------------------\n\n')


def print_day_schedule():
    # Get the required tables
    shop_data = pd.DataFrame(Shop.objects.all().values())
    emp_exp_data = pd.DataFrame(Employee_Experience.objects.all().values())
    emp_data = pd.DataFrame(Employee.objects.all().values())
    emp_avail_data = pd.DataFrame(Employee_Availability.objects.all().values())
    supervisors = emp_data.loc[emp_data['is_supervisor'] == 'Yes']['initials']

    #     print(supervisors)

    supervisors_leading = []

    # Ask for date (i/p)
    selected_date = datetime.strptime(input("\nEnter the date of the schedule you want to create: "), '%d/%m/%Y').date()
    selected_day = calendar.day_name[selected_date.weekday()]

    print(str(selected_date))
    print(str(selected_date)[:2])

    available_emp = list(emp_avail_data.loc[emp_avail_data['available ' + str(selected_date)[-2:]] == 1]['initials'])
    supervisors_avail = [x for x in supervisors if x in available_emp]

    #     print(available_emp)

    #     print(supervisors_avail)

    #     print(selected_day)

    # Select stores from list (i/p)

    print('\n', shop_data.iloc[:, 2:4])

    selected_shops = input(
        "\nSelect the shops that need to be stocktaked on the selected date.\n\nYour input must be separated by',': '").split(
        ',')

    # Shop's required data

    shop_dict = {}
    for shop in selected_shops:
        shop_dict[shop] = {}
        shop_dict[shop]['shop_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]]['shop_size'].item()
        shop_dict[shop]['deli_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]]['deli_size'].item()
        shop_dict[shop]['stockroom_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'stockroom_size'].item()
        shop_dict[shop]['has_off_licence'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'has_off_licence'].item()
        shop_dict[shop]['off_licence_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'off_licence_size'].item()
        shop_dict[shop]['behind_till_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'behind_till_size'].item()
        shop_dict[shop]['toiletries_size'] = shop_data.loc[shop_data['name'] == shop.split(' ')[1]][
            'toiletries_size'].item()
        shop_dict[shop]['crew'] = []

    print()

    # Lead_Supervisor assignment
    sorted_shop_size = sorted(shop_dict, key=lambda x: (shop_dict[x]['shop_size']))
    for shop in sorted_shop_size:
        shop_dict[shop]['lead_supervisor'] = supervisors_avail.pop(0)
        shop_dict[shop]['crew'].append(shop_dict[shop]['lead_supervisor'])
        supervisors_leading.append(shop_dict[shop]['lead_supervisor'])

    #     print(supervisors_leading)

    # Deli size
    # If Big then deli_count => 30
    # If Mid then deli_count => 10
    # Else < 10
    sorted_deli = sorted(shop_dict, key=lambda x: (shop_dict[x]['deli_size']))

    big_deli_crew = [x for x in list(
        emp_exp_data[~emp_exp_data.loc[emp_exp_data['deli_count'] > 29].isin(supervisors_leading)]['initials']) if
                     pd.isnull(x) == False]
    mid_deli_crew = [x for x in list(
        emp_exp_data[~emp_exp_data.loc[emp_exp_data['deli_count'] > 9].isin(supervisors_leading)]['initials']) if
                     pd.isnull(x) == False]
    all_deli_crew = [x for x in list(
        emp_exp_data[~emp_exp_data.loc[emp_exp_data['deli_count'] > 0].isin(supervisors_leading)]['initials']) if
                     pd.isnull(x) == False]
    #     newlist = [x for x in mylist if math.isnan(x) == False]

    big_deli_crew_avail = [x for x in big_deli_crew if x in available_emp]
    mid_deli_crew_avail = [x for x in mid_deli_crew if x in available_emp]
    all_deli_crew_avail = [x for x in all_deli_crew if x in available_emp]

    for shop in sorted_deli:
        print(all_deli_crew_avail)
        if shop_dict[shop]['deli_size'] == 'Big':
            shop_dict[shop]['deli_taker'] = big_deli_crew_avail[0]
            shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
            big_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            all_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
        elif shop_dict[shop]['deli_size'] == 'Mid':
            if len(big_deli_crew_avail) != 0:
                shop_dict[shop]['deli_taker'] = big_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
                big_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            else:
                shop_dict[shop]['deli_taker'] = mid_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])

            mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            all_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
        elif shop_dict[shop]['deli_size'] == 'Small':
            if len(big_deli_crew_avail) != 0:
                shop_dict[shop]['deli_taker'] = big_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
                big_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
                mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
            elif len(big_deli_crew_avail) == 0 and len(mid_deli_crew_avail) != 0:
                shop_dict[shop]['deli_taker'] = mid_deli_crew_avail[0]
                mid_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])
            else:
                shop_dict[shop]['deli_taker'] = all_deli_crew_avail[0]
                shop_dict[shop]['crew'].append(shop_dict[shop]['deli_taker'])

            all_deli_crew_avail.remove(shop_dict[shop]['deli_taker'])
    #     print(json.dumps(shop_dict, indent=3))

    # Stockroom size
    # Big then allocate => 5
    # Mid then allocate 3-4
    # Else allocate 1-2

    sorted_stockroom = sorted(shop_dict, key=lambda x: (shop_dict[x]['stockroom_size']))
    stockroom_crew = list(
        emp_exp_data.loc[emp_exp_data['do_stockroom'] == 'Yes'].sort_values(by='stockroom_count', ascending=False)[
            'initials'])

    stockroom_crew_avail = [x for x in stockroom_crew if x in available_emp]

    # this is available stockroom crew.
    stockroom_crew = pd.DataFrame(stockroom_crew_avail, columns=['SR_crew'])

    # for one shop discard crew from rest other shops.

    already_occupied_crew = []  # Update already occupied crew.

    for shop_i in shop_dict:
        already_occupied_crew = already_occupied_crew + shop_dict[shop_i]['crew']

    for shop in sorted_stockroom:

        #         print(remaining_stockroom_crew)
        remaining_stockroom_crew = [x for x in list(
            set(list(stockroom_crew[~stockroom_crew.isin(already_occupied_crew)]['SR_crew']))) if pd.isnull(x) == False]

        #         print('Crew: ', shop_dict[shop]['crew'])

        #         print('Remaining Crew: ', remaining_stockroom_crew)

        if shop_dict[shop]['stockroom_size'] == 'Big':
            shop_dict[shop]['stockroom_crew'] = remaining_stockroom_crew[0:5]
        elif shop_dict[shop]['stockroom_size'] == 'Mid':
            shop_dict[shop]['stockroom_crew'] = remaining_stockroom_crew[0:3]
        elif shop_dict[shop]['stockroom_size'] == 'Small':
            shop_dict[shop]['stockroom_crew'] = remaining_stockroom_crew[0:2]
        shop_dict[shop]['crew'] = shop_dict[shop]['crew'] + shop_dict[shop]['stockroom_crew']
        already_occupied_crew = already_occupied_crew + shop_dict[shop]['stockroom_crew']

    # Off_licence (if Off_licence is Yes)
    # Big then 1-2
    # Else 1-2
    sorted_off_l = sorted(shop_dict, key=lambda x: (shop_dict[x]['off_licence_size']))
    off_l_crew = list(
        emp_exp_data.loc[emp_exp_data['do_off_licence'] == 'Yes'].sort_values(by='off_licence_count', ascending=False)[
            'initials'])

    off_l_crew_avail = [x for x in off_l_crew if x in available_emp]

    # off license crew availabe
    off_l_crew = pd.DataFrame(off_l_crew_avail, columns=['OL_crew'])

    for shop in sorted_off_l:
        occupied_crew = []
        for shop_i in shop_dict:
            if shop != shop_i:
                occupied_crew = occupied_crew + shop_dict[shop_i]['crew']

        remaining_off_l_crew = [x for x in list(set(list(off_l_crew[~off_l_crew.isin(occupied_crew)]['OL_crew']))) if
                                pd.isnull(x) == False]

        for i in shop_dict[shop]['stockroom_crew']:  # Removing all stockroom crew as they won't do off licence after SR
            if i in remaining_off_l_crew:
                remaining_off_l_crew.remove(i)

        remaining_off_l_crew.remove(shop_dict[shop]['lead_supervisor'])  # LS won't do off_l

        if shop_dict[shop]['off_licence_size'] == 'Big':
            shop_dict[shop]['off_l_crew'] = remaining_off_l_crew[0:2]
        else:
            shop_dict[shop]['off_l_crew'] = [remaining_off_l_crew[0]]
        shop_dict[shop]['crew'] = list(set(shop_dict[shop]['crew'] + shop_dict[shop]['off_l_crew']))

    # Behind the till
    # Big then behind_till_count => 50
    # Else < 50
    for shop in shop_dict:
        shop_dict[shop]['behind_till_crew'] = shop_dict[shop]['lead_supervisor']

    # Toiletries
    # Big then toiletries_count => 60
    # Mid then toiletries_count => 25
    # Else < 25

    already_occupied_crew = []  # Update already occupied crew.

    for shop_i in shop_dict:
        already_occupied_crew = already_occupied_crew + shop_dict[shop_i]['crew']

    # Shop_floor rest crew
    # If shop_size is Big Then crew_size => 9-10
    # If Mid Then crew_size 7-9
    # Else < 7

    print('\nDetailed Plan for the day:')
    for shop in shop_dict:
        crew_size = len(shop_dict[shop]['crew'])

        remaining_crew = [x for x in list(
            set(list(emp_exp_data[~emp_exp_data['initials'].isin(already_occupied_crew)]['initials']))) if
                          pd.isnull(x) == False]
        remaining_crew_avail = [x for x in remaining_crew if
                                x in available_emp]  # optimize by removing the kinda repetitive above statement

        if shop_dict[shop]['shop_size'] == 'Big':
            required_no = 10 - crew_size
        elif shop_dict[shop]['shop_size'] == 'Mid':
            required_no = 8 - crew_size
        else:
            required_no = 6 - crew_size
        shop_dict[shop]['crew'] = shop_dict[shop]['crew'] + remaining_crew_avail[0:required_no]
        already_occupied_crew = already_occupied_crew + shop_dict[shop]['crew']

        print('\nFor shop: ', shop, ' | Lead Supervisor: ', shop_dict[shop]['lead_supervisor'])
        print('Deli_Crew: ', shop_dict[shop]['deli_taker'])
        print('Stockroom_Crew: ', shop_dict[shop]['stockroom_crew'])
        print('Off_licence_Crew: ', shop_dict[shop]['off_l_crew'])
        print('Behind_till_Crew: ', shop_dict[shop]['behind_till_crew'])
        print('Entire_Crew: ', shop_dict[shop]['crew'])
        print()

    print_time_table(selected_date, selected_day, shop_dict)


