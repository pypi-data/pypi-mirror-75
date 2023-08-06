from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import models as matialvarezs_time_sleep_models
from . import errors as matialvarezs_time_sleep_errors
from . import settings, time_sleep_v2
import os, time, random
from matialvarezs_request_handler import utils as matialvarezs_request_handler_utils

random_string = "807HB9Z5JUOtagFolqf71Ff9sLFq54Ch"

"""
def parse_model_attributes(**kwargs):
	attributes = {}
	
	return attributes

def create_model(**kwargs):

	for key, value in parse_model_attributes(**kwargs).items():
		kwargs[key] = value
	return h_utils.db_create(matialvarezs_time_sleep_models.Model, **kwargs)

def get_model(**kwargs):
	return h_utils.db_get(matialvarezs_time_sleep_models.Model, **kwargs)

def get_or_none_model(**kwargs):
	return h_utils.db_get_or_none(matialvarezs_time_sleep_models.Model, **kwargs)

def filter_model(**kwargs):
	return h_utils.db_filter(matialvarezs_time_sleep_models.Model, **kwargs)

def q_model(q, **otions):
	return h_utils.db_q(matialvarezs_time_sleep_models.Model, q)

def delete_model(entry, **options):
	return h_utils.db_delete(entry)

def update_model(entry, **kwargs):
	attributes = {}
	for key, value in parse_model_attributes(**kwargs).items():
		attributes[key] = value
	return h_utils.db_update(entry, **attributes)
"""


def get_delay_schedule(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule = list()
    if total_time_sleep == 0:
        delay_schedule.append(0)

    # print("total time sleep", total_time_sleep)
    if total_time_sleep > 0:
        if options.get('time_in_minutes', False) is True:
            total_time_sleep = total_time_sleep * 60

        while True:
            random_time = random.randint(lower_boundary, upper_boundary)
            # print("antes de append sum(delay_schedule) + random_time",sum(delay_schedule) + random_time)
            if sum(delay_schedule) + random_time > total_time_sleep:
                continue
            else:
                # print("agrego numero")
                delay_schedule.append(random_time)
            # if sum(delay_schedule) + random_time > total_time_sleep:
            #     continue
            # print("despues de append sum(delay_schedule) + random_time", sum(delay_schedule) + random_time)
            if sum(delay_schedule) == total_time_sleep:
                break

    if options.get("debug", False):
        print("total time sleep", total_time_sleep)
        print(delay_schedule)
    return delay_schedule, total_time_sleep


def time_sleep(total_time_sleep, **options):
    delay_schedule, total_time_sleep = get_delay_schedule(total_time_sleep, **options)  # list()
    # if options.get('time_in_minutes',False) is True:
    #     total_time_sleep = total_time_sleep*60
    # while sum(delay_schedule) < total_time_sleep:
    #     delay_schedule.append(random.randint(1, 10))

    print(delay_schedule)
    for delay in delay_schedule:
        time.sleep(delay)


def should_stop(**kwargs):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = kwargs.get('url', settings.URL_SHOULD_STOP_TIME_SLEEP)
    method = kwargs.get('method', "GET")
    data = kwargs.get('data', {})
    results = {}
    if method == "GET":
        results = matialvarezs_request_handler_utils.send_get_and_get_response(url, headers=headers).json()
    if method == "POST":
        results = matialvarezs_request_handler_utils.send_post_and_get_response(url, headers=headers, data=data,
                                                                                convert_data_to_json=True).json()
    return eval(results['stop'])


#
# def time_sleep_with_stop_url(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
#     delay_schedule, total_time_sleep_in_seconds = get_delay_schedule(total_time_sleep, lower_boundary, upper_boundary,
#                                                                      **options)
#     url_send_pending_time = options.get('url_send_pending_time', None)
#     data = options.get('data')
#     accumulate = 0
#     pending_time = total_time_sleep_in_seconds
#     for delay in delay_schedule:
#         if options.get("debug", False):
#             print("********************************************")
#             print("DATA ACTUAL: ", options.get('data'))
#         stop_sleep = should_stop(**options)
#         accumulate += delay
#         if stop_sleep:
#             return (None, accumulate, pending_time)
#         else:
#             time.sleep(delay)
#             pending_time = pending_time - delay
#             if url_send_pending_time:
#                 headers = {"Content-Type": "application/json; charset=utf-8"}
#                 data['pending_time'] = pending_time
#                 matialvarezs_request_handler_utils.send_post_and_get_response(url_send_pending_time, headers=headers,
#                                                                               data=data,
#                                                                               convert_data_to_json=True)
#             if options.get("debug", False):
#                 print("ACCUMULATE: " + str(accumulate))
#                 print("TIEMPO PENDIENTE: " + str(pending_time))
#                 print("----------------------------------------")
#     return (True, 0, 0)


def time_sleep_with_stop_url(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    return time_sleep_v2.time_sleep_with_stop_url(total_time_sleep, lower_boundary=lower_boundary,
                                                  upper_boundary=upper_boundary, **options)


def time_sleep_with_stop_entry_field_database_condition(total_time_sleep, entry, atributte, atributte_equals_to,
                                                        lower_boundary=1, upper_boundary=10, **options):
    return time_sleep_with_stop_entry_field_database_condition(total_time_sleep, entry, atributte, atributte_equals_to,
                                                               lower_boundary=lower_boundary, upper_boundary=upper_boundary, **options)
    # '''
    # SE RECALCULA EL DELAY RESTANDO LOS TIEMPOS DEL RECUEST SHOULD_STOP Y EL OPCIONAL DE ENVIAR EL TIEMPO PENDIENTE,
    # EJECUTANDO EL TIME SLEEP CON LA RESTA EXACTA CON TODOS LOS DECIMALES
    # :param total_time_sleep:
    # :param lower_boundary:
    # :param upper_boundary:
    # :param options:
    # :return:
    # '''
    # delay_schedule, total_time_sleep_in_seconds = get_delay_schedule(total_time_sleep, lower_boundary,
    #                                                                       upper_boundary,
    #                                                                       **options)
    # url_send_pending_time = options.get('url_send_pending_time', None)
    # data = options.get('data')
    # accumulate = 0
    # pending_time = total_time_sleep_in_seconds
    # for delay in delay_schedule:
    #     if options.get("debug", False):
    #         print("********************************************")
    #         print("DATA ACTUAL: ", options.get('data'))
    #     start_time_should_stop = time.time()
    #     stop_sleep = should_stop(**options)
    #     finish_time_should_stop = time.time()
    #     diff_time_should_stop = finish_time_should_stop - start_time_should_stop
    #     accumulate += delay
    #     if stop_sleep:
    #         return (None, accumulate, pending_time)
    #     else:
    #         if options.get("debug", False):
    #             print("CURRENT DELAY: ", delay)
    #         pending_time = pending_time - delay
    #         new_delay = delay - diff_time_should_stop
    #         if url_send_pending_time:
    #             headers = {"Content-Type": "application/json; charset=utf-8"}
    #             data['pending_time'] = pending_time
    #             start_time_update_pending_time = time.time()
    #             # print("DATA ENVIADA ACTUALIZAR TIEMPO PENDIENTE: ", data)
    #             matialvarezs_request_handler_utils.send_post_and_get_response(url_send_pending_time,
    #                                                                           headers=headers,
    #                                                                           data=data,
    #                                                                           convert_data_to_json=True)
    #             finish_time_update_pending_time = time.time()
    #             diff_time_update_pending_time = finish_time_update_pending_time - start_time_update_pending_time
    #             new_delay = new_delay - diff_time_update_pending_time
    #         time.sleep(abs(new_delay))
    #         if options.get("debug", False):
    #             print("ACCUMULATE: " + str(accumulate))
    #             print("TIEMPO PENDIENTE: " + str(pending_time))
    #             print("----------------------------------------")
    #         print("CURRENT, NEW DELAY: ", new_delay)
    # return (True, 0, 0)
