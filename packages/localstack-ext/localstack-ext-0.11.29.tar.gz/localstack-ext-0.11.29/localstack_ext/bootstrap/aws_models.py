from localstack.utils.aws import aws_models
qOXSy=super
qOXSx=None
qOXSs=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qOXSy(LambdaLayer,self).__init__(arn)
  self.cwd=qOXSx
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,qOXSs,env=qOXSx):
  qOXSy(RDSDatabase,self).__init__(qOXSs,env=env)
 def name(self):
  return self.qOXSs.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,qOXSs,env=qOXSx):
  qOXSy(RDSCluster,self).__init__(qOXSs,env=env)
 def name(self):
  return self.qOXSs.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
