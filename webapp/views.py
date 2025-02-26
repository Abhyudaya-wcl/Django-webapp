from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import json
import os
import ssl
import re
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage
from promptflow.core import Flow
def home(request):
    return render(request, 'home.html')

PROMPTFLOW_PATH = "D:\Repos\HR-Prompt-Flow\HR Bot Draft - 4\\flow.dag.yaml"


def response(request):
    output_text = None

    if request.method == "POST":
        request_data = json.loads(request.body)
        user_input = request_data.get("message", "")

        if user_input:
            try:
                flow = Flow.load(source=PROMPTFLOW_PATH)
                result = flow(query=user_input)
                # result = {"reply": ["test [doc0]"], "documents": [{"0": "document 0 content"}]} #for testing. remove when flow is implemented.

                if isinstance(result, dict):
                    reply_generator = result.get("reply")
                    documents = result.get("documents", [])

                    if reply_generator:
                        output_text = "".join(reply_generator)
                    else:
                        output_text = "Reply generator was empty."

                    response_data = {"response": output_text, "documents": documents}
                    reply = response_data.get('response', '') #changed to response
                    documents_list = response_data.get('documents', []) #get the whole list.
                    # print("doclist", documents_list)
                    if documents_list and isinstance(documents_list, list) and len(documents_list) > 0: #Check if documents is a list, and not empty.
                         #access the first document.
                        # print("doc", documents)
                        doc_refs = re.findall(r'\[doc(\d+)\]', reply)
                        if doc_refs:
                            for doc_num_str in doc_refs:
                                doc_num = int(doc_num_str)
                                doc_text = documents_list[(doc_num-1)]["content"]
                                escaped_doc_text = doc_text.replace("'", "\\'")
                                reply = reply.replace(
                                    f'[doc{doc_num}]',
                                    f'<button onclick="showDocument(\'{doc_num}\', \'{escaped_doc_text}\')">Document {doc_num}</button>'
                                )
                            response_data['response'] = reply #changed to response
                    return JsonResponse(response_data)

                else:
                    return JsonResponse({"response": "Unexpected result type from Prompt Flow."})

            except Exception as e:
                return JsonResponse({"response": f"Error: {str(e)}"})
    return JsonResponse({"response": "Invalid request"})
