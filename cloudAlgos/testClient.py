import socket
import patient_pb2

def createPatient():
    patient = patient_pb2.Patient()
    patient.fname  = "Han"
    patient.lname  = "Solo"
    patient.email  = "hansolo.gmail.com"
    patient.age    = 29
    patient.gender = patient_pb2.Patient.MALE
    patient.weight = 80.0
    patient.height = 180
    return patient


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8001))
    patient = createPatient()
    s.sendall(patient.SerializeToString())
    data = s.recv(1024)
    print "This is the response: " + repr(data)
    s.close()