from nlu import *
from nlu.pipe_components import SparkNLUComponent
from sparknlp.annotator import *
from nlu.components.embeddings import albert, bert, elmo,use, xlnet

class Classifier(SparkNLUComponent):
    def __init__(self, component_name='sentiment_dl', language='en', component_type='classifier', get_default=True ,model = None,sparknlp_reference =''):
        if 'classifierdl' in sparknlp_reference.split('_')[0] and get_default==False :
            SparkNLUComponent.__init__(self, 'classifier_dl', component_type)
            component_name='classifier_dl'
        elif 'sentimentdl' in sparknlp_reference.split('_')[0]:
            SparkNLUComponent.__init__(self, 'sentiment_dl', component_type)
            component_name='sentiment'
        else : SparkNLUComponent.__init__(self, component_name, component_type)

        #TODO GLOVE

        if model != None : self.model = model
        else :
            if 'sentiment' in component_name:
                from nlu import SentimentDl
                if get_default : self.model = SentimentDl.get_default_model()
                else : self.model = SentimentDl.get_pretrained_model(sparknlp_reference,language)
            elif 'vivekn' in component_name:
                from nlu import ViveknSentiment
                if get_default : self.model = ViveknSentiment.get_default_model()
                else : self.model = ViveknSentiment.get_pretrained_model(sparknlp_reference, language)
            elif 'ner' in component_name or 'ner.dl' in component_name:
                from nlu import NERDL
                if get_default : self.model = NERDL.get_default_model()
                else : self.model = NERDL.get_pretrained_model(sparknlp_reference,language)
            elif 'ner.crf' in component_name:
                from nlu import NERDLCRF
                if get_default : self.model = NERDLCRF.get_default_model()
                else : self.model = NERDLCRF.get_pretrained_model(sparknlp_reference,language)
            elif 'classifier_dl' in component_name:
                from nlu import ClassifierDl
                if get_default : self.model = ClassifierDl.get_default_model()
                else : self.model = ClassifierDl.get_pretrained_model(sparknlp_reference,language)
            elif 'language_detector' in component_name:
                from nlu import LanguageDetector
                if get_default : self.model = LanguageDetector.get_default_model()
                else: self.model = LanguageDetector.get_pretrained_model(sparknlp_reference, language)
            elif 'pos' in component_name:
                from nlu import PartOfSpeechJsl
                if get_default : self.model = PartOfSpeechJsl.get_default_model()
                else : self.model = PartOfSpeechJsl.get_pretrained_model(sparknlp_reference,language)
