from localstack.utils.aws import aws_models
sFClW=super
sFClN=None
sFClA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  sFClW(LambdaLayer,self).__init__(arn)
  self.cwd=sFClN
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,sFClA,env=sFClN):
  sFClW(RDSDatabase,self).__init__(sFClA,env=env)
 def name(self):
  return self.sFClA.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,sFClA,env=sFClN):
  sFClW(RDSCluster,self).__init__(sFClA,env=env)
 def name(self):
  return self.sFClA.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
