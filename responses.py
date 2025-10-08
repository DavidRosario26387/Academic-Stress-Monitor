from RAG import rag_query
from analyse import predict,categorize
import json

def parse_llm_response(llm_response):
    try:
        result = json.loads(llm_response)
        # Ensure both keys exist
        if "message" in result and "reason" in result:
            return result
        else:
            return None
    except (json.JSONDecodeError, TypeError):
        return None
    
def get_response(user_message,llm_obj):
    lowered=user_message.lower()
    l,score=predict(lowered)
    parsed_response=None
    label="Not Stressed"
    category=None
    if l==1:
        label="Stressed"
        category=categorize(score)
        rag_data=rag_query(text=f"{category} Stress, {lowered}",n=2)
        print(rag_data)
        llm_response=llm_obj.infer(lowered,category,rag_data)

        parsed_response = parse_llm_response(llm_response)


    return parsed_response,label,category,score