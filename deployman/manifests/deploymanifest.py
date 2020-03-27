from yaml import YAMLObject

class DeployManifestArtifact(YAMLObject):
    def __init__(self, name: str=None, source: str=None, target: str=None):
        self.name = name
        self.source = source
        self.target = target
    

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name},source={self.source},target={self.target})"

class DeployManifestProcess(YAMLObject):
    def __init__(self, user: str=None, group: str=None):
        self.user = user
        self.group = group

    def __repr__(self):
        return f"{self.__class__.__name__}(user={self.user},group={self.group})"

class DeployManifest(YAMLObject):
    def __init__(self, name: str, artifact: DeployManifestArtifact, process: DeployManifestProcess):
        self.name = name
        self.artifact = artifact
        self.process = process

        self.path = None

    def set_manifest_path(self, manifest_path:str):
        self.path = manifest_path

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name},artifact={{self.artifact}},process={{self.artifact}})"