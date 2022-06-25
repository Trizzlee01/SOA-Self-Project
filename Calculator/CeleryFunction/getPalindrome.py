from celery import Celery

palindrome = Celery ('prime', broker = 'redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')

palindrome.conf.task_routes = {
    'CeleryFunction.getPalindrome.getPrimePalindrome': {'queue': 'palindrome'}
}

def isPalindrome(number):
    number = str(number)
    return number == number[::-1]

@palindrome.task
def getPrimePalindrome(index, tes):
    ctr=1
    number=3
    if index==1:
        result=2
    else:
        while ctr<index:
            prime=True 
            for i in range(2, number-1):
                if number%i==0:
                    prime=False
                    break
            
            if prime==True:

                if isPalindrome(number):
                    ctr+=1
                    if ctr==index:
                        result = number
                        break
            
            number+=1
    
    hasil= {
        "result": result
    }
    return hasil