# import socket
#
# sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# sock.connect(('127.0.0.1', 5000))
#
# while True:
#     input_str: str = input('input a string:')
#     if input_str == 'quit':
#         sock.close()
#         break
#     sock.send(input_str.encode())
#     response: bytes = sock.recv(1024)
#     print(f'response data :{response.decode()}')

########################################################################################################################################################################################################


# import socket
#
# sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# sock.bind(('127.0.0.1', 5000))
# sock.listen(5)
#
# while True:
#     print('waiting connect...')
#     sck, addr = sock.accept()
#     print(f'socket:{sck}', f'address:{addr}', sep='\n')
#
#     while True:
#         rev_data: bytes = sck.recv(1024)
#         rev_str: str = rev_data.decode()
#         print(f'receive data:{rev_str}')
#
#         if rev_str == 'quit' or len(rev_data) == 0:
#             print(f'quit from client: {sck}')
#             break
#
#         response: str = rev_str.upper()
#         sck.send(response.encode())
