import grpc

import message_pb2
import message_pb2_grpc

def create_patient():
    patient = message_pb2.Patient()
    patient.fname  = "Han"
    patient.lname  = "Solo"
    patient.email  = "hansolo.gmail.com"
    patient.age    = 29
    patient.gender = message_pb2.Patient.MALE
    patient.weight = 80.0
    patient.height = 180
    return patient

# Helper to create a query with a numeric value when given a
# operator
#
# operator: String with GT, LT, or EQ values
# field:    The field the comparison should be applied to.
#           For example, age, weight or height.
# value:    The value that should be used in the comparison.
#           For example, in 'age GT 81', 81 is the value
def create_numeric_query_helper(operator, field, value):
    query = message_pb2.Query()
    query.operator = operator
    query.field = field
    query.numeric_value = value
    return query

# Helper to create a query with a string value when given a
# operator
#
# operator: String with EQ value
# field:    The field the comparison should be applied to.
#           In this case, gender.
# value:    The value that should be used in the comparison.
#           For example, in 'gender EQ male', male is the value
def create_string_query_helper(operator, field, value):
    query = message_pb2.Query()
    query.operator = operator
    query.field = field
    query.stringValue = value
    return query

# Creates a query using the protobuf definition. For example,
# a query with operator="EQ", field="age", value=19 will re-
# turn the number of patients that are 19.
#
# operator: The comparison to be performed on a value. This
#           comparison may be EQ (equal to), LT (less than),
#           or GT (greater than).
# field:    The field that will be compared to a value. These
#           fields may be age, weight, height, gender etc.
# value:    The value that will be compared to the value of
#           vield using the operator.
def create_count_query(operator, field, value):
    if type(value) == "string" and operator != "EQ":
        print("You can only perform a GT or LT query with a numeric value")
        return

    if field == "age":
        return create_numeric_query_helper(operator, field, value)
    elif field == "weight":
        return create_numeric_query_helper(operator, field, value)
    elif field == "height":
        return create_numeric_query_helper(operator, field, value)
    elif field == "gender":
        return create_string_query_helper(operator, field, value)

# Returns a request containing a query and the algorithm id.
# This request is passed to the coordinator and will be used
# to return a response.
#
# query: The query that the request will slap a header on
def create_request(q):
    req = message_pb2.ComputeRequest()
    req.algo_id = 0
    req.query.operator = q.operator
    req.query.field = q.field
    req.query.numeric_value = q.numeric_value
    return req

# Makes an RPC call to the coordinator with the given query
# and returns the count from each site.
#
# stub:  Stub for the cloud coordinator
# query: Query to be performed in local sites
def count(stub, query):
    req = create_request(query)
    result = stub.AlgoRequest(req)
    if not result.responses:
        print("Count failed")
    total = 0
    for i in result.responses:
        total += i.response
    print(total)
    return total


if __name__ == "__main__":
    # Sets up the connection so that we can make RPC calls
    with grpc.insecure_channel('127.0.0.1:50000') as channel:
        stub = message_pb2_grpc.CloudCoordinatorStub(channel)
        print("Counting number of patients with age above 81")
        query = create_count_query("GT", "age", 81)
        count(stub, query)

