#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    import thread
except ImportError:
    import dummy_thread as thread

from django.db.models import signals
from django.core import serializers

from models import *
from signals import *

# The state is a dictionary of lists. The key to the dict is the current
# thread and the list is handled as a stack of values.

state = {}


def get_active_histories():
    '''
    Returns histories that have been created during the current request
    '''

    (request, rq) = state.get(thread.get_ident(), (None, None))
    if rq is None:
        return FullHistory.objects.none()
    return FullHistory.objects.filter(request=rq)


def prepare_initial(entry):
    entry._fullhistory = get_all_data(entry)


def get_difference(entry):
    ret = dict()
    newdata = get_all_data(entry)
    keys = set(newdata.keys()) | set(entry._fullhistory.keys())
    for key in keys:
        oldvalue = entry._fullhistory.get(key, None)
        newvalue = newdata.get(key, None)
        if oldvalue != newvalue:
            ret[key] = (oldvalue, newvalue)
    return ret


def get_all_data(entry):
    serial = serializers.serialize('python', [entry])[0]
    serial['fields'][entry._meta.pk.name] = serial['pk']
    return serial['fields']


def get_all_data_tuple(entry):
    data = get_all_data(entry)
    for (key, value) in data.items():
        data[key] = (value, )
    return data


def get_or_create_request():
    thread_ident = thread.get_ident()
    (request, rq) = state.get(thread_ident, (None, None))
    if not rq:
        rq = Request()
        if request:
            rq.request_path = request.path
            if request.user.is_anonymous():
                rq.user_name = u'(Anonymous)'
            else:
                rq.user_pk = request.user.pk
                rq.user_name = unicode(request.user)[:255]
        else:
            rq.user_name = u'(System)'
        rq.save()
        state[thread_ident] = (request, rq)
    return rq


def create_history(entry, action):
    print action, 'fullhistory.py'
    request = get_or_create_request()
    if action == 'U':
        data = get_difference(entry)
        if len(data) == 0:
            data = get_all_data_tuple(entry)
    elif action == 'C':
        data = get_all_data_tuple(entry)
    else:
        data = None
    fh = FullHistory(data=data, content_object=entry, action=action,
                     request=request)
    fh.save()
    apply_parents(entry, lambda x: create_history(x, action))
    prepare_initial(entry)
    post_create.send(sender=type(entry), fullhistory=fh, instance=entry)
    return fh


def adjust_history(obj, action='U'):
    '''
    Adjusts the latest entry to accomidate any changes not picked up
    Likely changes are ManyToManyFields
    '''

    delta = get_difference(obj)
    if delta:
        ct = ContentType.objects.get_for_model(obj)
        try:
            history = get_active_histories().filter(content_type=ct,
                    object_id=obj.pk).latest()
        except FullHistory.DoesNotExist:
            history = FullHistory(content_object=obj,
                                  request=get_or_create_request(),
                                  action=action, data=dict())
        if history.action == 'C':
            for (key, value) in delta.items():
                delta[key] = (value[1], )
        data = history.data
        data.update(delta)
        history.data = data
        history.info = history.create_info()
        history.save()
        prepare_initial(obj)
        post_adjust.send(sender=type(obj), fullhistory=history,
                         instance=obj)
        return history
    return None


def apply_parents(instance, func):
    for field in instance._meta.parents.values():
        if field and getattr(instance, field.name, None):
            func(getattr(instance, field.name))


def init_history_signal(instance, **kwargs):
    if instance.pk is not None:
        prepare_initial(instance)
        apply_parents(instance, prepare_initial)


def save_history_signal(instance, created, **kwargs):
    print created, 'created', 'fullhistory.py'
    create_history(instance, created and 'C' or 'U')


def delete_history_signal(instance, **kwargs):
    create_history(instance, 'D')


def end_session():
    state.pop(thread.get_ident(), None)


registered_models = set()


def register_model(cls):
    if cls in registered_models:
        return
    for parent in cls._meta.parents.keys():
        register_model(parent)
    signals.post_init.connect(init_history_signal, sender=cls)
    signals.post_save.connect(save_history_signal, sender=cls)
    signals.post_delete.connect(delete_history_signal, sender=cls)
    registered_models.add(cls)


class FullHistoryMiddleware(object):

    def process_request(self, request):
        state[thread.get_ident()] = (request, None)

    def process_response(self, request, response):
        end_session()
        return response


