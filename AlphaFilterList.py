#-----------------------------------------------------------------------------
# Copyright (c) 2023 Doug Bellinger
# All rights reserved.
#
# The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------
import param
import panel as pn
pn.extension()
class AlphaFilterList(param.Parameterized):
    letters = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    all = param.List(precedence=-1)
    name = param.String(default="Objects")
    filter = param.ListSelector(objects=letters)
    selector = param.ListSelector(objects=['1','2'])
    width = param.Integer(default=100, precedence=-1)
    
    def count_matches(self, w):
        return(sum(map(lambda x: 1 if x in w else 0, self.filter)))

    def match_all(self):
        return [w for w in self.all if (self.count_matches(w)==len(self.filter))]

    def match_any(self):
        return [w for w in self.all if (self.count_matches(w)>0)]
   
    def match_none(self):
        return [w for w in self.all if (self.count_matches(w)==0)]

    def starts_with(self):
        return [w for w in self.all if w[0] in self.filter]

    def __init__(self, func=None, **params):
        self.function = func if func else self.starts_with
        super(AlphaFilterList, self).__init__(**params)
        self.updateOptions() 

    @param.depends('all', watch=True)
    def updateOptions(self):
        self.selector = []
        self.param.selector.objects = self.all

    @param.depends('filter', watch=True)
    def updateFilter(self):
        if (self.selector):
            self.param.selector.objects = self.selector + self.function(self)
        else:
            self.param.selector.objects =  self.function(self)
        return   
    
    def __new_class(self, cls, **kwargs):
        return type(type(cls).__name__, (cls,), kwargs)
    
    def view(self):
        alphaFilterView = pn.Param(
                self,default_layout=self.__new_class(pn.GridBox, ncols=2),
                    show_name=False,
                    widgets = {
                        "filter": {"type": pn.widgets.MultiSelect,
                                    "size":26, "width": 70}, 
                        "selector": {"type": pn.widgets.MultiSelect, "name":self.name, 
                                     "size":26, "width": self.width}
                    } )
        return(alphaFilterView)
