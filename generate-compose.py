import os
from jinja2 import Template

# Docker Compose template for multiple LLM services
docker_compose_template = """
version: '3'
services:
  framework:
    build:
      context: ./framework
    image: local-framework-image
    ports:
      - "{{ framework_port }}:5000"
    depends_on:
      {% if llm_count > 0 %}
      {% for i in range(llm_count) %}
      - llm_{{ i }}
      {% endfor %}
      {% endif %}

  {% for i in range(llm_count) %}
  llm_{{ i }}:
    build:
      context: ./llm
    image: local-llm-image_{{ i }}
    ports:
      - "{{ llm_base_port + i }}:5000"
  {% endfor %}
"""

# Configuration variables
framework_port = 8000  # Framework port
llm_base_port = 5002   # Base port for LLM services
llm_count = 3          # Number of LLM containers

# Generate the docker-compose.yml file using Jinja2 template
template = Template(docker_compose_template)
docker_compose_content = template.render(
    framework_port=framework_port,
    llm_base_port=llm_base_port,
    llm_count=llm_count
)

# Write the generated content to docker-compose.yml
with open("docker-compose.yml", "w") as f:
    f.write(docker_compose_content)

print("docker-compose.yml generated successfully")

# Function to build Docker images
def build_docker_image(image_name, dockerfile_path):
    try:
        command = f"docker build -t {image_name} -f {dockerfile_path} ."
        os.system(command)
        print(f"Image {image_name} built successfully")
    except Exception as e:
        print(f"Failed to build image {image_name}: {e}")

# Paths to Dockerfiles
framework_dockerfile = "framework/Dockerfile"
llm_dockerfile = "llm/Dockerfile"

# Build the framework Docker image
build_docker_image("local-framework-image", framework_dockerfile)

# Build LLM Docker images
for i in range(llm_count):
    build_docker_image(f"local-llm-image_{i}", llm_dockerfile)

print("All Docker images built successfully")

# Start the Docker containers
os.system("docker-compose up -d")
print("Docker containers started successfully")
