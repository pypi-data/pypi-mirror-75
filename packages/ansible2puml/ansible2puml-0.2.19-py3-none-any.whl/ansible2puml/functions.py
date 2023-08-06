import yaml
import json
from jinja2 import Template
import plantuml as plantuml


def parseAnsibleFile(filePath, destination):
    """
    Parse Ansible yaml file
    """
    with open(filePath, "r") as f:
        ansible_file = yaml.load(f, Loader=yaml.FullLoader)
        print(f"Filename: {f.name}")
        # print(f"Parsed: {json.dumps(ansible_file, indent=2)}")

    tasks = []

    for item in ansible_file:
        # if there is a key "tasks" it is a playbook
        if item["tasks"]:
            # if name in playbook
            if "name" in item:
                tasks.append(
                    {"taskDescription": item["name"], "bold": True})

            for task in item["tasks"]:
                if "name" in task:
                    tasks.append({"taskDescription": task["name"]})

                # if task is a block
                if "block" in task:
                    for returnedTask in parseBlock(block=task["block"]):
                        tasks.append(returnedTask)

        # parse tasks file
        else:
            for task in item:
                if "name" in task:
                    tasks.append({"taskDescription": task["name"]})

    # print(f"Extracted: {json.dumps(tasks, indent=2)}")
    generatePlantUML(tasks, destination)


def parseBlock(block):
    array = []
    for item in block:
        if "name" in item:
            array.append({"taskDescription": item["name"]})
    return array


def generatePlantUML(taskArray, destination):
    """
    Generate a PlantUML File from a tasks array.
    """

    activityTemplate = """@startuml
skinparam defaultTextAlignment center
skinparam componentStyle uml2

skinparam activity {
    FontColor          white
    AttributeFontColor white
    FontSize           17
    AttributeFontSize  15
    AttributeFontname  Droid Sans Mono
    BackgroundColor    #527BC6
    BorderColor        black
    ArrowColor         #222266
    ArrowFontSize      15
}

skinparam activityDiamond {
    FontColor          white
    AttributeFontColor white
    FontSize           17
    BackgroundColor    #527BC6
    BorderColor        black
}

{% for item in taskArray -%}
{% if item.bold -%}
:**{{ item.taskDescription }}**;
{% else -%}
:{{ item.taskDescription }};
{% endif -%}
{% endfor -%}
@enduml
"""

    rendered = Template(activityTemplate).render(taskArray=taskArray)

    plantUML = plantuml.PlantUML(url="http://www.plantuml.com/plantuml/png/")
    url = plantUML.get_url(plantuml_text=rendered)

    with open(destination, "w") as f:
        f.write(rendered)

    print(f"PNG: {url}")
