import zmq

def main():
    """ main method """

    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:5563")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A0")
    #subscriber.setsockopt(zmq.SUBSCRIBE, b"A1")
    for i in range(20):
        # Read envelope with address
        [address, A1, A2, A3, A4] = subscriber.recv_multipart()
        print("[%s] %s %s %s %s" % (address,  A1, A2, A3, A4))

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()