# BASE PIPELINE CLASS
from sparknlp import pretrained
import sparknlp
import pandas as pd
import numpy as np
from sparknlp.base import *
import logging
import nlu
logger = logging.getLogger('nlu')


from pyspark.sql.functions import flatten, explode, arrays_zip, map_keys, map_values, monotonically_increasing_id




class BasePipe():
    def __init__(self):
        self.raw_text_column = 'text'
        self.raw_text_matrix_slice = 1  # place holder for getting text from matrix
        self.spark_nlp_pipe = None
        self.needs_fitting = True
        self.is_fitted = False
        self.output_positions = False  # Wether to putput positions of Features in the final output. E.x. positions of tokens, entities, dependencies etc.. inside of the input document.
        self.output_level = 'document'  # either document, chunk, sentence, token
        self.output_different_levels = True
        self.user_has_set_output_level = False
        self.pipe_components = []  # orderd list of nlu_component objects
    def add(self, component, component_name="auto_generate"):
        self.pipe_components.append(component)
        # self.component_execution_plan.update()

class NLUPipeline(BasePipe):
    def __init__(self):
        super().__init__()
        """ Initializes a pretrained pipeline         ## todo check wether this is a sparknlp or some other pipeline """
        self.spark = sparknlp.start()
        self.provider = 'sparknlp'
        self.pipe_ready = False  # ready when we have created a spark df
        # The NLU pipeline uses  types of Spark NLP annotators to identify how to handle different columns
        self.levels = {
            'token': ['token', 'pos', 'ner', 'lemma', 'word_embeddings', 'named_entity', 'entity', 'dependency',
                      'labeled_dependency'],
            'sentence': ['sentence', 'sentence_embeddings'],
            'chunk': ['chunk', ],
            'document': ['document','language'],
            'embedding_level': ['sentiment', 'classifer']
            # embedding level  annotators output levels depend on the level of the embeddings they are fed. If we have Doc/Chunk/Word/Sentence embeddings, those annotators output at the same level.

        }
        # ' todo output levels for : date? dependencty, labeld dependency? ( depnendcy probably token, sentiment maybe too depending on annoator)

    def get_sample_spark_dataframe(self):
        data = {"text": ['This day sucks', 'I love this day', 'I dont like Sami' ]}
        text_df = pd.DataFrame(data)
        return sparknlp.start().createDataFrame(data=text_df)


    def fit(self, dataset=None):
        if dataset == None:  # todo implement fitting on input datset
            stages = []
            for component in self.pipe_components:
                stages.append(component.model)
            self.is_fitted = True
            self.spark_estimator_pipe = Pipeline(stages=stages)
            self.spark_transformer_pipe = self.spark_estimator_pipe.fit(self.get_sample_spark_dataframe())

    def get_output_level_of_embeddings_provider(self, component_output_column_name, name):
        '''
        This function will go through all components to find the component which  generate @component_output_column_name.
        Then it will goa gain through all components to find the component, from which @component_output_column_name is taking its inputs
        Then it will return the type of the provider component. This result isused to resolve the output level of the component that depends on the inpit for the output level
        :param component_output_column_name:
        :return:
        '''
        # find the component. Column output name should be unique
        component_inputs = []
        for component in self.pipe_components:
            if name == component.component_info.name:
                component_inputs = component.component_info.spark_input_column_names

        # get the embedding feature name
        target_output_component = ''
        for input_name in component_inputs:
            if 'embed' in input_name: target_output_component = input_name

        # get the model that outputs that feature
        for component in self.pipe_components:
            component_outputs = component.component_info.spark_output_column_names
            for input_name in component_outputs:
                if target_output_component == input_name:
                    # this is the component that feeds into the component we are trying to resolve the output  level for.  That is so, because the output of this component matches the input of the component we are resolving
                    return self.resolve_type_to_output_level(component.component_info.type)

    def resolve_type_to_output_level(self, field_type, name):
        '''
        This checks the levels dict for what the output level is for the input annotator type.
        If the annotator type depends on the embedding level, we need further checking.# todo implement
        @ param field_type : type of the spark field
        @ param name : name of thhe spark field
        @ return : String, which corrosponds to the output level of this Component.
        '''
        logger.info('Resolving output level for field_type=%s and field_name=%s', field_type,name)
        if name == 'sentence': return 'sentence'
        if field_type in self.levels['token']: return 'token'
        if field_type in self.levels['sentence']: return 'sentence'
        if field_type in self.levels['chunk']: return 'chunk'
        if field_type in self.levels['document']: return 'document'
        if field_type in self.levels['embedding_level']: return self.get_output_level_of_embeddings_provider(field_type,name)

    def resolve_outputlevel_to_int(self, output_level):
        '''
        @ param field_type : type of the spark field
        @ param name : name of thhe spark field
        This checks the levels dict for what the output level is for the input annotator type.
        If the annotator type depends on the embedding level, we need further checking.# todo implement
        @ return : String, which corrosponds to the output level of this Component.
        '''
        if output_level == 'token' : return 0
        if output_level == 'sentence': return 1
        if output_level == 'chunk': return 2
        if output_level == 'document': return 3
        if output_level == 'language': return 3 # special case

    def resolve_int_outputlevel_to_str(self, output_level):
        '''
        This function maps output int levels back to string
        @ param output_level : Int level output
        @ return : String, which corrosponds to the output level of this Component.
        '''
        logger.info("resolving int output level to str")
        if output_level ==  0  : return 'token'
        if output_level == 1  : return 'sentence'
        if output_level == 2  : return 'chunk'
        if output_level == 3  : return 'document'
        if output_level == 3  : return 'language' # special case


    def get_field_types_dict(self, sdf):
        """
        @ param sdf: Spark Dataframe which a NLU/SparkNLP pipeline has transformed.
        This function returns a dictionary that maps column names to their spark annotator types.
        @return : Dictionary, Keys are spark column column names, value is the type of annotator
        """
        logger.info('Getting field types for output SDF')
        field_types_dict = {}
        for field in sdf.schema.fieldNames():
            if field == self.raw_text_column: continue
            if 'label' in field: continue  # speciel case for input lables
            logger.info('Parsing Output Field =%s', field)
            a_row = sdf.select(field + '.annotatorType').take(1)[0]['annotatorType']
            if len(a_row) > 0:
                a_type = a_row[0]
            else:
                logger.exception('Error there are no rows for this Component in the final Dataframe. For field=%s', field)
                a_type = 'Error'  # (no results)
            field_types_dict[field] = a_type
            logger.info('Parsed type=%s  for field=%s', a_type, field)
        logger.info('Parsing field types done, parsed %s', field_types_dict)
        return field_types_dict

    def make_output_pretty(self, processed, output_level='document', get_different_level_output=True):
        '''
        This functions takes in a spark dataframe with Spark NLP annotations in it and transforms it into a Pandas Dataframe with common feature types for further NLP/NLU downstream tasks.

        :param processed: Spark dataframe which an NLU pipeline has transformed
        :param output_level: The output level at which returned pandas Dataframe should be
        :param get_different_level_output:  Wheter to get features from different levels
        :return: Pandas dataframe which easy accessable features
        '''
        # adding ID lets us map back individual Tokens, Sentsences and Chunks to their original soruces ( usually that would  be a row in the original input dataset )
        # we do double handling because once we handle the cols that need to be exploded. We explode only those cols, which are at the current output level
        # The cols which did not get exploeded will be added manually to the resulting df. --> Problem. Outputs from lower levels will be duplicated at higher levels. For example. if every row is a sentence, every row will include all word embeddings
        logger.info('Pythonyfying SDF outputs..')
        sdf = processed.select(['*', monotonically_increasing_id().alias('id')])  # todo implement optional ID provided by user
        field_dict = self.get_field_types_dict(processed) #map field to type of field
        not_at_same_output_level = []
        positional = False
        all_output_levels_str = []
        all_output_levels_int = []
        # infer output level
        # if not self.user_has_set_output_level : TODO implement next version
        #     # only if user has not set output level we will auto infer at which level to output \
        #     # loop over all columns and find the MIN and MAX output level possible. ( I.E. If there are no tokens, then token output is not possible)
        #     # OR : Look at the last step of the pipeline and infer from that at which level to output.
        #     for k_name in field_dict.keys():
        #         all_output_levels_str.append(self.resolve_type_to_output_level(field_dict[k_name],k_name))
        #         all_output_levels_int.append(self.resolve_outputlevel_to_int(all_output_levels_str[-1]))
        #     logger.info('Detected output levels_str=%s', all_output_levels_str)
        #     logger.info('Detected output levels_int=%s', all_output_levels_int)
        #     self.output_level = self.resolve_outputlevel_to_str(max(all_output_levels_int)) #output heighest, todo make smarter!
        #     logger.info('Auto inferred because user did not set output level to : output_level=%s', self.output_level)

        c_names = [self.output_level + '.result']
        for field in processed.schema.fieldNames():  # loop over all fields.
            if field == self.raw_text_column: continue
            if field == output_level: continue
            if 'label' in field and 'dependency' not in field: continue  # speciel case for input lables

            f_type = field_dict[field]
            # print(f_type)
            if self.resolve_type_to_output_level(f_type, field) == output_level:
                if 'embeddings' not in field: c_names.append(field + '.result')  # result of embeddigns is just the word/sentence
                if self.output_positions:
                    c_names.append(field + '.begin')
                    c_names.append(field + '.end')
                if 'embeddings' in f_type:
                    c_names.append(field + '.embeddings')
            else:
                if 'embeddings' not in field: not_at_same_output_level.append(field + '.result')  # result of embeddigns is just the word/sentence
                if self.output_positions:
                    not_at_same_output_level.append(field + '.begin')
                    not_at_same_output_level.append(field + '.end')
                if 'embeddings' in f_type:
                    not_at_same_output_level.append(field + '.embeddings')

        print('zipping ', c_names)

        ptmp = sdf.withColumn("tmp", arrays_zip(*c_names)).withColumn("res", explode('tmp'))

        # select the results of the explode
        final_select = []
        final_not_at_same_output_level = []
        for i, field in enumerate(c_names):
            print(i, field)
            # if i == len(field) : break
            if self.raw_text_column in field: continue
            # if  'token' in field   : continue
            # ptmp = ptmp.withColumn(field.split('.')[0], ptmp['res.'+str(i)]) # get the outputlevel results row by row
            new_field = field.replace('.', '_')
            ptmp = ptmp.withColumn(new_field, ptmp['res.' + str(i)])  # get the outputlevel results row by row
            final_select.append(new_field)
        # get the non exploded columns
        if get_different_level_output:
            for i, field in enumerate(not_at_same_output_level):
                print(i, field)
                # if i == len(field) : break
                if self.raw_text_column in field: continue
                # if  'token' in field   : continue
                # ptmp = ptmp.withColumn(field.split('.')[0], ptmp['res.'+str(i)]) # get the outputlevel results row by row
                new_field = field.replace('.', '_')
                ptmp = ptmp.withColumn(new_field, ptmp[field])  # get the outputlevel results row by row
                final_not_at_same_output_level.append(new_field)

        final_select.append('id')
        ptmp.toPandas()
        return ptmp.select(final_select + final_not_at_same_output_level).toPandas()

    def predict(self, data, extraction_config={}):
        """ Annotates a Pandas Dataframe or a Numpy Dataframe or a Spark DataFrame or Python List of strings or a Python String"""
        if not self.is_fitted: self.fit()
        sdf = None
        if type(data) is pd.DataFrame:  # casting follows pd->spark->pd
            if self.raw_text_column in data.columns: sdf = self.spark_transformer_pipe.transform(
                self.spark.createDataFrame(data), )

        elif type(
                data) is np.ndarray:  # This is a bit inefficient. Casting follow  np->pd->spark->pd. We could cut out the first pd step
            if len(data.shape) != 1: print("Exception : Input numpy array must be 1 Dimensional. Input data shape is",
                                           data.shape, ' TODO ACTUALLY THROW EXCPETION here')
            sdf = self.spark_transformer_pipe.transform(self.spark.createDataFrame(pd.DataFrame({self.raw_text_column:data}))) # todo pyarrow or internal data embelishment
        elif type(data) is np.matrix: # assumes default axis for raw texts
            print ('Todo np matrix annotate implementation ')
            pass
        elif type(data) is str:  # inefficient, str->pd->spark->pd , we can could first pd
            sdf = self.spark_transformer_pipe.transform(self.spark.createDataFrame(
                pd.DataFrame({self.raw_text_column: data}, index=[0])))  # todo pyarrow or internal data embelishment
        elif type(data) is list:  # inefficient, list->pd->spark->pd , we can could first pd
            if all(type(elem) == str for elem in data):
                sdf = self.spark_transformer_pipe.transform(self.spark.createDataFrame(pd.DataFrame(
                    {self.raw_text_column: pd.Series(data)})))  # todo pyarrow or internal data embelishment
            else:
                print("Exception: Not all elements in input list are of type string.",
                      ' TODO ACTUALLY THROW EXCPETION here')
        elif type(data) is dict():  # Assumes values should be predicted
            print('todo dict string Annotate implementation?')

        # After we have SDF, which contains pipes annotations we apply pipeline finisher to make resulting DF pretty
        return self.make_output_pretty(sdf, self.output_level, self.output_different_levels)
        # if extraction_config == {} : return sdf.toPandas() #todo default prettifying
        # else : return self.finisher.extract_all_features(sdf,extraction_config) # RENAME PREBUILT PIPE!


## todo remove this class and integrade pretraiend pipelines into stackable pipes
class PretrainedPipe(BasePipe):
    def __init__(self, name, lang='en'):
        super().__init__()
        """ Initializes a pretrained pipeline         ## todo check wether this is a sparknlp or some other pipeline """
        self.spark = sparknlp.start()
        self.spark_nlp_pipe = pretrained.PretrainedPipeline(name, lang)
        self.name = name + "_" + lang
        self.provider = 'sparknlp'
        #self.add()  TODO wiggle the models out of the spark NLP pipeline and properly build and add all components

    def predict(self, data, extraction_config = {}):
        """ Annotates a Pandas Dataframe or a Numpy Dataframe or a Spark DataFrame or Python List of strings or a Python String"""

        sdf = None
        if type(data) is pd.DataFrame: # casting follows pd->spark->pd
            if self.raw_text_column in data.columns : sdf =  self.spark_nlp_pipe.annotate(self.spark.createDataFrame(data), column=self.raw_text_column)

        elif type(data) is np.ndarray : # This is a bit inefficient. Casting follow  np->pd->spark->pd. We could cut out the first pd step
            if len(data.shape) != 1 : print("Exception : Input numpy array must be 1 Dimensional. Input data shape is", data.shape, ' TODO ACTUALLY THROW EXCPETION here')
            sdf = self.spark_nlp_pipe.annotate(self.spark.createDataFrame(pd.DataFrame({self.raw_text_column:data})), column=self.raw_text_column) # todo pyarrow or internal data embelishment
        elif type(data) is np.matrix: # assumes default axis for raw texts
            print ('Todo np matrix annotate implementation ')
            pass
        elif type(data) is str:  # inefficient, str->pd->spark->pd , we can could first pd
            sdf = self.spark_nlp_pipe.annotate(
                self.spark.createDataFrame(pd.DataFrame({self.raw_text_column: data}, index=[0])),
                column=self.raw_text_column)  # todo pyarrow or internal data embelishment
        elif type(data) is list:  # inefficient, list->pd->spark->pd , we can could first pd
            if all(type(elem) == str for elem in data):
                sdf = self.spark_nlp_pipe.annotate(
                    self.spark.createDataFrame(pd.DataFrame({self.raw_text_column: pd.Series(data)})),
                    column=self.raw_text_column)  # todo pyarrow or internal data embelishment
            else:
                print("Exception: Not all elements in input list are of type string.",
                      ' TODO ACTUALLY THROW EXCPETION here')
        elif type(data) is dict():  # Assumes values should be predicted
            print('todo dict string Annotate implementation?')

        # After we have SDF, which contains pipes annotations we apply pipeline finisher to make resulting DF pretty
        # if extraction_config == {} : return sdf.toPandas() #todo default prettifying
        # else : return self.finisher.extract_all_features(sdf,extraction_config) # RENAME PREBUILT PIPE!

## TODO this class will handle nlu pipeline building requests
# You pass a list of NLU components to the pipeline (or a NLU pipeline)
# For every component, it checks if all rqeuirements are met.
# It checks and fixes the following issues  for a list of components:
# 1. Missing Features / component requirements
# 2. Bad order of components (which will cause missing features.
# 3. Check Feature naems in the output
# 4. Check wether pipeline needs to be fitted
class PipelineQueryVerifier():
    amount_of_component_priority_levels = 12

    @staticmethod
    def has_embeddings_requirement(component):
        '''
        Check for the input component, wether it depends on some embedding. Returns True if yes, otherwise False.
        :param component:  The component to check
        :return: True if the component needs some specifc embedding (i.e.glove, bert, elmo etc..). Otherwise returns False
        '''

        if type(component) == list or type(component) == set :
            for feature in component:
                if 'embed' in feature : return  True
            return False
        else :
            for feature in component.component_info.inputs:
                if 'embed' in feature : return  True
        return False

    @staticmethod
    def has_embeddings_provisions(component):
        '''
        Check for the input component, wether it depends on some embedding. Returns True if yes, otherwise False.
        :param component:  The component to check
        :return: True if the component needs some specifc embedding (i.e.glove, bert, elmo etc..). Otherwise returns False
        '''
        if type(component) == type(list) or type(component) == type(set):
            for feature in component:
                if 'embed' in feature : return  True
            return False
        else :
            for feature in component.component_info.outputs:
                if 'embed' in feature : return  True
        return False

    @staticmethod
    def clean_irrelevant_features(component_list):
        #remove irrelevant missing features for pretrained models
        if 'text' in component_list: component_list.remove('text')
        if 'raw_text' in component_list: component_list.remove('raw_text')
        if 'raw_texts' in component_list: component_list.remove('raw_texts')
        if 'label' in component_list: component_list.remove('label')
        if 'sentiment_label' in component_list: component_list.remove('sentiment_label')
        return component_list

    @staticmethod
    def get_missing_required_features (pipe:NLUPipeline)  :
        '''
        Takes in a NLUPipeline and returns a list of missing  feature types types which would cause the pipeline to crash if not added
        If it is some kind of model that uses embeddings, it will check the metadata for that model and return a string with moelName@spark_nlp_embedding_reference format
        '''
        logger.info('Resolving missing components')
        pipe_requirements = []
        pipe_provided_features = []
        # pipe_types = [] # list of string identifiers

        for component in pipe.pipe_components:
            # 1. Get all feature provisions from the pipeline
            if not component.component_info.inputs == component.component_info.outputs:
                pipe_provided_features.append(component.component_info.outputs)  # edge case for components that provide token and require token and similar cases.

            # 2. get all feature requirements for pipeline
            if PipelineQueryVerifier.has_embeddings_requirement(component) :
                # special case for models with embedding requirements. we will modify the output string which then will be resolved by the default component resolver (which will get the correct embedding )
                sparknlp_embeddings_requirement_reference = component.model.extractParamMap()[component.model.getParam('storageRef')]
                inputs_with_sparknlp_reference = []
                for feature in component.component_info.inputs:
                    if 'embed' in feature : inputs_with_sparknlp_reference.append(feature + '@' + sparknlp_embeddings_requirement_reference)
                    else : inputs_with_sparknlp_reference.append(feature)
                pipe_requirements.append(inputs_with_sparknlp_reference)
            else : pipe_requirements.append(component.component_info.inputs)
            # pipe_types.append(component.component_info.type)

        # 3. get missing requirements, by substracting provided from requirements
        # Flatten lists, make them to sets and get missing components by substracting them.
        flat_requirements = set(item for sublist in pipe_requirements for item in sublist)
        flat_provisions = set(item for sublist in pipe_provided_features for item in sublist)
        #rmv spark identifier from provision
        flat_requirements_no_ref = set(item.split('@')[0] if '@' in item else item for item in flat_requirements)

        #see what is missing, with identifier removed
        missing_components = PipelineQueryVerifier.clean_irrelevant_features(flat_requirements_no_ref - flat_provisions)
        # since embeds are missing, we add embed with reference back
        if PipelineQueryVerifier.has_embeddings_requirement(missing_components):
            missing_components = PipelineQueryVerifier.clean_irrelevant_features(flat_requirements - flat_provisions)

        if len(missing_components) == 0 :
            logger.info('No more components missing!')
            return []
        else:
            # we must recaclulate the difference, because we reoved the spark nlp reference previously for our set operation. Since it was not 0, we ad the Spark NLP rererence back
            logger.info('Components missing=%s', str(missing_components))
            return missing_components

    @staticmethod
    def check_and_fix_nlu_pipeline(pipe:NLUPipeline):
        # main entry point for Model stacking withouth pretrained pipelines
        # requirements and provided features will be lists of lists
        all_features_provided = False
        while all_features_provided == False :
            # After new components have been added, we must loop agan and check for the new components if requriements are met
            # OR we implement a function caled "Add components with requirements". That one needs to know though, which requirements are already met ...

            # Find missing components
            missing_components = PipelineQueryVerifier.get_missing_required_features(pipe)
            if len(missing_components) == 0: break  # Now all features are provided

            components_to_add = []
            # 3. Create missing components
            for missing_component in missing_components:
                components_to_add.append(nlu.get_default_component_of_type(missing_component))
            logger.info('Resolved for missing components the following NLU components : %s', str(components_to_add))


            # 3. Add missing components and validate order of components is correct
            for new_component in components_to_add:
                pipe.add(new_component)
                logger.info('adding %s=', new_component.component_info.name)


        print('Fixing column names')
        # 4. Validate naming of output columns is correct and no error will be thrown in spark
        pipe = PipelineQueryVerifier.check_and_fix_component_output_column_names(pipe)

        # 3.  fix order
        logger.info('Optimizing pipe component order')

        pipe = PipelineQueryVerifier.check_and_fix_component_order(pipe)
        # 5. Todo Download all file depenencies like train files or  dictionaries
        logger.info('Done with pipe optimizing')

        return pipe

    @staticmethod
    def check_and_fix_component_output_column_names(pipe: NLUPipeline):
        '''
        This function verifies that every input and output column name of a component is satisfied.
        If some output names are missing, it will be added by this methods.
        Usually classifiers need to change their input column name, so that it matches one of the previous embeddings because they have dynamic output names
        :return:
        '''
        # 1. For each component we veryify that all input column names are satisfied  by checking all other components output names
        # 2. When a input column is missing we do the following :
        # 2.1 Figure out the type of the missing input column. The name of the missing column should be equal to the type
        # 2.2 Check if there is already a component in the pipe, which provides this input (It should)
        # 2.3. When the providing component is found, update its output name, or update the original coponents input name
        all_names_provided = False

        for component_to_check in pipe.pipe_components:
            all_names_provided_for_component = False
            input_columns = set(component_to_check.component_info.spark_input_column_names)
            print(component_to_check.component_info.name, input_columns)
            for other_component in pipe.pipe_components:
                if component_to_check.component_info.name == other_component.component_info.name: continue
                output_columns = set(other_component.component_info.spark_output_column_names)
                input_columns -= output_columns  # set substraction

            input_columns = PipelineQueryVerifier.clean_irrelevant_features(input_columns)

            if len(input_columns) != 0:  # fix missing column name
                for missing_column in input_columns:
                    for other_component in pipe.pipe_components:
                        if component_to_check.component_info.name == other_component.component_info.name: continue
                        if other_component.component_info.type == missing_column:
                            # resolve which setter to use ...
                            # We update the output name for the component which provides our feature
                            other_component.component_info.spark_output_column_names = [missing_column]
                            other_component.model.setOutputCol(missing_column)

        return pipe

    @staticmethod
    def component_priority_level_resolver(type):
        # resolves the level of prioirty for a given component name
        if type == 'document_assembler': return 0
        if type == 'tokenizer': return 1
        if type == 'sentence_detector': return 2
        if type == 'word_embeddings': return 3

        return 4

    @staticmethod
    def check_and_fix_component_order_old(pipe: NLUPipeline):
        '''
        This method takes care that the order of components is the correct in such a way,
        that the pipeline can be iteratively processed by spark NLP.
        '''

        # Get all components by order. Inefficent Double Loop. List size will be very small, so it will not be that dramatic., todo optimize
        components_by_priority = {}  # Keys from level 0 to  max_level. Each value is a list of components of that priority level in the current pipe
        for priority_level in range(nlu.PipelineQueryVerifier.amount_of_component_priority_levels + 1):
            if not priority_level in components_by_priority.keys(): components_by_priority[priority_level] = []
            for component in pipe.pipe_components:
                component_priority_level = component.component_info.pipe_priorioty_slot  # nlu.PipelineQueryVerifier.component_priority_level_resolver(component.component_info.type, component.component_info.type)
                if int(component_priority_level) == int(
                        priority_level):  # semi bug under the hood, check typing in json files and info class
                    components_by_priority[priority_level].append(component)

        correct_order_component_pipeline = []
        for priority_level in range(nlu.PipelineQueryVerifier.amount_of_component_priority_levels + 1):
            correct_order_component_pipeline.append(components_by_priority[priority_level])

        # flatten nested list
        correct_order_component_pipeline = [e for esub in correct_order_component_pipeline for e in esub]

        pipe.pipe_components = correct_order_component_pipeline
        return pipe

    @staticmethod
    def check_and_fix_component_order(pipe: NLUPipeline):
        '''
        This method takes care that the order of components is the correct in such a way,
        that the pipeline can be iteratively processed by spark NLP.
        '''
        logger.info("Starting to optimize component order ")
        correct_order_component_pipeline = []
        all_components_orderd = False
        all_components = pipe.pipe_components

        provided_features = []
        while all_components_orderd == False:
            for component in all_components:
                logger.info("Optimizing order for component %s", component.component_info.name)

                if component.component_info.name == 'document_assembler':
                    provided_features.append('document')
                    correct_order_component_pipeline.append(component)
                    all_components.remove(component)

                input_columns = PipelineQueryVerifier.clean_irrelevant_features(component.component_info.inputs)
                if set(input_columns).issubset(provided_features):  #  component not in correct_order_component_pipeline:
                    correct_order_component_pipeline.append(component)
                    if component in all_components : all_components.remove(component) # ??? dirty bugged fixed
                    for feature in component.component_info.outputs: provided_features.append(feature)
            if len(all_components) == 0: all_components_orderd = True

        pipe.pipe_components = correct_order_component_pipeline

        return pipe

