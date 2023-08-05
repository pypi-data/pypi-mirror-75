from nlu.pipe_components import SparkNLUComponent, NLUComponent

class Stemmer(SparkNLUComponent):
    def __init__(self,component_name='stemmer', component_type='stemmer',model = None):
        if model != None : self.model = model
        else :

            # super(Tokenizer,self).__init__(component_name = component_name, component_type = component_type)
            SparkNLUComponent.__init__(self,component_name,component_type)
            if component_name == 'stemmer':
                from nlu import SparkNLPStemmer # wierd import issue ... does not work when outside scoped.
                self.model =  SparkNLPStemmer.get_default_model()
