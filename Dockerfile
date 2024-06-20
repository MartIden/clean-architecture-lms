################
# STAGE: BUILD #
################

FROM python:3.12 as builder

LABEL org.opencontainers.image.authors="Roman Morozkin <romasa464@gmail.com>"

# INSTAL SYSTEM DEPENDENCIES
RUN apt-get clean -y \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends  \
      apt-transport-https=2.\* \
      build-essential=12.9 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install
COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry==1.8.3 && poetry install


################
# STAGE: FINAL #
################

FROM python:3.12-slim as final

COPY --from=builder /install /usr/local
COPY .. /app

WORKDIR /app

RUN apt-get clean -y \
  && apt-get update -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && addgroup --gid 1000 editorconfig \
  && adduser \
    --uid 1000 \
    --home /home/editorconfig \
    --shell /bin/sh \
    --ingroup editorconfig \
    --disabled-password \
    romasa464\
  && chown -R 1000:1000 /app

USER romasa464

EXPOSE 5050
