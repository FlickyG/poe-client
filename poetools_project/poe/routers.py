#!/bin/Python

class PoeRouter(object): 
    def db_for_read(self, model, **hints):
        #print("hello from PoeRouter")
        if model._meta.model_name == 'poeuser':
            return 'default'
        elif model._meta.app_label == 'poe':            
            return 'poe_db'
        #if model._meta.app_label == 'poe_auth':
        #    #print("app label ", model._meta.app_label)
        #    return 'default'
        else:
            return 'default'
    
    def db_for_write(self, model, **hints):
        #print("hello from PoeRouter db_for_write")
        return self.db_for_read(model, **hints)

    
    def allow_relation(self, obj1, obj2, **hints):
        #print("hello from PoeRouter allow_realtion")
        if obj1._meta.app_label == 'poe' or \
            obj2._meta.app_label == 'poe':
            return True
        else:
            return None
        
    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if model_name != 'poeuser' and app_label == 'poe':
            #print("poe_db" == db, "model_name", model_name, "app_label", app_label)
            return 'poe_db' == db
        else:
            #print("default" == db, "model_name", model_name, "app_label", app_label)
            return 'default' == db 