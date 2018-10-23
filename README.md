# dolos

Dolos is the spirit of trickery and guile. He is also a master at cunning deception, craftiness, and treachery. Very similar in many ways to most cloud marketing departments.

Performance and error rate are important when you work all day with automation on a public cloud. Kubernetes cluster creation and deletion times are important if you value clean room testing as part of your pipelines.

This repo contains a set of scripts that will let you independently test each cloud provider.

# Usage

You'll need Python 3 and Docker. Read each section below in order to create some credentials to put into the config.yml.

Once you have good `config.yml` and `service-account.json` files simply run `docker-compose up -d`. This will start a container per cloud and update a logfile in `log/`. Leave it running for a few hours and you should get a number of creation and deletion timings.

Each cloud is tested in the same way. Starting from a brand new account with nothing in we provision a Kubernetes cluster, deploy an application, and then test it's up. We then delete everything and try again, in a loop, forever until you cancel it.

*Warning: cloud resources cost money so don't accidentally leave this on forever*


## Azure

Sign up to Azure and get your $200 of free credits.

This process follows the [kubernetes walkthrough](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough) documentation.

Install the Azure CLI tool on your laptop.
```
pip install --user azure-cli
```

Login and authenticate via a web browser.
```
az login
```

Create a service principle with a password of your choice. Make a note of the `appId` and `tenant` fields for the next commands.
```
az ad sp create-for-rbac --name dolos --password <PASSWORD>
```

Take the `appId` value from the previous command and use it in the role assignment.
```
az role assignment create --assignee <APP_ID> --role Owner
```

Take the `appId`, `password` and `tenant` from the previous commands and try to login.
```
az login --service-principal --username <APP_ID> --password <PASSWORD> --tenant <TENANT_ID>
```

Create a Resource Group
```
az group create --name dolos --location eastus
```

Now put the `appId`, `password` and `tenant` into the `config.yml.example` and rename the file to `config.yml`.

## Google

Sign up to GCP and get your $300 of free credits. Then [enable billing](https://cloud.google.com/billing/docs/how-to/modify-project?visit_id=636756998918052718-1229259697&rd=1#enable-billing).

Install the [Gcloud sdk](https://cloud.google.com/sdk/docs/quickstarts)

This process follows the [GKE Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart)

Login for the first time on your local machine.
```
gcloud init
```

Set some variables for the service account we're about to create.
```
export PROJECT_ID=$(gcloud config get-value core/project)
export SERVICE_ACCOUNT_NAME="dolos-sa"
```

Create the service account.
```
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} --display-name "Dolos Service Account"
```

Assign the service account to the project and give it a role.
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role='roles/owner'
```

Download the service-account.json. This need to stay in the root dir of this repo.
```
gcloud iam service-accounts keys create \
  --iam-account "${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  service-account.json
```

Go to the link that pops up when this errors and click enable. Not sure how to do this without an error.
```
gcloud services enable serviceusage.googleapis.com
```

Enable the container services.
```
gcloud services enable container.googleapis.com
```

Finally, take the value for `project_id` in the `service-account.json` and put it in `config.yml` under the gke section.

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
