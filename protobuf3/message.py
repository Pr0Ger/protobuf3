from functools import reduce


class Message(object):
    def __init__(self):
        pass

    @staticmethod
    def _decode_varint(input_iterator):
        result = []
        while True:
            next_byte = next(input_iterator)
            result.append(next_byte & 0b01111111)
            if not next_byte & (1 << 7):
                return reduce(lambda a, b: a + b,
                              map(lambda a, b: a * b,
                                  result,
                                  [(1 << 7) ** i for i in range(len(result))]
                              )
                )
