
from . import settings
import os, time, random
from matialvarezs_request_handler import utils as matialvarezs_request_handler_utils


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



def time_sleep_with_stop_url(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule, total_time_sleep_in_seconds = get_delay_schedule(total_time_sleep, lower_boundary, upper_boundary,
                                                                     **options)
    url_send_pending_time = options.get('url_send_pending_time', None)
    data = options.get('data')
    accumulate = 0
    pending_time = total_time_sleep_in_seconds
    for delay in delay_schedule:
        if options.get("debug", False):
            print("********************************************")
            print("DATA ACTUAL: ", options.get('data'))
        stop_sleep = should_stop(**options)
        accumulate += delay
        if stop_sleep:
            return (None, accumulate, pending_time)
        else:
            time.sleep(delay)
            pending_time = pending_time - delay
            if url_send_pending_time:
                headers = {"Content-Type": "application/json; charset=utf-8"}
                data['pending_time'] = pending_time
                matialvarezs_request_handler_utils.send_post_and_get_response(url_send_pending_time, headers=headers,
                                                                              data=data,
                                                                              convert_data_to_json=True)
            if options.get("debug", False):
                print("ACCUMULATE: " + str(accumulate))
                print("TIEMPO PENDIENTE: " + str(pending_time))
                print("----------------------------------------")
    return (True, 0, 0)


