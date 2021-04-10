class VaccineSummary:

    def __init__(self, index, range_age, total, male, female, health_workers, not_health_workers, rsa_hosts, over_80, armed_for, scool_emp, first_dose, second_dose, last_update):
        self.index = index
        self.range_age = range_age
        self.total = total
        self.male = male
        self.female = female
        self.health_workers = health_workers
        self.not_health_workers = not_health_workers
        self.rsa_hosts = rsa_hosts
        self.over_80 = over_80
        self.scool_emp = scool_emp
        self.armed_for = armed_for
        self.first_dose = first_dose
        self.second_dose = second_dose
        self.last_update = last_update
    
        def get_index(self):
            return self.index
        def set_index(self, index):
            self.index = index
        
        def get_range_age(self):
            return self.range_age
        def set_range_age(self, range_age):
            self.range_age = range_age
        
        def get_total(self):
            return self.total
        def set_total(self, total):
            self.total = total
        
        def get_male(self):
            return self.male
        def set_male(self, male):
            self.male = male
        
        def get_female(self):
            return self.female
        def set_male(self, female):
            self.female = female

        def get_health_workers(self):
            return self.health_workers
        def set_male(self, health_workers):
            self.health_workers = health_workers

        def get_not_health_workers(self):
            return self.not_health_workers
        def set_not_health_workers(self, not_health_workers):
            self.not_health_workers = not_health_workers

        def get_rsa_hosts(self):
            return self.rsa_hosts
        def set_rsa_hosts(self, rsa_hosts):
            self.rsa_hosts = rsa_hosts
        
        def get_last_update(self):
            return self.last_update
        def set_last_update(self, last_update):
            self.last_update = last_update