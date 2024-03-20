import docker
import hashlib

def calculate_sha256(image_name, tag):
    """Calculates the SHA256 hash of a Docker image.

    Args:
        image_name (str): Name of the Docker image.
        tag (str): Tag of the image (optional).

    Returns:
        str: The SHA256 hash of the image, or None if retrieval fails.
    """

    try:
        # Connect to Docker
        client = docker.from_env()

        # Check for `get_digest` method availability
        if hasattr(client.images, 'get_digest'):
            # Use `get_digest` for newer versions
            digest = client.images.get_digest(f"{image_name}:{tag}")
        else:
            # Fallback for older versions: inspect image and extract digest
            image = client.images.get(f"{image_name}:{tag}")
            digest = image.attrs['RepoDigests'][0]

        # Calculate SHA256 hash
        sha256_hash = hashlib.sha256(digest.encode()).hexdigest()

        return sha256_hash

    except Exception as e:
        print(f"Error retrieving SHA256: {e}")
        return None

# Example usage:
image_name = "kindest"
tag = ""
sha256_hash = calculate_sha256(image_name, tag)
print("SHA256 hash:", sha256_hash)
