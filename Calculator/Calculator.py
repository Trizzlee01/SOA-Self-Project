from nameko.rpc import rpc
from CeleryFunction.getPrime import getPrime, prime
from CeleryFunction.getPalindrome import getPrimePalindrome, palindrome
from celery.result import AsyncResult

def isPalindrome(number):
    number = str(number)
    return number == number[::-1]

class CalculatorService:

    name = 'calculator_service'

    @rpc
    def getPrime(self, idx):
        index = getPrime.apply_async((idx,1))
        hasil = AsyncResult(index.id, app = prime)
        return hasil.get()
    
    @rpc
    def getPrimePalindrome(self, idx):
        index = getPrimePalindrome.apply_async((idx,1))
        hasil = AsyncResult(index.id, app= palindrome)
        return hasil.get()
    
