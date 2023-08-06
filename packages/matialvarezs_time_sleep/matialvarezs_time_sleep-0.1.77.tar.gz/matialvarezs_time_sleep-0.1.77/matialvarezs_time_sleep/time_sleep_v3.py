from . import settings
import os, time, random, math, json
from matialvarezs_request_handler import utils as matialvarezs_request_handler_utils
# from . import signals
from paho.mqtt import publish as publish
from matialvarezs_handlers_easy import mqtt as mqtt_utils
'''
VERSION 3:
- CHECK STOP INTO DATABASE
- SEND PENDING TIME BY MQTT

'''


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


def should_stop(entry, atributte, atributte_equals_to):
    start_time_should_stop = time.time()
    entry.refresh_from_db()
    finish_time_should_stop = time.time()
    diff_time_should_stop = finish_time_should_stop - start_time_should_stop
    # if entry:
    stop = entry.__getattribute__(atributte) == atributte_equals_to
    return stop, diff_time_should_stop
    # return False,diff_time_should_stop


def send_by_http_pending_time(data, pending_time, url_send_pending_time):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data['pending_time'] = pending_time
    start_time_update_pending_time = time.time()
    print("DATA ENVIADA ACTUALIZAR TIEMPO PENDIENTE: ", data)
    start_time_update_pending_time = time.time()
    matialvarezs_request_handler_utils.send_post_and_get_response(url_send_pending_time,
                                                                  headers=headers,
                                                                  data=data,
                                                                  convert_data_to_json=True)
    finish_time_update_pending_time = time.time()
    return finish_time_update_pending_time - start_time_update_pending_time


def send_by_mqtt_pending_time(topic, payload, broker, qos, auth, client_id, pending_time):
    payload['pending_time'] = pending_time
    start_time_update_pending_time = time.time()
    result = mqtt_utils.publish_simgle(topic=topic, payload=json.dumps(payload), hostname=broker, qos=qos, auth=auth, client_id=client_id)
    print("result publish desde modulo time sleep: ",result)
    finish_time_update_pending_time = time.time()
    return finish_time_update_pending_time - start_time_update_pending_time


def time_sleep_with_stop_entry_field_database_condition(protocol, total_time_sleep, entry, atributte,
                                                        atributte_equals_to,
                                                        lower_boundary=1, upper_boundary=10, **options):
    '''
       SE RECALCULA EL DELAY RESTANDO LOS TIEMPOS DE ACTUALIZACIÓN DEL OBJETO DESDE LA DB
       Y EL OPCIONAL DE ENVIAR EL TIEMPO PENDIENTE POR HTTP,
       EJECUTANDO EL TIME SLEEP CON LA RESTA EXACTA CON TODOS LOS DECIMALES
       ;:param protocol - http or mqtt
       :param total_time_sleep:
       :param model_database
       :param kwargs_query
       :param kwargs_query
       :param  atributte_equals_to
       :param lower_boundary:
       :param upper_boundary:
       :param options:


       kwargs
       ;:param url_send_pending_time => url to send pending time
       ;:param data => data to send by http or mqtt to url or topic
       ;:param method => http method: get or post
       :return:
       '''
    delay_schedule, total_time_sleep_in_seconds = get_delay_schedule(total_time_sleep, lower_boundary,
                                                                     upper_boundary,
                                                                     **options)
    url_send_pending_time = options.get('url_send_pending_time', None)
    topic = options.get('topic', '#')
    broker = options.get('broker', 'localhost')
    qos = options.get('qos', 2)
    payload = options.get('payload', {})
    auth_mqtt = options.get('auth_mqtt', None)
    client_id_mqtt = options.get('client_id_mqtt', 'matialvarezs-module-time-sleep')
    data = options.get('data')
    accumulate = 0
    pending_time = total_time_sleep_in_seconds
    for delay in delay_schedule:
        if options.get("debug", False):
            print("********************************************")
            # print("DATA ACTUAL: ", options.get('data'))
        # start_time_should_stop = time.time()
        stop_sleep, diff_time_should_stop = should_stop(entry, atributte, atributte_equals_to)
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
            print("diff_time_should_stop: ", diff_time_should_stop)
            new_total_time = pending_time - diff_time_should_stop
            if protocol.upper() == "HTTP":
                diff_time_update_pending_time = send_by_http_pending_time(data, pending_time, url_send_pending_time)
            if protocol.upper() == "MQTT":
                send_by_mqtt_pending_time(topic, payload, broker, qos, auth_mqtt, client_id_mqtt+'-matialvarezs-module-time-sleep', pending_time)
                # if url_send_pending_time:
                #     headers = {"Content-Type": "application/json; charset=utf-8"}
                #     data['pending_time'] = pending_time
                #     start_time_update_pending_time = time.time()
                #     print("DATA ENVIADA ACTUALIZAR TIEMPO PENDIENTE: ", data)
                #     matialvarezs_request_handler_utils.send_post_and_get_response(url_send_pending_time,
                #                                                                   headers=headers,
                #                                                                   data=data,
                #                                                                   convert_data_to_json=True)
                #    finish_time_update_pending_time = time.time()

                # signals.send_pending_time.send(sender=None, data=data)
                #    diff_time_update_pending_time = finish_time_update_pending_time - start_time_update_pending_time
                new_total_time = new_total_time - diff_time_update_pending_time
            # if settings.MQTT_BROKER and settings.MQTT_PORT  and settings.MQTT_USER and settings.MQTT_PASSWORD:
            #     start_time_update_pending_time = time.time()
            #     payload = {
            #         'pending_time': pending_time
            #     }
            #     mqtt_topic = options.get('mqtt_topic')
            #     auth = {settings.MQTT_USER, settings.MQTT_PASSWORD}
            #     result_publish = publish.single(topic=mqtt_topic, payload=payload, port=1883, hostname=settings.MQTT_BROKER,
            #                    auth=auth)
            #     print("RESULT PUBLISH: ",result_publish)
            #     finish_time_update_pending_time = time.time()
            #     diff_time_update_pending_time = finish_time_update_pending_time - start_time_update_pending_time
            #     print("diff_time_update_pending_time: ",diff_time_update_pending_time)
            #     new_total_time = new_total_time - diff_time_update_pending_time
            if options.get("debug", False):
                print("ACCUMULATE: " + str(accumulate))
                print("TIEMPO PENDIENTE: " + str(pending_time))
                print("----------------------------------------")

            # print("new_total_time: ", new_total_time)
            if new_total_time > 0:  # and protocol.upper() == "HTTP":
                return time_sleep_with_stop_entry_field_database_condition(
                    protocol, new_total_time, entry, atributte, atributte_equals_to,
                    1, 5, debug=True,
                    url=options.get('url'),
                    url_send_pending_time=url_send_pending_time,
                    method="POST",
                    data=data,
                    topic=topic,
                    broker=broker,
                    payload=payload,
                    qos=qos,
                    client_id_mqtt=client_id_mqtt,
                    auth_mqtt=auth_mqtt,
                    time_in_minutes=False)
            return (True, 0, 0)

    return (True, 0, 0)
