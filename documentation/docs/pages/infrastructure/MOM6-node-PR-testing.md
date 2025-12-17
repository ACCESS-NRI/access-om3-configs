ACCESS-NRI are a node of the [MOM6 Consortium](https://mom6.readthedocs.io/en/main/api/generated/pages/Testing.html#consortium-testing). As part of this, we review and test pull requests (PRs) to the `main` branch of the "authoritative" MOM6 code respository: [https://github.com/mom-ocean/MOM6/tree/main](https://github.com/mom-ocean/MOM6/tree/main).

MOM6 has a policy that existing solutions must be able to be preserved as the code base evolves. Our PR testing involves running a set of ACCESS configurations using MOM6 including the code changes in the PR under review. This is done on GitHub using ACCESS-NRI CI/CD infrastructure:

- We use the [ACCESS-NRI build-cd infrastucture](https://github.com/ACCESS-NRI/build-cd) to create prerelease deployments of the model(s) to be tested, typically ACCESS-OM3.
- We use the [ACCESS-NRI model configuration test infrastructure](https://github.com/ACCESS-NRI/model-config-tests) to check whether the code changes under review change answers.

A list of PRs to create ACCESS-OM3 prerelease deployments for the purpose of MOM6 node PR testing can be found [here](https://github.com/ACCESS-NRI/ACCESS-OM3/issues?q=label%3Amom6-PR-test). A list of PRs to test ACCESS-OM3 configurations using these deployments can be found [here](https://github.com/ACCESS-NRI/access-om3-configs/issues?q=label%3Amom6-pr-test).