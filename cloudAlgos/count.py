import socket
import message_pb2

def createPatient():
    patient = message_pb2.Patient()
    patient.fname  = "Han"
    patient.lname  = "Solo"
    patient.email  = "hansolo.gmail.com"
    patient.age    = 29
    patient.gender = message_pb2.Patient.MALE
    patient.weight = 80.0
    patient.height = 180
    return patient

def createNumericQuery(comparator, field, value):
    query = message_pb2.Query()
    query.comparator = comparator
    query.field = field
    query.numericValue = value
    return query

def createStringQuery(comparator, field, value):
    query = message_pb2.Query()
    query.comparator = comparator
    query.field = field
    query.stringValue = value
    return query

# COMPARATOR: GT, LT, EQ
# FIELD: age (int) , weight (int), height (int), gender (string)
def countQuery(comparator, field, value):
    if type(value) == "string" and comparator != "EQ":
        print("You can only perform a GT or LT query with a numeric value")
        return

    if field == "age":
        return createNumericQuery(comparator, field, value)
    elif field == "weight":
        return createNumericQuery(comparator, field, value)
    elif field == "height":
        return createNumericQuery(comparator, field, value)
    elif field == "gender":
        return createStringQuery(comparator, field, value)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8000))
    query = countQuery("GT", "age", 81)
    s.sendall(query.SerializeToString())
    s.shutdown(socket.SHUT_WR)
    data = s.recv(1024)
    res = message_pb2.Result()
    res.ParseFromString(data)
    print "This is the count: " + str(res.count)
    s.close()
