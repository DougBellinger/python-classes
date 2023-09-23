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
from panel.theme import  Material

logger = logging.getLogger('panel.AlphaFilterList')

class AlphaFilter():
    def count_matches(word, letters):
        return(sum(map(lambda x: 1 if x in word else 0, letters)))

    def match_all(words, letters):
        return [w for w in words if (AlphaFilter.count_matches(w)==len(letters))]

    def match_any(words, letters):
        return [w for w in words if (AlphaFilter.count_matches(letters)>0)]
   
    def match_none(words, letters):
        return [w for w in words if (AlphaFilter.count_matches(w, letters)==0)]

    def starts_with(words, letters):
        return [w for w in words if w[0] in letters]

class AlphaFilterList(param.Parameterized):
    letters = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    all = None
    design = None
    styles = None
    name = param.String(default="Objects")
    filter = param.ListSelector(default=[],objects=letters)
    selector = param.ListSelector(objects=['1','2'])
    width = param.Integer(default=100, precedence=-1)

    def __init__(self, all=None, styles=None, func=None, design=Material, **params):
        logger.debug(f"Creating AlphaFilterList {self.name}")
        self.function = func if func else self.starts_with
        self.styles = styles if styles else None
        self.design = design if design else Material
        self.all = all if all else list()
        #self.filter=filter if filter else []
        logger.debug(f"params:{params}")
        params.pop("all", None)
        params.pop("styles", None)
        params.pop("design", None)
        #logger.debug(f"params:{params}")
        super(AlphaFilterList, self).__init__(**params)
        self.update_options() 

    def reset_filter(self):
        self.param.filter.objects = self.letters
        self.param.filter = []
        self.param.selector.objects = self.all
        self.param.selector=[]

    #@param.depends('all', watch=True)
    def update_options(self):
        logger.debug(f"{self.name} update all")
        self.selector = []
        self.param.selector.objects = self.all

    @param.depends('filter', watch=True)
    def update_filter(self):
        logger.debug(f"{self.name} update filter")
        if (self.selector):
            self.param.selector.objects = self.selector + self.function(self.param.selector.objects,self.filter)
        else:
            self.param.selector.objects =  self.function(self.param.selector.objects,self.filter)
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
                                    "size":26, "width": 70, 
                                    "design":self.design}, 
                        "selector": {"type": pn.widgets.MultiSelect, "name":self.name, 
                                     "size":26, "width": self.width, 
                                     "design":self.design}
                    } )
        if (self.styles):
            alphaFilterView.widgets["filter"].styles = self.styles
            alphaFilterView.widgets["selector"].styles = self.styles
        return(alphaFilterView)
