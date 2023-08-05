from nlu.pipe_components import SparkNLUComponent, NLUComponent

class Util(SparkNLUComponent):

    def __init__(self,component_name='document_assembler', component_type='util', model = None):
        # super(Tokenizer,self).__init__(component_name = component_name, component_type = component_type)
        SparkNLUComponent.__init__(self,component_name,component_type)
        if model != None : self.model = model
        else :
            if component_name == 'document_assembler':
                from nlu import SparkNlpDocumentAssembler # wierd import issue ... does not work when outside scoped.
                self.model =  SparkNlpDocumentAssembler.get_default_model()
            elif component_name == 'sentence_detector' :
                from nlu import SparkNLPSentenceDetector # wierd import issue ... does not work when outside scoped.
                self.model =  SparkNLPSentenceDetector.get_default_model()