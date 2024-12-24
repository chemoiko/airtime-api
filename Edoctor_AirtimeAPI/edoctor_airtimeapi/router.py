class DashboardRouter:
    dashboard_db = "dashboard_users"
    default_db = "default"

    def db_for_read(self, model, **hints):
        model_name = model._meta.app_label
        print("using model: ",model_name)
        if model_name == 'dashboard_users':
            return self.dashboard_db
        else:
            return None

    def db_for_write(self, model, **hints):

        model_name = model._meta.app_label
        print("using model: ",model_name)
        #model_name
        if model_name == 'dashboard_users':
            return self.dashboard_db
        else:
            return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'dashboard_users':
            return db == 'dashboard_users'
        else:
            return db == 'default'
