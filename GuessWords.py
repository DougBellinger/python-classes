import logging
import panel as pn

logger = logging.getLogger("GuessWords")

class GuessLetter(pn.widgets.TextInput):
    def _guess_letter_change(self, e):
        e.obj.value = e.new.upper()
        if len(e.new)== 2:
            logger.debug(f'Style {e.new[0]} to {e.new[1]}')
            match e.new[1]:
                case '!':
                    self.styles ={'border':'8px solid black', 'border-radius':'20%'}
                    self.match = 0
                case '?':
                    self.styles ={'border':'8px solid yellow', 'border-radius':'20%'}  
                    self.match = -1 
                case '=':
                   self.styles ={'border':'8px solid green', 'border-radius':'20%'}
                   self.match = 1
        elif len(e.new)==1:
            self.styles ={'border':'8px solid black', 'border-radius':'20%'}
            self.match = 0
        else:
            self.styles ={'border':'8px solid grey', 'border-radius':'20%'}
            self.match = 0

    def __init__(self, guess, letter, **params):
        self.guess=guess
        self.letter=letter
        self.match=0
        params.pop("guess", None)
        params.pop("letter", None)
        super(GuessLetter, self).__init__(max_length=2, width=60, height=50, **params)
        self.styles = {'border': '8px solid grey', 'border-radius':'20%' }
        self.param.watch(self._guess_letter_change, ['value_input'], onlychanged=False)

class WordValue(pn.widgets.StaticText):
    def set_style(self):
          color = "green" if self.in_fives else "red"
          self.styles ={"color":color, 
                        "padding":"8px",
                        "padding-top":"10px",
                        'border': f"8px solid {color}",
                        'border-radius':"25%"}

    def _word_value_change(self,e):
        logger.debug(f"word {self.value} event: {e} ")
        if (self.value.find("_")!=-1):
            logger.debug("incomplete word")
            return
        #todo... update style if not in self.source_words
        if (self.value in self.source_words):
            self.in_fives = True
            logger.debug("Word is in self.source_words")
            self.set_style()
        else:
            self.in_fives = False
            logger.debug("Word is not in self.source_words")
            self.set_style()

    #word = param.String('_____', regex='[A-Z_]{5}')
    def __init__(self, guess, source_words, **params):
        self.guess = guess
        self.in_fives = False
        self.source_words = source_words
        params.pop("guess", None)
        super(WordValue, self).__init__(height=50, width=70, **params)
        self.value = "_____"
        self.param.watch(self._word_value_change, ['value'], onlychanged=False)
        self.set_style()

class GuessWord(pn.GridBox):
    def _word_letter_change(self, e):
        logger.debug(f"word {self.guess} letter changed:{int(e.obj.guess)}-{e.obj.letter}: {e.new}")
        if (len(e.new)>=1):
            l = e.new[0].upper()
        else:
            l = '_'
        self.word.value = self.word.value[:e.obj.letter]+l+self.word.value[e.obj.letter+1:]
        logger.debug(f"guess: {self.word.value}")
        self.objects[5].value = self.word.value

    def current_guess(self):
        return(self.objects[-1])
    
    def include_letters(self):
        inc = []
        for i in range(0, len(self.objects)-1):
            if (len(self.objects[i].value) >= 1):
                if (abs(self.objects[i].match) == 1):
                    inc.append(self.objects[i].value[0])
                    logger.debug(f"Including:{self.objects[i].value}({self.objects[i].match})")
        return(inc if len(inc)>0 else None)
    
    def exclude_letters(self):
        ex = []
        for i in range(0, len(self.objects)-1):
            if (len(self.objects[i].value) >= 1):
                if (self.objects[i].match == 0):
                    ex.append(self.objects[i].value[0])
                    logger.debug(f"Excluding:{self.objects[i].value}({self.objects[i].match})")
                # Replace letter for case of "E" followed by "E?" or "E="... there is an E
                # TOOD: this pattern says "there is one but not two E's"  Algorithm will continue
                # to include words with two E's
                elif ((self.objects[i].match == 1) and (self.objects[i].value[0] in ex)):
                    logger.debug(f"Taking {self.objects[i].value[0]} out of exclude")
                    ex.remove(self.object[i].value[0])
        return(ex if len(ex)>0 else None)
    
    def match_string(self):
        m =""
        for i in range(0, len(self.objects)-1):
            if (len(self.objects[i].value) >= 1):
                m = m + (self.objects[i].value[0] if self.objects[i].match==1 else "_")
            else:
                m = m + "_"
        return(m if m!="_"*self.length else None)

    def negative_match(self):
        m =""
        for i in range(0, self.length):
            if (len(self.objects[i].value) >= 1):
                m = m + (self.objects[i].value[0] if self.objects[i].match==-1 else "_")
            else:
                m = m + "_"
        return(m if m!="_"*self.length else None)

    def __init__(self, guess, source_words, length=5,  **params):
        self.word = WordValue(guess, source_words)
        super(GuessWord, self).__init__(nrows=1, ncols=length+1, **params)
        self.guess = guess
        self.length = length
        # self.source_words = source_words
        self.objects = [GuessLetter(guess, letter) for letter in 
                            range(0,self.length)]+[self.word]
        for i in range(0,self.length):
            self.objects[i].param.watch(self._word_letter_change, ['value_input'], onlychanged=False)