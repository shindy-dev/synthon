from client import MyClient

if __name__ == "__main__":
    client = MyClient(("localhost", 22222))
    print(client.request_hello())
    with open("hoge.txt", mode="w") as f:
        f.write("test")
    client.request_sendfile(path="hoge.txt")
