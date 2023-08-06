from .tokenizer import jieba_segment as segment
from difflib import SequenceMatcher


class Comparator:
    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    @staticmethod
    def _cut_statement(statement):
        return segment.cut(statement, seg_only=True)

    def compare(self, statement_a, statement_b):
        return 0


class LevenshteinDistance(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement.
    """

    def compare(self, statement, other_statement):
        """
        Compare the two input statements.

        :return float: The percent of similarity between the text of the statements.
        """

        # Return 0 if either statement has a falsy text value
        if not statement or not other_statement:
            return 0

        similarity = SequenceMatcher(
            None,
            statement,
            other_statement
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent


# class BM25Distance(Comparator):
#     """
#     Compare the similarity of two sentences using the bm25 algorithm
#
#     :return float: The percent of similarity between the text of the statements.
#     """
#
#     def compare(self, statement, other_statement):
#         # Return 0 if either statement has a falsy text value
#         if not statement or not other_statement:
#             return 0
#
#         # Calculate a decimal percent of the similarity
#         statement_token = self._cut_statement(statement)
#         other_statement_token = self._cut_statement(other_statement)
#         s = SnowNLP(statement_token)
#         percent = s.sim(other_statement_token)
#
#         return percent


# class VectorDistance(Comparator):
#     """
#     Calculate the similarity of two statements.
#     """
#     def __init__(self, **kwargs):
#         # logger
#         self.logger = kwargs.get('logger', logger)
#         app_id = '16082031'
#         api_key = 'iNCC8w5mI63I7eYh0Y1t4Spv'
#         secret_key = 'rjOM3cERogv4RqDEux0n8nbLBItOP7iF'
#
#         self._baidu_client = AipNlp(app_id, api_key, secret_key)
#
#     def _get_word_vector(self, word):
#         response = self._baidu_client.wordEmbedding(word)
#         if not response.get('vec'):
#             self.logger.debug('dictionary does not have this word "{}"'.format(word))
#         return response.get('vec', [0])
#
#     def _get_statement_vector(self, statement):
#         statement_vector = []
#         print(self._cut_statement(statement))
#         for word in self._cut_statement(statement):
#             word_vector = self._get_word_vector(word)
#             if word_vector != [0]:
#                 statement_vector.append(word_vector)
#
#         return statement_vector if statement_vector else [[0]]
#
#     def compare(self, statement, other_statement):
#         """
#         Compare the two input statements.
#
#         :return: The percent of similarity between the vector distance.
#         :rtype: float
#         """
#         # Return 0 if either statement has a falsy text value
#         if not statement or not other_statement:
#             return 0
#
#         statement_vector = self._get_statement_vector(statement)
#         other_statement_vector = self._get_statement_vector(other_statement)
#         return dot(matutils.unitvec(array(statement_vector).mean(axis=0)),
#                    matutils.unitvec(array(other_statement_vector).mean(axis=0)))


levenshtein_distance = LevenshteinDistance()
# vector_distance = VectorDistance()
