from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

def custom(image):
    return Custom(image.capitalize(), "./icons/" + image + ".png")

def label(text):
    return Edge(label=text)

with Diagram("", show=True):
    user = custom("user")
    terraform = custom("terraform")
    jenkins = custom("jenkins")
    gitlab = custom("gitlab")
    multiple_aws_infra = [
        Custom("Infra 1", "./icons/aws.png"),
        Custom("Infra 2", "./icons/aws.png"),
        Custom("Infra n", "./icons/aws.png")
    ]
    user >> gitlab >> jenkins >> terraform >> label("Apply/Update/Destroy") >> multiple_aws_infra