# pip install pypdf2  
from hashlib import sha256
import PyPDF2

def updatehash(*args):
    hashing_text = ""; h = sha256()

    #loop through each argument and hash
    for arg in args:
        hashing_text += str(arg)
        

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

def readPDF(filename):
    # creating a pdf file object
    pdfFileObj = open(filename, 'rb')
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # creating a page object
    pageObj = pdfReader.getPage(0)
    certif=pageObj.extractText()
    # closing the pdf file object
    pdfFileObj.close()
    return certif.encode('utf-8')
 

    
class Block():

   
    def __init__(self,number=0, previous_hash="0"*64, data=None, nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce
        )

    
    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce
            )
        )



class Blockchain():
    #the number of zeros in front of each hash
    difficulty = 4

    
    def __init__(self):
        self.chain = []

    
    def add(self, block):
        self.chain.append(block)

    
    def remove(self, block):
        self.chain.remove(block)

    
    def mine(self, block):
        try: block.previous_hash = self.chain[-1].hash()
        except IndexError: pass
        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                block.nonce += 1
    def isValid(self):
        for i in range(1,len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True


#for testing purposes
def main():
    blockchain = Blockchain()
    
    lokcertif='C:/Users/Sos/Desktop/____/Github/Blockchain/Digital Signature( diplome validation )/2.pdf'
    wailcertif='C:/Users/Sos/Desktop/____/Github/Blockchain/Digital Signature( diplome validation )/1.pdf' 
    database = [["Lokmane","Zitouni","USTHB","181831091028",readPDF(lokcertif)],["WAil Zinedine","Alouane","USTHB","181831032956",readPDF(wailcertif)]]

    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(num, data=data))

    for block in blockchain.chain:
        print(block)

    print(blockchain.isValid())

    blockchain.chain[1].data[4] = readPDF(lokcertif)
    blockchain.mine(blockchain.chain[1])
    print(blockchain.isValid())
    print(blockchain.chain[1])


if __name__ == '__main__':
    main()