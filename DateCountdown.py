from datetime import date
from dateutil import relativedelta
from dateutil.rrule import rrule, DAILY
import holidays

import param
import panel as pn
pn.extension()

class DateCountdown(param.Parameterized):
    d0 = param.Date(date.today(), precedence=-1)
    d1 = param.Date(date(2025, 6, 14), precedence=-1)
    total_days = param.Integer(default=0, precedence=-1)
    business_days = param.Integer(default=0, precedence=-1)
    country = param.String(default = "CA", precedence=-1)
    years = param.Integer(default=0)
    months = param.Integer(default=0)
    days = param.Integer(default=0)
    #delta = d1 - d0

    def __init__(self, func=None, **params):
        super(DateCountdown, self).__init__(**params)

    def __new_class(self, cls, **kwargs):
        return type(type(cls).__name__, (cls,), kwargs)
    
    def holidays(self):
        h = holidays.country_holidays(self.country)
        return([dt for dt in rrule(DAILY, dtstart=self.d0, until=self.d1) 
                if (dt in h) or (dt.weekday()>=5)])
    
    def count_holidays(self):
        return(len(self.holidays()))
    
    def update(self):
        delta = relativedelta.relativedelta(self.d1, self.d0)
        self.years = delta.years
        self.months = delta.months
        self.days = delta.days
        self.total_days = (self.d1-self.d0).days
        self.business_days = self.total_days - self.count_holidays()

    def view(self):
        self.update()
        dateCountdownView = pn.Param(
                self,default_layout=self.__new_class(pn.GridBox, ncols=3),
                    show_name=False,
                    widgets = {
                        "years": {"type": pn.widgets.Number}, 
                        "months": {"type": pn.widgets.Number}, 
                        "days": {"type": pn.widgets.Number}
                    } )
        return(dateCountdownView)
    
    def business_view(self):
        self.update()
        number = pn.indicators.Number(
             name='Business Days', value=self.business_days, format='{value}')    
        return(number)