from nlu.pipe_components import SparkNLUComponent, NLUComponent

class Tokenizer(SparkNLUComponent):

    def __init__(self,component_name='spark_nlp_tokenizer', language='en', component_type='tokenizer', get_default = True,sparknlp_reference=''):
        if 'token' in component_name : component_name = 'spark_nlp_tokenizer'
        SparkNLUComponent.__init__(self,component_name,component_type)
        if component_name == 'spark_nlp_tokenizer' or 'token' in component_name:
            from nlu import SparkNLPTokenizer
            if get_default : self.model =  SparkNLPTokenizer.get_default_model()
            else : self.model =  SparkNLPTokenizer.get_default_model()  # there are no pretrained tokenizrs, only default 1
