
def paginate(query_result, page=1):

    
    return [query_result[i:i+10] for i in range(0, len(query_result), 10)][page-1]

