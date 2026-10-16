# Sandbox image for running model-written code, used two ways (no network at run time):
#   - visible_runner.py: one disposable container per visible check (see
#     src/system1/loop/sandbox.py, VisibleRunner); no hidden data mounted.
#   - worker.py: the hidden-test grader in the `sandbox` compose service, with
#     the EvalPlus cache mounted read-only; it runs only after generation.
# EvalPlus is pinned so the hidden-test check is the official one.
FROM python:3.12.14-slim-bookworm@sha256:1aaa65a85fda306ffb8b910824d4e93bdce61e212c7e87168123ea3073b41a1a

RUN pip install --no-cache-dir evalplus==0.3.1 \
    && useradd --create-home --uid 10001 sandbox

COPY worker.py visible_runner.py /opt/sandbox/

USER sandbox
WORKDIR /tmp
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

CMD ["sleep", "infinity"]
