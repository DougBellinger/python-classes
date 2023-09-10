#-----------------------------------------------------------------------------
# Copyright (c) 2023 Doug Bellinger
# All rights reserved.
#
# The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------
import param
import panel as pn
import logging
pn.extension()

logger = logging.getLogger('panel.AlphaFilterList')

class AlphaFilterList(param.Parameterized):
    letters = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    all = []
    name = param.String(default="Objects")
    filter = param.ListSelector(default=[],objects=letters)
    selector = param.ListSelector(objects=['1','2'])
    width = param.Integer(default=100, precedence=-1)
    
    def count_matches(self, w):
        return(sum(map(lambda x: 1 if x in w else 0, self.filter)))

    def match_all(self):
        return [w for w in self.param.selector.objects if (self.count_matches(w)==len(self.filter))]

    def match_any(self):
        return [w for w in self.param.selector.objects if (self.count_matches(w)>0)]
   
    def match_none(self):
        return [w for w in self.param.selector.objects if (self.count_matches(w)==0)]

    def starts_with(self):
        return [w for w in self.param.selector.objects if w[0] in self.filter]

    def __init__(self, func=None, **params):
        logger.debug(f"Creating AlphaFilterList {self.name}")
        self.function = func if func else self.starts_with
        self.all = all if all else []
        #self.filter=filter if filter else []
        super(AlphaFilterList, self).__init__(**params)
        self.update_options() 

    def reset_filter(self):
        self.param.filter.objects = self.letters
        self.param.filter = []
        self.param.selector.objects = self.all
        self.param.selector=[]

    @param.depends('all', watch=True)
    def update_options(self):
        logger.debug(f"{self.name} update filter")
        self.selector = []
        self.param.selector.objects = self.all

    @param.depends('filter', watch=True)
    def update_filter(self):
        logger.debug(f"{self.name} update filter")
        if (self.selector):
            self.param.selector.objects = self.selector + self.function(self)
        else:
            self.param.selector.objects =  self.function(self)
        return   
    
    def get_objects(self):
        return(self.param.selector.objects)
    
    def drop_letters(self, to_drop):
        logger.debug(f"{self.name} dropping letters {to_drop}")
        if not to_drop:
            return
        self.param.filter.objects = [x for x in self.letters
                                     if x not in to_drop]
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
