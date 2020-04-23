import time

import rsa
from phe import paillier


def test_rsa(data):
    print('===================================')
    # print('rsa - data:', data)
    # print('rsa - data_length:', len(data))
    rsa_public_key, rsa_secret_key = rsa.newkeys(nbits=1024)  # 初始化rsa公钥，私钥
    data = [str(x) for x in data]
    data = [x.encode('utf-8') for x in data]

    begin_time = time.clock()
    encrypt_data = [rsa.encrypt(x, rsa_public_key) for x in data]
    end_time = time.clock()
    encrypt_time = (end_time - begin_time)

    begin_time = time.clock()
    decrypt_data = [rsa.decrypt(x, rsa_secret_key) for x in encrypt_data]
    end_time = time.clock()
    decrypt_data = [x.decode('utf-8') for x in decrypt_data]
    decrypt_data = [int(x) for x in decrypt_data]
    decrypt_time = (end_time - begin_time)
    total_time = encrypt_time + decrypt_time

    print('rsa - encrypt_time:', encrypt_time)
    print('rsa - decrypt_time:', decrypt_time)
    print('rsa - encrypt_time / decrypt_time:', encrypt_time / decrypt_time)
    print('rsa - encrypt_time / total_time:', encrypt_time / total_time)
    print('rsa - decrypt_time / total_time:', decrypt_time / total_time)
    # print('rsa - decrypt_data:', decrypt_data)
    return total_time


def test_pailler(data):
    print('===================================')
    # print('paillier - data:', data)
    # print('pailler - data_length:', len(data))
    paillier_public_key, paillier_private_key = paillier.generate_paillier_keypair(
        n_length=1024)  # 初始化paillier公钥，私钥    begin_time = time.clock()
    begin_time = time.clock()
    encrypt_data = [paillier_public_key.encrypt(x) for x in data]
    end_time = time.clock()
    encrypt_time = (end_time - begin_time)
    begin_time = time.clock()
    decrypt_data = [paillier_private_key.decrypt(x) for x in encrypt_data]
    end_time = time.clock()
    decrypt_time = (end_time - begin_time)
    total_time = encrypt_time + decrypt_time
    print('pailler - encrypt_time:', encrypt_time)
    print('paillier - decrypt_time:', decrypt_time)
    print('pailler - encrypt_time / decrypt_time:', encrypt_time / decrypt_time)
    print('pailler - encrypt_time / total_time:', encrypt_time / total_time)
    print('pailler - decrypt_time / total_time:', decrypt_time / total_time)
    # print('paillier - decrypt_data:', decrypt_data)
    return total_time


data = [item for item in range(0, 5000)]
rsa_total_time = test_rsa(data)
paillier_total_time = test_pailler(data)
print('rsa_total_time', rsa_total_time)
print('paillier_total_time', paillier_total_time)
print('rsa_total_time/paillier_total_time', rsa_total_time / paillier_total_time)
