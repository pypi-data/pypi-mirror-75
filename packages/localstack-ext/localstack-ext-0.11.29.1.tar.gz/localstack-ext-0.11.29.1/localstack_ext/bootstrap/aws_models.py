from localstack.utils.aws import aws_models
mvuTW=super
mvuTh=None
mvuTH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  mvuTW(LambdaLayer,self).__init__(arn)
  self.cwd=mvuTh
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,mvuTH,env=mvuTh):
  mvuTW(RDSDatabase,self).__init__(mvuTH,env=env)
 def name(self):
  return self.mvuTH.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,mvuTH,env=mvuTh):
  mvuTW(RDSCluster,self).__init__(mvuTH,env=env)
 def name(self):
  return self.mvuTH.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
