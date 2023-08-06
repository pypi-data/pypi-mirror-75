from localstack.utils.aws import aws_models
jMVUf=super
jMVUW=None
jMVUl=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jMVUf(LambdaLayer,self).__init__(arn)
  self.cwd=jMVUW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,jMVUl,env=jMVUW):
  jMVUf(RDSDatabase,self).__init__(jMVUl,env=env)
 def name(self):
  return self.jMVUl.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,jMVUl,env=jMVUW):
  jMVUf(RDSCluster,self).__init__(jMVUl,env=env)
 def name(self):
  return self.jMVUl.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
