from nlu.pipe_components import SparkNLUComponent, NLUComponent

class Util(SparkNLUComponent):

    def __init__(self,component_name='pragmatic_sentence_detector', component_type='sentence_detector'):
        # super(Tokenizer,self).__init__(component_name = component_name, component_type = component_type)
        SparkNLUComponent.__init__(self,component_name,component_type)
        if component_name == 'deep_sentence_detector':
            from nlu import DeepSentenceDetector # wierd import issue ... does not work when outside scoped.
            self.model =  DeepSentenceDetector.get_default_model()
        elif component_name == 'pragmatic_sentence_detector' :
            from nlu import PragmaticSentenceDetector
            self.model =  PragmaticSentenceDetector.get_default_model()