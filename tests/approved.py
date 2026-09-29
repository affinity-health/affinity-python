import asyncio, json, urllib.request
from affinity import Affinity, AsyncAffinity, AffinityError
BASE='http://127.0.0.1:5199/python-practice-retry'
api=Affinity('test',base_url=BASE,max_retries=1)
urllib.request.urlopen(BASE+'/reset').read()
patient=api.patients.create(params={'name':{'first':'Alex','last':'Example'},'date_of_birth':'1990-01-01'})
assert patient.id=='pat_a'
api.patients.update(patient.id,params={'email':None})
api.patients.delete(patient.id)
patients=api.patients.iterate(params={'limit':1,'query':'Alex'})
assert [p.id for p in patients]==['pat_a','pat_b']
try:api.patients.get('pat_a',options={'practice_id':'prac_b'})
except ValueError:pass
else:raise AssertionError('practice mismatch accepted')
try:api.orders.submit('ord_a')
except ValueError:pass
else:raise AssertionError('missing key accepted')
api.orders.sign('ord_a',params={'prescriber':{'id':'prov_a'},'expected_revision':'rev_reviewed','signature_attestation':True},options={'idempotency_key':'sign_job'})
api.orders.submit('ord_a',options={'idempotency_key':'submit_job'})
try:api.patients.get('pat_error')
except AffinityError as error:
 assert error.status==429 and error.code=='rate_limited' and error.request_id=='req_a' and error.retry_after==0
 assert 'private' not in str(error)
else:raise AssertionError('missing error')
trace=json.load(urllib.request.urlopen(BASE+'/trace'))
assert len([r for r in trace if r['path']=='/v1/auth/access'])==1
writes=[r for r in trace if r['method']=='PATCH']
assert len(writes)==2 and writes[0]['key']==writes[1]['key'] and writes[0]['body']=={'email':None}
assert len({r['key'] for r in trace if r['method'] in ['POST','DELETE','PATCH']})>=4
async def check_async():
 api=AsyncAffinity('test',base_url='http://127.0.0.1:5199/python-platform')
 scoped=api.for_practice('prac_a')
 assert (await scoped.patients.get('pat_a')).id=='pat_a'
 assert [p.id async for p in scoped.patients.iterate(params={'limit':1})]==['pat_a','pat_b']
 try:await api.patients.get('pat_a')
 except ValueError:pass
 else:raise AssertionError('platform default practice')
asyncio.run(check_async())
print('Python approved interface passed')
