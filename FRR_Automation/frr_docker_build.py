import subprocess

def build_docker_image(tag, dockerfile_path):
    """
    Build a Docker image for the FRR configuration script.

    Args:
    - tag (str): Tag for the Docker image.
    - dockerfile_path (str): Path to the Dockerfile.

    Returns:
    - bool: True if image building is successful, False otherwise.
    """
    try:
        subprocess.run(['docker', 'build', '-t', tag, '-f', dockerfile_path, '.'], check=True)
        print(f"Docker image '{tag}' built successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to build Docker image. {e}")
        return False

def main():
    # Specify the tag for the Docker image
    image_tag = 'my-frr-script'

    # Specify the path to the Dockerfile
    dockerfile_path = '/home/ana-moeez-2/Desktop/frr_docker_automation/Dockerfile'

    # Build Docker image
    if build_docker_image(image_tag, dockerfile_path):
        print(f"Build successful. You can now run your Docker container with tag '{image_tag}'.")

if __name__ == "__main__":
    main()
