from django.contrib import admin
from django.conf import settings
# Register your models here.
PLANT = settings.PLANT
import importlib

def get_AdminPage(model_name, *args, **kwargs):
    base_class = (admin.ModelAdmin, )
    if args:
        base_class = args
    show_dict = {}
    for k,v in mylist.__dict__.items():
        if isinstance(getattr(mylist, k), dict):
            show_dict[k] = v.get(model_name, ())
    show_dict.update(kwargs)
    
    return type('AdminPage', base_class, show_dict)


def admin_register(lists):
    global mylist
    mylist = lists
    register_models = importlib.import_module(lists.__module__).__dict__['register_model']
    for plant in PLANT.keys():
        for table in register_models:
            admin.site.register(table.get_db(plant), get_AdminPage(table.__name__))

def admin_register_importexport(model, base_class, resource_class):
    for plant in PLANT.keys():
        admin.site.register(model.get_db(plant), 
                            get_AdminPage(model.__name__, base_class, resource_class = resource_class(plant))) 
