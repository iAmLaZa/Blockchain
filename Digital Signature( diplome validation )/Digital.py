import hashlib
import rsa
#pip intall rsa


def createsignature(message, pubkey, prikey):
    crypto=rsa.encrypt(message, pubkey)
    return (crypto)


def decryptsignature(message ,pubkey, prikey):
    message = rsa.decrypt(message,prikey)
    print(message.decode())

def hashfiles(path):
    with open(path, 'rb') as opened_file:
        content = opened_file.read()
        sha256= hashlib.sha256()
        sha256.update(content)
        print('{}: {}'.format(sha256.name, sha256.hexdigest()))
        texttt=(sha256.hexdigest())
        return (texttt)

if __name__ == '__main__':
    (pubkey,privkey)=rsa.newkeys(1024)
    print(type(pubkey))
    print(type(privkey))

    #creating hash for file
    print('the hash of file is: ')
    path = r'./fichierpdf.pdf'
    hashedfile=hashfiles(path)
    cryptedhash = str.encode(hashedfile)


    #crypthash
    messg=createsignature(cryptedhash, pubkey, privkey)
    print('the signature is :')
    print(messg)

    #decrypt signature
    print('the original message is :')
    decryptsignature(messg,pubkey,privkey)