## Amazon EKS Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This construct library allows you to define [Amazon Elastic Container Service
for Kubernetes (EKS)](https://aws.amazon.com/eks/) clusters programmatically.
This library also supports programmatically defining Kubernetes resource
manifests within EKS clusters.

This example defines an Amazon EKS cluster with the following configuration:

* Managed nodegroup with 2x **m5.large** instances (this instance type suits most common use-cases, and is good value for money)
* Dedicated VPC with default configuration (see [ec2.Vpc](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ec2-readme.html#vpc))
* A Kubernetes pod with a container based on the [paulbouwer/hello-kubernetes](https://github.com/paulbouwer/hello-kubernetes) image.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = eks.Cluster(self, "hello-eks",
    version=eks.KubernetesVersion.V1_16
)

cluster.add_resource("mypod",
    api_version="v1",
    kind="Pod",
    metadata={"name": "mypod"},
    spec={
        "containers": [{
            "name": "hello",
            "image": "paulbouwer/hello-kubernetes:1.5",
            "ports": [{"container_port": 8080}]
        }
        ]
    }
)
```

### Capacity

By default, `eks.Cluster` is created with a managed nodegroup with x2 `m5.large` instances. You must specify the kubernetes version for the cluster with the `version` property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster-two-m5-large",
    version=eks.KubernetesVersion.V1_16
)
```

To use the traditional self-managed Amazon EC2 instances instead, set `defaultCapacityType` to `DefaultCapacityType.EC2`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = eks.Cluster(self, "cluster-self-managed-ec2",
    default_capacity_type=eks.DefaultCapacityType.EC2,
    version=eks.KubernetesVersion.V1_16
)
```

The quantity and instance type for the default capacity can be specified through
the `defaultCapacity` and `defaultCapacityInstance` props:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster",
    default_capacity=10,
    default_capacity_instance=ec2.InstanceType("m2.xlarge"),
    version=eks.KubernetesVersion.V1_16
)
```

To disable the default capacity, simply set `defaultCapacity` to `0`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster-with-no-capacity",
    default_capacity=0,
    version=eks.KubernetesVersion.V1_16
)
```

The `cluster.defaultCapacity` property will reference the `AutoScalingGroup`
resource for the default capacity. It will be `undefined` if `defaultCapacity`
is set to `0` or `defaultCapacityType` is either `NODEGROUP` or undefined.

And the `cluster.defaultNodegroup` property will reference the `Nodegroup`
resource for the default capacity. It will be `undefined` if `defaultCapacity`
is set to `0` or `defaultCapacityType` is `EC2`.

You can add `AutoScalingGroup` resource as customized capacity through `cluster.addCapacity()` or
`cluster.addAutoScalingGroup()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_capacity("frontend-nodes",
    instance_type=ec2.InstanceType("t2.medium"),
    min_capacity=3,
    vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC}
)
```

### Managed Node Groups

Amazon EKS managed node groups automate the provisioning and lifecycle management of nodes (Amazon EC2 instances)
for Amazon EKS Kubernetes clusters. By default, `eks.Nodegroup` create a nodegroup with x2 `t3.medium` instances.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Nodegroup(stack, "nodegroup", cluster=cluster)
```

You can add customized node group through `cluster.addNodegroup()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_nodegroup("nodegroup",
    instance_type=ec2.InstanceType("m5.large"),
    min_size=4
)
```

### Fargate

AWS Fargate is a technology that provides on-demand, right-sized compute
capacity for containers. With AWS Fargate, you no longer have to provision,
configure, or scale groups of virtual machines to run containers. This removes
the need to choose server types, decide when to scale your node groups, or
optimize cluster packing.

You can control which pods start on Fargate and how they run with Fargate
Profiles, which are defined as part of your Amazon EKS cluster.

See [Fargate
Considerations](https://docs.aws.amazon.com/eks/latest/userguide/fargate.html#fargate-considerations)
in the AWS EKS User Guide.

You can add Fargate Profiles to any EKS cluster defined in your CDK app
through the `addFargateProfile()` method. The following example adds a profile
that will match all pods from the "default" namespace:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_fargate_profile("MyProfile",
    selectors=[{"namespace": "default"}]
)
```

To create an EKS cluster that **only** uses Fargate capacity, you can use
`FargateCluster`.

The following code defines an Amazon EKS cluster without EC2 capacity and a default
Fargate Profile that matches all pods from the "kube-system" and "default" namespaces. It is also configured to [run CoreDNS on Fargate](https://docs.aws.amazon.com/eks/latest/userguide/fargate-getting-started.html#fargate-gs-coredns) through the `coreDnsComputeType` cluster option.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = eks.FargateCluster(self, "MyCluster",
    version=eks.KubernetesVersion.V1_16
)

# apply k8s resources on this cluster
cluster.add_resource(...)
```

**NOTE**: Classic Load Balancers and Network Load Balancers are not supported on
pods running on Fargate. For ingress, we recommend that you use the [ALB Ingress
Controller](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)
on Amazon EKS (minimum version v1.1.4).

### Spot Capacity

If `spotPrice` is specified, the capacity will be purchased from spot instances:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_capacity("spot",
    spot_price="0.1094",
    instance_type=ec2.InstanceType("t3.large"),
    max_capacity=10
)
```

Spot instance nodes will be labeled with `lifecycle=Ec2Spot` and tainted with `PreferNoSchedule`.

The [AWS Node Termination Handler](https://github.com/aws/aws-node-termination-handler)
DaemonSet will be installed from [
Amazon EKS Helm chart repository
](https://github.com/aws/eks-charts/tree/master/stable/aws-node-termination-handler) on these nodes. The termination handler ensures that the Kubernetes control plane responds appropriately to events that can cause your EC2 instance to become unavailable, such as [EC2 maintenance events](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances-status-check_sched.html) and [EC2 Spot interruptions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-interruptions.html) and helps gracefully stop all pods running on spot nodes that are about to be
terminated.

### Bootstrapping

When adding capacity, you can specify options for
[/etc/eks/boostrap.sh](https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh)
which is responsible for associating the node to the EKS cluster. For example,
you can use `kubeletExtraArgs` to add custom node labels or taints.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# up to ten spot instances
cluster.add_capacity("spot",
    instance_type=ec2.InstanceType("t3.large"),
    min_capacity=2,
    bootstrap_options={
        "kubelet_extra_args": "--node-labels foo=bar,goo=far",
        "aws_api_retry_attempts": 5
    }
)
```

To disable bootstrapping altogether (i.e. to fully customize user-data), set `bootstrapEnabled` to `false` when you add
the capacity.

### Masters Role

The Amazon EKS construct library allows you to specify an IAM role that will be
granted `system:masters` privileges on your cluster.

Without specifying a `mastersRole`, you will not be able to interact manually
with the cluster.

The following example defines an IAM role that can be assumed by all users
in the account and shows how to use the `mastersRole` property to map this
role to the Kubernetes `system:masters` group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# first define the role
cluster_admin = iam.Role(self, "AdminRole",
    assumed_by=iam.AccountRootPrincipal()
)

# now define the cluster and map role to "masters" RBAC group
eks.Cluster(self, "Cluster",
    masters_role=cluster_admin,
    version=eks.KubernetesVersion.V1_16
)
```

When you `cdk deploy` this CDK app, you will notice that an output will be printed
with the `update-kubeconfig` command.

Something like this:

```
Outputs:
eks-integ-defaults.ClusterConfigCommand43AAE40F = aws eks update-kubeconfig --name cluster-ba7c166b-c4f3-421c-bf8a-6812e4036a33 --role-arn arn:aws:iam::112233445566:role/eks-integ-defaults-Role1ABCC5F0-1EFK2W5ZJD98Y
```

Copy & paste the "`aws eks update-kubeconfig ...`" command to your shell in
order to connect to your EKS cluster with the "masters" role.

Now, given [AWS CLI](https://aws.amazon.com/cli/) is configured to use AWS
credentials for a user that is trusted by the masters role, you should be able
to interact with your cluster through `kubectl` (the above example will trust
all users in the account).

For example:

```console
$ aws eks update-kubeconfig --name cluster-ba7c166b-c4f3-421c-bf8a-6812e4036a33 --role-arn arn:aws:iam::112233445566:role/eks-integ-defaults-Role1ABCC5F0-1EFK2W5ZJD98Y
Added new context arn:aws:eks:eu-west-2:112233445566:cluster/cluster-ba7c166b-c4f3-421c-bf8a-6812e4036a33 to /Users/boom/.kube/config

$ kubectl get nodes # list all nodes
NAME                                         STATUS   ROLES    AGE   VERSION
ip-10-0-147-66.eu-west-2.compute.internal    Ready    <none>   21m   v1.13.7-eks-c57ff8
ip-10-0-169-151.eu-west-2.compute.internal   Ready    <none>   21m   v1.13.7-eks-c57ff8

$ kubectl get all -n kube-system
NAME                           READY   STATUS    RESTARTS   AGE
pod/aws-node-fpmwv             1/1     Running   0          21m
pod/aws-node-m9htf             1/1     Running   0          21m
pod/coredns-5cb4fb54c7-q222j   1/1     Running   0          23m
pod/coredns-5cb4fb54c7-v9nxx   1/1     Running   0          23m
pod/kube-proxy-d4jrh           1/1     Running   0          21m
pod/kube-proxy-q7hh7           1/1     Running   0          21m

NAME               TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)         AGE
service/kube-dns   ClusterIP   172.20.0.10   <none>        53/UDP,53/TCP   23m

NAME                        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/aws-node     2         2         2       2            2           <none>          23m
daemonset.apps/kube-proxy   2         2         2       2            2           <none>          23m

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/coredns   2/2     2            2           23m

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/coredns-5cb4fb54c7   2         2         2       23m
```

For your convenience, an AWS CloudFormation output will automatically be
included in your template and will be printed when running `cdk deploy`.

**NOTE**: if the cluster is configured with `kubectlEnabled: false`, it
will be created with the role/user that created the AWS CloudFormation
stack. See [Kubectl Support](#kubectl-support) for details.

### Kubernetes Resources

The `KubernetesResource` construct or `cluster.addResource` method can be used
to apply Kubernetes resource manifests to this cluster.

The following examples will deploy the [paulbouwer/hello-kubernetes](https://github.com/paulbouwer/hello-kubernetes)
service on the cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app_label = {"app": "hello-kubernetes"}

deployment = {
    "api_version": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "hello-kubernetes"},
    "spec": {
        "replicas": 3,
        "selector": {"match_labels": app_label},
        "template": {
            "metadata": {"labels": app_label},
            "spec": {
                "containers": [{
                    "name": "hello-kubernetes",
                    "image": "paulbouwer/hello-kubernetes:1.5",
                    "ports": [{"container_port": 8080}]
                }
                ]
            }
        }
    }
}

service = {
    "api_version": "v1",
    "kind": "Service",
    "metadata": {"name": "hello-kubernetes"},
    "spec": {
        "type": "LoadBalancer",
        "ports": [{"port": 80, "target_port": 8080}],
        "selector": app_label
    }
}

# option 1: use a construct
KubernetesResource(self, "hello-kub",
    cluster=cluster,
    manifest=[deployment, service]
)

# or, option2: use `addResource`
cluster.add_resource("hello-kub", service, deployment)
```

#### Adding resources from a URL

The following example will deploy the resource manifest hosting on remote server:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import js_yaml as yaml
import sync_request as request

manifest_url = "https://url/of/manifest.yaml"
manifest = yaml.safe_load_all(request("GET", manifest_url).get_body())
cluster.add_resource("my-resource", (SpreadElement ...manifest
  manifest))
```

Since Kubernetes resources are implemented as CloudFormation resources in the
CDK. This means that if the resource is deleted from your code (or the stack is
deleted), the next `cdk deploy` will issue a `kubectl delete` command and the
Kubernetes resources will be deleted.

#### Dependencies

There are cases where Kubernetes resources must be deployed in a specific order.
For example, you cannot define a resource in a Kubernetes namespace before the
namespace was created.

You can represent dependencies between `KubernetesResource`s using
`resource.node.addDependency()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
namespace = cluster.add_resource("my-namespace",
    api_version="v1",
    kind="Namespace",
    metadata={"name": "my-app"}
)

service = cluster.add_resource("my-service",
    metadata={
        "name": "myservice",
        "namespace": "my-app"
    },
    spec=
)

service.node.add_dependency(namespace)
```

NOTE: when a `KubernetesResource` includes multiple resources (either directly
or through `cluster.addResource()`) (e.g. `cluster.addResource('foo', r1, r2, r3,...))`), these resources will be applied as a single manifest via `kubectl`
and will be applied sequentially (the standard behavior in `kubectl`).

### Patching Kubernetes Resources

The KubernetesPatch construct can be used to update existing kubernetes
resources. The following example can be used to patch the `hello-kubernetes`
deployment from the example above with 5 replicas.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KubernetesPatch(self, "hello-kub-deployment-label",
    cluster=cluster,
    resource_name="deployment/hello-kubernetes",
    apply_patch={"spec": {"replicas": 5}},
    restore_patch={"spec": {"replicas": 3}}
)
```

### AWS IAM Mapping

As described in the [Amazon EKS User Guide](https://docs.aws.amazon.com/en_us/eks/latest/userguide/add-user-role.html),
you can map AWS IAM users and roles to [Kubernetes Role-based access control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac).

The Amazon EKS construct manages the **aws-auth ConfigMap** Kubernetes resource
on your behalf and exposes an API through the `cluster.awsAuth` for mapping
users, roles and accounts.

Furthermore, when auto-scaling capacity is added to the cluster (through
`cluster.addCapacity` or `cluster.addAutoScalingGroup`), the IAM instance role
of the auto-scaling group will be automatically mapped to RBAC so nodes can
connect to the cluster. No manual mapping is required any longer.

> NOTE: `cluster.awsAuth` will throw an error if your cluster is created with `kubectlEnabled: false`.

For example, let's say you want to grant an IAM user administrative privileges
on your cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
admin_user = iam.User(self, "Admin")
cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
```

A convenience method for mapping a role to the `system:masters` group is also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.aws_auth.add_masters_role(role)
```

### Cluster Security Group

When you create an Amazon EKS cluster, a
[cluster security group](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html)
is automatically created as well. This security group is designed to allow
all traffic from the control plane and managed node groups to flow freely
between each other.

The ID for that security group can be retrieved after creating the cluster.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_security_group_id = cluster.cluster_security_group_id
```

### Cluster Encryption Configuration

When you create an Amazon EKS cluster, envelope encryption of
Kubernetes secrets using the AWS Key Management Service (AWS KMS) can be enabled. The documentation
on [creating a cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)
can provide more details about the customer master key (CMK) that can be used for the encryption.

The Amazon Resource Name (ARN) for that CMK can be retrieved.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_encryption_config_key_arn = cluster.cluster_encryption_config_key_arn
```

### Node ssh Access

If you want to be able to SSH into your worker nodes, you must already
have an SSH key in the region you're connecting to and pass it, and you must
be able to connect to the hosts (meaning they must have a public IP and you
should be allowed to connect to them on port 22):

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
asg = cluster.add_capacity("Nodes",
    instance_type=ec2.InstanceType("t2.medium"),
    vpc_subnets=SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
    key_name="my-key-name"
)

# Replace with desired IP
asg.connections.allow_from(ec2.Peer.ipv4("1.2.3.4/32"), ec2.Port.tcp(22))
```

If you want to SSH into nodes in a private subnet, you should set up a
bastion host in a public subnet. That setup is recommended, but is
unfortunately beyond the scope of this documentation.

### kubectl Support

When you create an Amazon EKS cluster, the IAM entity user or role, such as a
[federated user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html)
that creates the cluster, is automatically granted `system:masters` permissions
in the cluster's RBAC configuration.

In order to allow programmatically defining **Kubernetes resources** in your AWS
CDK app and provisioning them through AWS CloudFormation, we will need to assume
this "masters" role every time we want to issue `kubectl` operations against your
cluster.

At the moment, the [AWS::EKS::Cluster](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html)
AWS CloudFormation resource does not support this behavior, so in order to
support "programmatic kubectl", such as applying manifests
and mapping IAM roles from within your CDK application, the Amazon EKS
construct library uses a custom resource for provisioning the cluster.
This custom resource is executed with an IAM role that we can then use
to issue `kubectl` commands.

The default behavior of this library is to use this custom resource in order
to retain programmatic control over the cluster. In other words: to allow
you to define Kubernetes resources in your CDK code instead of having to
manage your Kubernetes applications through a separate system.

One of the implications of this design is that, by default, the user who
provisioned the AWS CloudFormation stack (executed `cdk deploy`) will
not have administrative privileges on the EKS cluster.

1. Additional resources will be synthesized into your template (the AWS Lambda
   function, the role and policy).
2. As described in [Interacting with Your Cluster](#interacting-with-your-cluster),
   if you wish to be able to manually interact with your cluster, you will need
   to map an IAM role or user to the `system:masters` group. This can be either
   done by specifying a `mastersRole` when the cluster is defined, calling
   `cluster.awsAuth.addMastersRole` or explicitly mapping an IAM role or IAM user to the
   relevant Kubernetes RBAC groups using `cluster.addRoleMapping` and/or
   `cluster.addUserMapping`.

If you wish to disable the programmatic kubectl behavior and use the standard
AWS::EKS::Cluster resource, you can specify `kubectlEnabled: false` when you define
the cluster:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eks.Cluster(self, "cluster",
    kubectl_enabled=False
)
```

**Take care**: a change in this property will cause the cluster to be destroyed
and a new cluster to be created.

When kubectl is disabled, you should be aware of the following:

1. When you log-in to your cluster, you don't need to specify `--role-arn` as
   long as you are using the same user that created the cluster.
2. As described in the Amazon EKS User Guide, you will need to manually
   edit the [aws-auth ConfigMap](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)
   when you add capacity in order to map the IAM instance role to RBAC to allow nodes to join the cluster.
3. Any `eks.Cluster` APIs that depend on programmatic kubectl support will fail
   with an error: `cluster.addResource`, `cluster.addChart`, `cluster.awsAuth`, `props.mastersRole`.

### Helm Charts

The `HelmChart` construct or `cluster.addChart` method can be used
to add Kubernetes resources to this cluster using Helm.

The following example will install the [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
to you cluster using Helm.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# option 1: use a construct
HelmChart(self, "NginxIngress",
    cluster=cluster,
    chart="nginx-ingress",
    repository="https://helm.nginx.com/stable",
    namespace="kube-system"
)

# or, option2: use `addChart`
cluster.add_chart("NginxIngress",
    chart="nginx-ingress",
    repository="https://helm.nginx.com/stable",
    namespace="kube-system"
)
```

Helm charts will be installed and updated using `helm upgrade --install`, where a few parameters
are being passed down (such as `repo`, `values`, `version`, `namespace`, `wait`, `timeout`, etc).
This means that if the chart is added to CDK with the same release name, it will try to update
the chart in the cluster. The chart will exists as CloudFormation resource.

Helm charts are implemented as CloudFormation resources in CDK.
This means that if the chart is deleted from your code (or the stack is
deleted), the next `cdk deploy` will issue a `helm uninstall` command and the
Helm chart will be deleted.

When there is no `release` defined, the chart will be installed using the `node.uniqueId`,
which will be lower cased and truncated to the last 63 characters.

By default, all Helm charts will be installed concurrently. In some cases, this
could cause race conditions where two Helm charts attempt to deploy the same
resource or if Helm charts depend on each other. You can use
`chart.node.addDependency()` in order to declare a dependency order between
charts:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
chart1 = cluster.add_chart(...)
chart2 = cluster.add_chart(...)

chart2.node.add_dependency(chart1)
```

### Bottlerocket

[Bottlerocket](https://aws.amazon.com/bottlerocket/) is a Linux-based open-source operating system that is purpose-built by Amazon Web Services for running containers on virtual machines or bare metal hosts. At this moment the managed nodegroup only supports Amazon EKS-optimized AMI but it's possible to create a capacity of self-managed `AutoScalingGroup` running with bottlerocket Linux AMI.

> **NOTICE**: Bottlerocket is in public preview and only available in [some supported AWS regions](https://github.com/bottlerocket-os/bottlerocket/blob/develop/QUICKSTART.md#finding-an-ami).

The following example will create a capacity with self-managed Amazon EC2 capacity of 2 `t3.small` Linux instances running with `Bottlerocket` AMI.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# add bottlerocket nodes
cluster.add_capacity("BottlerocketNodes",
    instance_type=ec2.InstanceType("t3.small"),
    min_capacity=2,
    machine_image_type=eks.MachineImageType.BOTTLEROCKET
)
```

To define only Bottlerocket capacity in your cluster, set `defaultCapacity` to `0` when you define the cluster as described above.

Please note Bottlerocket does not allow to customize bootstrap options and `bootstrapOptions` properties is not supported when you create the `Bottlerocket` capacity.

### Service Accounts

With services account you can provide Kubernetes Pods access to AWS resources.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# add service account
sa = cluster.add_service_account("MyServiceAccount")

bucket = Bucket(self, "Bucket")
bucket.grant_read_write(service_account)

mypod = cluster.add_resource("mypod",
    api_version="v1",
    kind="Pod",
    metadata={"name": "mypod"},
    spec={
        "service_account_name": sa.service_account_name,
        "containers": [{
            "name": "hello",
            "image": "paulbouwer/hello-kubernetes:1.5",
            "ports": [{"container_port": 8080}]
        }
        ]
    }
)

# create the resource after the service account
mypod.node.add_dependency(sa)

# print the IAM role arn for this service account
cdk.CfnOutput(self, "ServiceAccountIamRole", value=sa.role.role_arn)
```

### Roadmap

* [ ] AutoScaling (combine EC2 and Kubernetes scaling)
