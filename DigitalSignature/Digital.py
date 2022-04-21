import hashlib
import rsa
from CreateDiploma import *
#pip intall rsa
#pip install flask-mysqldb
#pip install pyqt5-tools
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
    # print(type(pubkey))
    # print(type(privkey))
    #creaing the file
    CreateDiplomat(['Wail', 'Alouane', '20', 'Boumerdes', 'SSI', 'USTHB'])
    #creating hash for file
    print('the hash of file1 is: ')
    path = r'Wail_Alouane_file.pdf'
    hashedfile=hashfiles(path)
    cryptedhash = str.encode(hashedfile)



    #crypthash
    messg=createsignature(cryptedhash, pubkey, privkey)
    # print('the signature is :')
    # print(messg)

    #decrypt signature
    # print('the original message is :')
    # decryptsignature(messg,pubkey,privkey)

    # fenetreA():
    # get matricule
    # etudiant recherche par matricule ()
    # genere certificat(data etudiant) DONE
    # hashé et signi certificat   DONE
    # passe data lokman pour cree le block ...
    # ajouter le block ...
    #
    #
    # fenetreB():
    # get pdf
    # hash pdf
    # cherche dans blockchain sur le hash
    # verifie la transaction
    # valider le pdf 
    # afficher le resultat de validation
    #






