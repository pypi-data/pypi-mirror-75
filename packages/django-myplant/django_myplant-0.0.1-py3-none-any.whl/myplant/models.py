from django.db import models
from django.conf import settings
import sys
import inspect

PLANT = settings.PLANT

import importlib

class NewMetaclass(type):
    pass

class NewModel(models.Model): # metaclass=NewMetaclass

    @classmethod
    def get_db(cls, plant):
        classname = PLANT[plant] + cls.__name__
        return importlib.import_module(cls.__module__).__dict__[classname]

    class Meta:
        abstract = True


def create_p_db(table, plant, unique=[], **kwargs):

    class Meta:
        db_table = table.__name__.lower() + '_' + plant
        verbose_name = PLANT[plant] + table.Meta.verbose_name
        verbose_name_plural = verbose_name

    class_name = PLANT[plant] + table.__name__
    class_dict = {}
    class_dict['__module__'] = table.__module__
    class_dict['Meta'] = Meta

    def get_foreignkey(table, unique2, chinese):
        if unique2:
            return models.ForeignKey(table.get_db(plant), on_delete=models.CASCADE, default='', unique=True, verbose_name=chinese)
        else:
            return models.ForeignKey(table.get_db(plant), on_delete=models.CASCADE, default='', verbose_name=chinese)

    if hasattr(table, 'FK'):
        for k, v in table.FK.__dict__.items():
            if inspect.isclass(getattr(table.FK, k)):
                class_dict[k] = get_foreignkey(v, False, v.Meta.verbose_name)
    
    # for k, v in kwargs.items():
    #     if k in unique:
    #         class_dict[k] = get_foreignkey(v, True, v.Meta.verbose_name)
    #     else:
    #         class_dict[k] = get_foreignkey(v, False, v.Meta.verbose_name)
    return type(class_name, (table,), class_dict)

def create_all_db(models):
    for model in models:
        v = importlib.import_module(model.__module__).__dict__
        for p in PLANT.keys():
            P = PLANT[p] # Plant plant
            v[P + model.__name__]  = create_p_db(model, p)