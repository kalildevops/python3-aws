from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.aws.network import Route53, CloudFront
from diagrams.aws.security import WAF
from diagrams.aws.storage import S3

with Diagram("Frontend with private bucket", show=True):
    user = Custom("User", "./icons/user.png")
    with Cluster("aws_account"):
        with Cluster("Private Bucket"):
            s3 =S3("S3 (static files)")
        user >> Edge(label="HTTPS") >> Route53("Route53") >> WAF("WAF") >> CloudFront("Cloudfront") >> s3