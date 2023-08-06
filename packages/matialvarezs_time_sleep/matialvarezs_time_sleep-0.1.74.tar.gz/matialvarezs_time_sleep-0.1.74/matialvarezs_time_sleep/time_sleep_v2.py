from . import settings
import os, time, random, math
from matialvarezs_request_handler import utils as matialvarezs_request_handler_utils


def get_delay_schedule(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule = list()
    frac_total_time_sleep, whole_total_time_sleep = math.modf(total_time_sleep)
    if options.get('time_in_minutes', False) is True:
        total_time_sleep = whole_total_time_sleep * 60
    if math.trunc(whole_total_time_sleep) == 0:
        delay_schedule.append(total_time_sleep)
    if math.trunc(whole_total_time_sleep) > 0:
        while True:
            random_time = random.randint(lower_boundary, upper_boundary)
            if sum(delay_schedule) + random_time > total_time_sleep:
                continue
            else:
                delay_schedule.append(random_time)
            if sum(delay_schedule) == math.trunc(total_time_sleep):
                break

    if frac_total_time_sleep > 0:
        delay_schedule.append(frac_total_time_sleep)

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
    start_time_should_stop = time.time()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = kwargs.get('url', '')
    method = kwargs.get('method', "GET")
    data = kwargs.get('data', {})
    results = {}
    if method == "GET":
        results = matialvarezs_request_handler_utils.send_get_and_get_response(url, headers=headers).json()
    if method == "POST":
        results = matialvarezs_request_handler_utils.send_post_and_get_response(url, headers=headers, data=data,
                                                                                convert_data_to_json=True).json()
    finish_time_should_stop = time.time()
    diff_time_should_stop = finish_time_should_stop - start_time_should_stop
    if results:
        return eval(results['stop']), diff_time_should_stop
    return False,diff_time_should_stop

def time_sleep_with_stop_url(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    '''
       SE RECALCULA EL DELAY RESTANDO LOS TIEMPOS DEL RECUEST SHOULD_STOP Y EL OPCIONAL DE ENVIAR EL TIEMPO PENDIENTE,
       EJECUTANDO EL TIME SLEEP CON LA RESTA EXACTA CON TODOS LOS DECIMALES
       :param total_time_sleep:
       :param lower_boundary:
       :param upper_boundary:
       :param options:
       :return:
       '''
    delay_schedule, total_time_sleep_in_seconds = get_delay_schedule(total_time_sleep, lower_boundary,
                                                                     upper_boundary,
                                                                     **options)
    url_send_pending_time = options.get('url_send_pending_time', None)
    data = options.get('data')
    accumulate = 0
    pending_time = total_time_sleep_in_seconds
    for delay in delay_schedule:
        if options.get("debug", False):
            print("********************************************")
            print("DATA ACTUAL: ", options.get('data'))
        # start_time_should_stop = time.time()
        stop_sleep, diff_time_should_stop = should_stop(**options)
        # finish_time_should_stop = time.time()
        # diff_time_should_stop = finish_time_should_stop - start_time_should_stop
        diff_time_update_pending_time = 0
        accumulate += delay
        if stop_sleep:
            return (None, accumulate, pending_time)
        else:
            print("CURRENT DELAY: ", delay)
            time.sleep(delay)
            pending_time = pending_time - delay
            new_total_time = pending_time - diff_time_should_stop
            if url_send_pending_time:
                headers = {"Content-Type": "application/json; charset=utf-8"}
                data['pending_time'] = pending_time
                start_time_update_pending_time = time.time()
                print("DATA ENVIADA ACTUALIZAR TIEMPO PENDIENTE: ", data)
                matialvarezs_request_handler_utils.send_post_and_get_response(url_send_pending_time,
                                                                              headers=headers,
                                                                              data=data,
                                                                              convert_data_to_json=True)
                finish_time_update_pending_time = time.time()
                diff_time_update_pending_time = finish_time_update_pending_time - start_time_update_pending_time
                new_total_time = new_total_time - diff_time_update_pending_time
            if options.get("debug", False):
                print("ACCUMULATE: " + str(accumulate))
                print("TIEMPO PENDIENTE: " + str(pending_time))
                print("----------------------------------------")

            print("new_total_time: ", new_total_time)
            if new_total_time > 0:
                return time_sleep_with_stop_url(
                    new_total_time,
                    1, 5, debug=True,
                    url=options.get('url'),
                    url_send_pending_time=url_send_pending_time,
                    method="POST",
                    data=data,
                    time_in_minutes=False)
            return (True, 0, 0)
    return (True, 0, 0)
