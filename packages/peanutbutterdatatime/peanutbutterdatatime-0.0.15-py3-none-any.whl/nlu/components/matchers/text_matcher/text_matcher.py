import sparknlp

class TextMatcher:
    @staticmethod
    def get_default_model():
        return   sparknlp.annotator.RegexMatcherModel.pretrained() \
            .setInputCols("document") \
            .setOutputCol("entity") \


    @staticmethod
    def get_pretrained_model(name, language):
        return   sparknlp.annotator.RegexMatcherModel.pretrained(name,language) \
            .setInputCols("document") \
            .setOutputCol("entity") \


