'''# This file contains all the column names that we would expect when handling a Dataframe returned by a Spark-NLP pipeline
# It is being used to identify

# Spark NLP Selector Values :
Selectable Colums
Position(thats begin and end), metaData, embeddings



# Meta Data Json Descriptor

# Language  identifiers
english = en
german = ger
russian = rus
...

# Output column identifiers

# Description






'''
from pyspark.sql.functions import flatten, explode, map_values, arrays_zip
import pyspark
class Feature():
    ''' this is the base class which is inherited by Feature Columns.
        It is used to represent meta data about features are outputted and also required by a specific component
        A component may output and require multiple Featurse.
        Each specific feature class implementation should provide functions that operate on the output of a component and return a PANDAS series or dataframe
        A feature implementation should load be able to load information about the columns of a component from a component_infos.json file
        Feature Object define the main mechanism to turn Component outputs into Pandas objects and provides a facet of different configurable outputs.

        Spark-NLP Feature classes expect a Pyspark DF to operate on
        '''
    def __init__(self):
        self.has_embeddings = False
        self.is_positional = False # has begin and end
        self.has_token_level_output = False # If this is true, this means explode will result in multiple rows. Such columns should be exploded for Token level output
        self.has_sentence_level_output = False
        self.has_chunk_level_output = False
        self.has_document_level_output = False
        self.has_many_output_columns_mode = False  # If enabled then instead of returning lists when multiple entities occur, the resulting dataframe has many columns, one for each entity and its location and metadata.

    def info(self): pass
    def created_by_components(self): pass # iterate over all info.json and output the componenets which output this feature
    def required_by_components(self): pass # iterate over all info.json and output the componenets which require this feature
    def verify_output_config_is_valid(self, config): pass # verify that output config is valid for this feature

class Entity_Feature(Feature): # This should actually inherit from some Spark_nlp base classs!
    '''This class handelns the entity column which is outputted by explain ML pipelines from Spark-NLP pretraiend pipeline componenets,


    - Token Level output : For every entity found in an input string(Document/Sentence), a new row will be created. One to many mapping
    - Sentence Level output: For all entity found in an input sentence, one row will be outputted. The output row contains a list with 0 to N entities in the document found.  One to one.
    - Chunk Level output: For all entity found in an input Chunk, one row will be outputted. The output row contains a list with 0 to N entities in the document found.  One to one.
    - Document Level output: For all entity found in an input Document, one row will be outputted . The output row contains a list with 0 to N entities in the document found.. One to one.
    - Positional output : If token level output is specified, then the resulting dataframe will have a entity_position column, which indicated the psotion of the entity. Otherwise, the entity_position column will have a list of tuples, unless "MANY_COLUMNS" output mode is specified.

    - MANY COLUMNS OUTPUT MODE (to be implemented) : When many columns is enabled, then every entity found in a sentence will be at a numberd column position, ex: entity_1, entity_2, etc... The positions of these entities will be specified in entity_1_start, entity_2_start, and entity_1_end, entity_2_end. Analgous for entity_1_metadata

    '''
    def __init__(self):
        super().__init__()
        self.is_positional=True
        self.spark_nlp_annotator_type = 'chunk'
        self.has_sentence_level_output = True
        self.has_chunk_level_output = True
        self.has_document_level_output = True
        self.has_embeddings = True # It DOES have them in Spark-NLP but they seem useless


    def token_level_output(self, sdf : pyspark.sql.dataframe.DataFrame, output_positions = False ):
        ## WATCH OUT WITH OVERWRITING THIS VARIABLE!!! If it is call by reference it could cause naughty bugs. It could be done for memory optimization bt should be tested first how the references exactly behave .. Instead of using ptmp, we could just overwrite sdf variable

        if output_positions :
            ptmp = sdf.withColumn("tmp", arrays_zip("entities.result", "entities.begin", "entities.end", "entities.metadata")).withColumn("res", explode('tmp')) \
                .select(["text", "res.0", "res.1","res.2",map_values ("res.3")  ]) \
                .withColumnRenamed('0','entity', ).withColumnRenamed('1','entity_beginning').withColumnRenamed('2','entity_end' ).withColumnRenamed('map_values(res.3)','entity_type' )
            ptmp = sdf.select('entity', 'entity_beginning', 'entity_end',ptmp.entity_type[0],ptmp.entity_type[1],ptmp.entity_type[2]) \
                .withColumnRenamed('entity_type[0]', 'entity_label').withColumnRenamed('entity_type[1]', 'entity_sentence_pos').withColumnRenamed('entity_type[2]', 'entity_chunk_pos')
        else :
            ptmp = sdf.withColumn("tmp", arrays_zip("entities.result", "entities.metadata")).withColumn("res", explode('tmp')) \
                .select(["text", "res.0",map_values ("res.1")  ]).withColumnRenamed('0','entity', ).withColumnRenamed('map_values(res.1)','entity_type' )#.show()
            ptmp = ptmp.select('text','entity', ptmp.entity_type[0]) \
                .withColumnRenamed('entity_type[0]', 'entity_label')

        print('debug')
        return ptmp

    def row_level_output(self, sdf : pyspark.sql.dataframe.DataFrame, output_positions = False ):
        '''One to one mapping of rows. TODO List of Maps handing / Dict handling'''
        ## WATCH OUT WITH OVERWRITING THIS VARIABLE!!! If it is call by reference it could cause naughty bugs. It could be done for memory optimization bt should be tested first how the references exactly behave .. Instead of using ptmp, we could just overwrite sdf variable

        if output_positions :
            print('pos')
            ptmp = sdf.select('text','entities.metadata', 'entities.result', 'entities.begin','entities.end' ) \
                .withColumnRenamed('metadata', 'entity_info' ) \
                .withColumnRenamed('result', 'entities' ) \
                .withColumnRenamed('begin', 'entities_start' ) \
                .withColumnRenamed('end', 'entities_end' )
        else :
            print(' not pos')

            ptmp = sdf.select('text','entities.metadata', 'entities.result') \
                .withColumnRenamed('metadata', 'entity_info' ) \
                .withColumnRenamed('result', 'entities' ) \
                .withColumnRenamed('begin', 'entities_start' ) \
                .withColumnRenamed('end', 'entities_end' )

        print('tmp')
        return ptmp



class Sentiment_Feature(Feature): # This should actually inherit from some Spark_nlp base classs! # todo
    '''This class handelns the entity column which is outputted by explain ML pipelines from Spark-NLP pretraiend pipeline componenets,
    - Token Level output : For every entity found in an input string(Document/Sentence), a new row will be created. One to many mapping
    - Sentence Level output: For all entity found in an input sentence, one row will be outputted. The output row contains a list with 0 to N entities in the document found.  One to one.
    - Chunk Level output: For all entity found in an input Chunk, one row will be outputted. The output row contains a list with 0 to N entities in the document found.  One to one.
    - Document Level output: For all entity found in an input Document, one row will be outputted . The output row contains a list with 0 to N entities in the document found.. One to one.
    - Positional output : If token level output is specified, then the resulting dataframe will have a entity_position column, which indicated the psotion of the entity. Otherwise, the entity_position column will have a list of tuples, unless "MANY_COLUMNS" output mode is specified.
    - MANY COLUMNS OUTPUT MODE : When many columns is enabled, then every entity found in a sentence will be at a numberd column position, ex: entity_1, entity_2, etc... The positions of these entities will be specified in entity_1_start, entity_2_start, and entity_1_end, entity_2_end. Analgous for entity_1_metadata

    '''
    def __init__(self):
        super().__init__()
        self.is_positional=True
        self.spark_nlp_annotator_type = 'chunk'
        self.has_sentence_level_output = True
        self.has_chunk_level_output = True
        self.has_document_level_output = True
        self.has_embeddings = True # It DOES have them in Spark-NLP but they seem useless


    def token_level_output(self, sdf : pyspark.sql.dataframe.DataFrame, output_positions = False ):
        ## WATCH OUT WITH OVERWRITING THIS VARIABLE!!! If it is call by reference it could cause naughty bugs. It could be done for memory optimization bt should be tested first how the references exactly behave .. Instead of using ptmp, we could just overwrite sdf variable
        pass

    def accumulate_sentiment_row_level(self): pass # Since Sentiment is a list of sentiments for each sentence/chunk, having a sentiment for the complete row is helpful