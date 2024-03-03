image_tag = ghcr.io/gem5/gem5-tutorial-hpca-2024-env:latest

.DEFAULT_GOAL := gem5-tutorial-env-push

gem5-tutorial-env-push: gem5-tutorial-env
	@echo "Pushing the gem5 tutorial docker image"
	docker push $(image_tag)

gem5-tutorial-env: gem5-tutorial-env-pull
	@echo "Building the gem5 tutorial docker image"
	docker build docker  -t $(image_tag)

gem5-tutorial-env-pull:
	@echo "Pulling the gem5 tutorial docker image"
	- docker pull $(image_tag)
