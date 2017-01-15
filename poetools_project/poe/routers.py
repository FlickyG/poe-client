#!/bin/Python

class PoeRouter(object): 
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'poe':
            return 'poe_db'
        else:
            return 'default'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'poe':
            return 'poe_db'
        else:
            return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        if model._meta.app_label == 'poe':
            return True
        else:
            return None
        
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print("app label ", app_label, model_name, db)
        return True
        '''if app_label == 'poe':
            print(db == 'poe_db')
            return db == 'poe_db'
        if not app_label == 'poe':
            return None'''