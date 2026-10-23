FROM vllm/vllm-openai:v0.30.0@sha256:5f5e535216848d0c52159c8c13a0af04be5f6fe1a84e79914300610796f76d40

# Container Apps serverless GPU requires an unprivileged process. The model
# cache is disposable for this smoke; protocol runs need persistent weights.
ENV HOME=/tmp \
    HF_HOME=/tmp/huggingface \
    XDG_CACHE_HOME=/tmp/.cache
USER 10001:10001

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
