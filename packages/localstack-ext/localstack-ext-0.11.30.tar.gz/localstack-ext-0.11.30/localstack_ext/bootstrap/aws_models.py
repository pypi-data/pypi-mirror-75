from localstack.utils.aws import aws_models
Ezrwk=super
Ezrwx=None
Ezrwc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Ezrwk(LambdaLayer,self).__init__(arn)
  self.cwd=Ezrwx
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,Ezrwc,env=Ezrwx):
  Ezrwk(RDSDatabase,self).__init__(Ezrwc,env=env)
 def name(self):
  return self.Ezrwc.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,Ezrwc,env=Ezrwx):
  Ezrwk(RDSCluster,self).__init__(Ezrwc,env=env)
 def name(self):
  return self.Ezrwc.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
