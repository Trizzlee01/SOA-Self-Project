import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    calculator_rpc = RpcProxy('calculator_service')

    @http('GET', 'prime/<int:idx>')
    def getPrime(self, request, idx):
        result = self.calculator_rpc.getPrime(idx)
        return json.dumps(result)

    @http('GET', 'prime/palindrome/<int:idx>')
    def getPrimePalindrome(self, request, idx):
        result = self.calculator_rpc.getPrimePalindrome(idx)
        return json.dumps(result)

