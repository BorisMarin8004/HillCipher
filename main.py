from math import sqrt, ceil
import numpy as np
import sympy as sy


class HillCipher:
    NUMBER_MAP = {
        " ": 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
        "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
        "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26, "0": 27, "1": 28, "2": 29,
        "3": 30, "4": 31, "5": 32, "6": 33, "7": 34, "8": 35, "9": 36, ".": 37, "?": 38, ",": 39,
        "-": 40
    }
    REV_NUMBER_MAP = {v: k for k, v in NUMBER_MAP.items()}

    def __init__(self, key: str):
        side = ceil(sqrt(len(key)))
        self.key = HillCipher.__get_number_matrix(
            lambda i: HillCipher.NUMBER_MAP.get(key[i]) if i < len(key) else i - len(key) + 1,
            (side, side))
        det = np.linalg.det(self.key) % len(HillCipher.NUMBER_MAP)
        key_adj = np.array(sy.Matrix(self.key).adjugate() % len(HillCipher.NUMBER_MAP))
        det_multi_inv = pow(int(det), -1, len(HillCipher.NUMBER_MAP))
        self.inv_key = (key_adj * det_multi_inv) % len(HillCipher.NUMBER_MAP)

    @staticmethod
    def __get_number_matrix(convert_func, dims: tuple) -> np.ndarray:
        return np.array(
            [convert_func(i) for i in range(np.prod(np.array(dims)))]
        ).reshape(*dims)

    @staticmethod
    def __get_string(matrix: np.ndarray) -> str:
        convert = np.vectorize(lambda val: HillCipher.REV_NUMBER_MAP.get(val))
        return "".join(np.concatenate(convert(matrix)))

    @staticmethod
    def __apply_key(msg, key):
        side = ceil(len(msg) / len(key))
        print("MSG:", msg)
        msg_number_matrix = HillCipher.__get_number_matrix(
            lambda i: HillCipher.NUMBER_MAP.get(msg[i]) if i < len(msg) else 0,
            (len(key), side))
        print("MSG_NUMBER_MATRIX:\n", msg_number_matrix)
        print("DOT:\n", np.dot(key, msg_number_matrix))
        msg_number_encrypt = np.dot(key, msg_number_matrix) % len(HillCipher.NUMBER_MAP)
        print("MSG_NUMBER_ENCRYPT:\n", msg_number_encrypt)
        return HillCipher.__get_string(msg_number_encrypt)

    def encrypt(self, msg):
        print("\n-----\nEncrypt:")
        return HillCipher.__apply_key(msg, self.key)

    def decrypt(self, msg):
        print("\n-----\nDecrypt:")
        return HillCipher.__apply_key(msg, self.inv_key)


def main(*args, **kwargs):
    h_cip = HillCipher("LINEAR")

    print("KEY:\n", h_cip.key)
    print("INV_KEY:\n", h_cip.inv_key)

    enc_msg = h_cip.encrypt("BORIS MARIN")
    print(h_cip.decrypt(enc_msg))


if __name__ == '__main__':
    main()

