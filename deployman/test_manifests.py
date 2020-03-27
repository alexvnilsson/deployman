import manifests

m = manifests.read("deploy.yml")

print(m.name)