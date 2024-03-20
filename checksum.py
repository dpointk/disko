import docker
import hashlib

def pull_image(source_repo, image_name, tag='latest'):
    client = docker.from_env()
    image_tag = f"{source_repo}/{image_name}:{tag}"
    print(f"Pulling image: {image_tag}")
    client.images.pull(image_tag)

def tag_image(source_repo, target_repo, image_name, tag='latest'):
    client = docker.from_env()
    source_image_tag = f"{source_repo}/{image_name}:{tag}"
    target_image_tag = f"{target_repo}/{image_name}:{tag}"
    print(f"Tagging image: {source_image_tag} => {target_image_tag}")
    client.images.get(source_image_tag).tag(target_image_tag)

def get_image_digest(repo, image_name, tag='latest'):
    client = docker.from_env()
    image_tag = f"{repo}/{image_name}:{tag}"
    image = client.images.get(image_tag)
    return image.id.split(":")[1]

def calculate_sha256(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    source_repo = 'source_repo'
    target_repo = 'target_repo'
    image_name = 'kindest/node'
    tag = ''

    pull_image(source_repo, image_name, tag)
    tag_image(source_repo, target_repo, image_name, tag)

    source_digest = get_image_digest(source_repo, image_name, tag)
    target_digest = get_image_digest(target_repo, image_name, tag)

    if source_digest == target_digest:
        print("Image digests match.")
    else:
        print("Image digests do not match.")

if __name__ == "__main__":
    main()
