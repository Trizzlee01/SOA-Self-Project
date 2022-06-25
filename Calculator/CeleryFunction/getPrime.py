from celery import Celery

prime = Celery ('prime', broker = 'redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')

prime.conf.task_routes = {
    'CeleryFunction.getPrime.getPrime': {'queue': 'prime'}
}

@prime.task
def getPrime(index, tes):
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
                ctr+=1
                if ctr==index:
                    result = number
                    break
            
            number+=1
    
    hasil= {
        "result": result
    }
    return hasil