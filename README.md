# dolos

Dolos is the spirit of trickery and guile. He is also a master at cunning deception, craftiness, and treachery. Very similar in many ways to most cloud marketing departments.

Performance and error rate are important when you work all day with automation on a public cloud. Kubernetes cluster creation and deletion times are important if you value clean room testing as part of your pipelines.

This repo contains a set of scripts that will let you independently test each cloud provider.

# Usage

## Azure

Sign up to Azure and get your $200 of free credits.

This process follows the [kubernetes walkthrough](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough) documentation.

```
pip install -r requirements.txt
```
```
az login
```
```
az aks install-cli
```
```
nohup ./aks.py &
```

Leave this running for an hour or two and then grep the log.

```
grep -i "total create time taken" dolos.txt
```
```
grep -i "total destroy time taken" dolos.txt
```


## Google

Sign up to GCP and get your $300 of free credits.

Install the [Gcloud sdk](https://cloud.google.com/sdk/docs/quickstarts)

This process follows the [GKE Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart)

```
pip install -r requirements.txt
```
```
gcloud init
```
```
gcloud config set compute/zone us-east1-b
```
```
gcloud services enable container.googleapis.com
```
```
nohup ./gke.py &
```
It can take a few minutes for Google to enable billing on a brand new account. The script won't run until this has been setup.


## Amazon

This is currently dreadful. I have automation in Travis for this at work and it consistently takes 20 minutes. This includes creating a VPC, NAT gateway (a few mins), then starting EKS (about 11 mins), then the workers need to join.

For ephemeral testing environments you could setup a VPC and leave it active. Then deploy EKS clusters into it. EKS itself takes approximately 11 minutes.

```
aws_eks_cluster.master: Creation complete after 11m19s (ID: eks-a2ceb349c3-dev)
```

Add a bit of extra time onto that for workers to join and cluster level services to be ready and you are close to 15 minutes. Destruction of EKS itself is about 8 minutes.

```
[0m[1maws_eks_cluster.master: Destruction complete after 8m18s[0m[0m
```
 
Destroying a VPC can take a while. Again, bringing the process for deletion to around 15 minutes. An entire round trip for create, test and destroy would be in excess of 30 minutes.

## Others

Feel free to contribute a py file and some instructions in the readme.
