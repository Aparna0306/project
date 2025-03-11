import socket
from pyasn1.type import univ, namedtype, constraint
from pyasn1.codec.der import encoder

# Define the BSM message (same as before)
class Uint8(univ.Integer):
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 255)

class Position(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('latitude', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(-900000000, 900000000))),
        namedtype.NamedType('longitude', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(-1800000000, 1800000000))),
        namedtype.NamedType('elevation', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(-1000, 10000)))
    )

class VehicleInformation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('speed', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 255))),
        namedtype.NamedType('heading', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 360))),
        namedtype.NamedType('direction', univ.Boolean())
    )

class BasicSafetyMessage(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('protocolVersion', Uint8()),
        namedtype.NamedType('position', Position()),
        namedtype.NamedType('vehicleInfo', VehicleInformation())
    )

# Create and populate the BSM message
bsm = BasicSafetyMessage()

bsm.setComponentByName('protocolVersion', 1)
position = Position()
position.setComponentByName('latitude', 37256000)
position.setComponentByName('longitude', -122419400)
position.setComponentByName('elevation', 30)

vehicle_info = VehicleInformation()
vehicle_info.setComponentByName('speed', 80)
vehicle_info.setComponentByName('heading', 90)
vehicle_info.setComponentByName('direction', True)

bsm.setComponentByName('position', position)
bsm.setComponentByName('vehicleInfo', vehicle_info)

# Encode the BSM message to DER format
encoded_bsm = encoder.encode(bsm)

# Send the encoded data over TCP
def send_data(host='localhost', port=65432, data=encoded_bsm):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    try:
        # Send the binary data over TCP
        client_socket.sendall(data)
        print(f"Sent data: {data}")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == '__main__':
    send_data(data=encoded_bsm)

