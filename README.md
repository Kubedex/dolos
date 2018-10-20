# dolos

Dolos is the spirit of trickery and guile. He is also a master at cunning deception, craftiness, and treachery. Very similar in many ways to most cloud marketing departments.

Performance and error rate are important when you work all day with automation on a public cloud. Kubernetes cluster creation and deletion times are important if you value clean room testing as part of your pipelines.

This repo contains a set of scripts that will let you independently test each cloud provider.

# Usage

## Azure

Sign up to Azure and get your $200 of free credits.

This process follows the [kubernetes walkthrough](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough) documentation.

```
pip install --user requirements.txt
```
```
az login
```
```
az aks install-cli
```
```
while true; do ./aks.py >> log.txt; sleep 2; done
```

Leave this running for an hour or two and then grep the log.

```
grep -i "total create time taken" log.txt
```
```
grep -i "total destroy time taken" log.txt
```


## Google

Not currently implemented. Everyone knows this takes less than 3 minutes so I'll probably only do this if anyone wants proof.

## Amazon

This is currently dreadful. I have automation in Travis for this at work and it consistently takes 20 minutes. This includes creating a VPC, NAT gateway (a few mins), then starting EKS (about 11 mins), then the workers need to join.

## Others

Feel free to contribute a py file and some instructions in the readme.
