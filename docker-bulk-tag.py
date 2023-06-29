import docker

def tag_image(docker_client, image_id, repository, tags):
    try:
        for tag in tags:
            docker_client.images.get(image_id).tag(repository, tag)
            print(f"Image {repository}:{tag} tagged successfully!")
    except docker.errors.ImageNotFound:
        print(f"Image with ID {image_id} not found.")
    except docker.errors.APIError as e:
        print(f"Error tagging image: {e}")

# Docker client initialization
docker_client = docker.from_env()
"""
def format_numbers(input_string):
    numbers = input_string.strip().split('\n')
    string_array = [str(num) for num in numbers]
    return string_array

input_string = input("Enter the numbers (separated by new lines):\n")
numbers = format_numbers(input_string)
print(numbers)
"""


# Example usage
image_id = "deaba7fe0b87"
repository = "kevins311/single_schema_test1"
#tags=numbers
tags = [  '8.5-200-08',
    '8.5-200-09',
    '8.5-200-10',
    '8.5-214-01',
    '8.5-226-01',
    '8.5-226.1645809065-01',
    '8.5-236-01',
    '8.5-236.1647448331-01',
    '8.5-236.1648460182-01',
    '8.5-239-01',
    '8.5-239.1651231664-01',
    '8.6-754-01',
    '8.6-754.1655117782-01',
    '8.0.01'
]


tag_image(docker_client, image_id, repository, tags)

# Docker login
login_prompt = "Do you need to login to Docker? (y/n): "
login_required = input(login_prompt).lower()

if login_required == 'y':
    docker_username = input("Enter your Docker username: ")
    docker_password = input("Enter your Docker password: ")
    #docker_registry = input("Enter your Docker registry (e.g., https://index.docker.io/v1/): ")
    docker_client.login(username=docker_username, password=docker_password, registry=docker_registry)

# Docker push
push_prompt = f"Are you ready to push your containers to the repository '{repository}'? (y/n): "
push_confirmation = input(push_prompt).lower()

if push_confirmation == 'y':
    try:
        for tag in tags:
            docker_client.images.push(repository, tag)
            print(f"Image {repository}:{tag} pushed successfully!")
    except docker.errors.APIError as e:
        print(f"Error pushing image: {e}")
else:
    print("Push operation aborted.")