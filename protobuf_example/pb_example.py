from protobuf_example.proto import address_book_pb2

if __name__ == '__main__':
    person1 = address_book_pb2.Person()
    person1.id = 1
    person1.name = "Mikasa"
    person1.email = "mikasa@gmail.com"

    phone11 = person1.phones.add()
    phone11.number = "021-12345678"
    phone11.type = address_book_pb2.Person.HOME

    phone12 = person1.phones.add()
    phone12.number = "13888888888"
    phone12.type = address_book_pb2.Person.MOBILE

    person2 = address_book_pb2.Person()
    person2.id = 1
    person2.name = "Historia"
    person2.email = "historia@example.com"

    phone21 = person2.phones.add()
    phone21.number = "021-88888888"
    phone21.type = address_book_pb2.Person.HOME

    phone22 = person2.phones.add()
    phone22.number = "13812345678"
    phone22.type = address_book_pb2.Person.MOBILE

    address_book = address_book_pb2.AddressBook()
    address_book.people.extend([person1, person2])

    print(address_book)

    serialized_data = address_book.SerializeToString()
    print(serialized_data)

    address_book_new = address_book_pb2.AddressBook()
    address_book_new.ParseFromString(serialized_data)
    print(address_book_new)
