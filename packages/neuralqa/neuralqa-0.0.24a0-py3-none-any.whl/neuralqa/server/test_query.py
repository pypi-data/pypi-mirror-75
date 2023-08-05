# # temporary file for testing search abstractions
# # TODO: Delete this file!!

# from elasticsearch import Elasticsearch, ConnectionError

# es = Elasticsearch([{'host': "localhost", 'port': 9200}])

# def parse_field_content(field_name, content):
#     """Parse content fields if nested using dot notation, else return content as is.
#     e.g. for acrray content and field_name casebody.data.opinions.text, we return
#     content[casebody][data][opinions][text]. If any nest level is an array we return only the
#     first instance of this array. e.g. if opinions is an array, we return
#     content[casebody][data][opinions][0][text].

#     Args:
#         field_name ([str]): [description]
#         content ([dict]): [description]

#     Returns:
#         [str]: content of field
#     """

#     if ("." not in field_name):
#         return content[field_name]
#     else:
#         fields = field_name.split(".")
#         for field in fields:
#             print("\t",content.keys(), field)
#             content =  content[field]
#             if (isinstance(content, list)):
#                 content = content[0]
#         return content

# def run_query(index_name, search_query, body_field, secondary_fields, max_documents=5, highlight_span=100, relsnip=True, num_fragments=5):

#     tags = {"pre_tags": [""], "post_tags": [""]}
#     highlight_params = {
#         "fragment_size": highlight_span,
#         "fields": {
#             body_field: tags
#         },
#         "number_of_fragments": num_fragments,
#         # "order": "score"
#     }

#     search_query = {
#         "query": {
#             "multi_match": {
#                 "query":    search_query,
#                 "fields": [body_field]
#             }
#         },
#         "_source": {"includes": [body_field]},
#         "size": max_documents
#     }

#     status = True
#     results = {}

#     if (relsnip):
#         search_query["highlight"] = highlight_params
#     # else:
#     #     search_query["_source"] = {"includes": [body_field]}

#     try:
#         # print(search_query)
#         query_result = es.search(index=index_name, body=search_query)
#         # RelSnip: for each document, we concatenate all
#         # fragments in each document and return as the document.

#         highlights = [" *** ".join(hit["highlight"][body_field])
#                         for hit in query_result["hits"]["hits"] if "highlight" in hit]
#         docs = [parse_field_content(body_field, hit["_source"])
#                 for hit in query_result["hits"]["hits"] if hit["_source"]]
#         took = query_result["took"]
#         results = {"took": took,  "highlight": highlights, "docs": docs}

#     except (ConnectionRefusedError, Exception) as e:
#         status = False
#         results["errormsg"] = str(e)

#     results["status"] = status
#     return results


# search_query = "what arson"
# max_documents = 2
# highlight_span = 50
# body_field = "casebody.data.opinions.text"
# secondary_fields = ["author"]
# num_fragments = 2

# results = run_query("cases", search_query, body_field, secondary_fields,
#                     max_documents=5, highlight_span=highlight_span, relsnip=True, num_fragments=num_fragments)
# print(results)
import logging
from neuralqa.expander import MLMExpander

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
# logging.getLogger("root").setLevel(logging.INFO)

expander = MLMExpander()
expanded_query = expander.expand_query(
    "what is the goal of the fourth amendment?  ")
terms = " ".join([term["token"] for term in expanded_query["terms"]])
print(expanded_query)
