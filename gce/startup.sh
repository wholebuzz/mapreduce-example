#!/usr/bin/env bash
set -x

# get image name and container parameters from the metadata
IMAGE_NAME=$(curl --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/image_name -H "Metadata-Flavor: Google" || echo "")

CONTAINER_FLAGS=$(curl --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/container_flags -H "Metadata-Flavor: Google" || echo "")

CONTAINER_PARAM=$(curl --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/container_param -H "Metadata-Flavor: Google" || echo "")

DB_PARAM=$(curl --fail http://metadata.google.internal/computeMetadata/v1/instance/attributes/db_param -H "Metadata-Flavor: Google" || echo "")

# This is needed if you are using a private images in GCP Container Registry
# (possibly also for the gcp log driver?)
sudo HOME=/home/root /usr/bin/docker-credential-gcr configure-docker

sudo mkdir /mnt/stateful_partition/cloudsql
sudo chmod a+w /mnt/stateful_partition/cloudsql

# Start a cloud sql proxy to provide database acces
if ![ -z $DB_PARAM ]; then
  sudo HOME=/home/root docker run -d --log-driver=gcplogs \
    -v /mnt/stateful_partition/cloudsql:/cloudsql \
    gcr.io/cloudsql-docker/gce-proxy:1.21.0 /cloud_sql_proxy -dir=/cloudsql \
    -instances=$DB_PARAM
fi

# Run! The logs will go to stack driver 
sudo HOME=/home/root docker run \
  -v /mnt/stateful_partition/cloudsql:/cloudsql \
  ${CONTAINER_FLAGS} --log-driver=gcplogs ${IMAGE_NAME} ${CONTAINER_PARAM}

# Get the zone
zoneMetadata=$(curl "http://metadata.google.internal/computeMetadata/v1/instance/zone" -H "Metadata-Flavor:Google")
# Split on / and get the 4th element to get the actual zone name
IFS=$'/'
zoneMetadataSplit=($zoneMetadata)
ZONE="${zoneMetadataSplit[3]}"

# Run compute delete on the current instance. Need to run in a container 
# because COS machines don't come with gcloud installed 
docker run --entrypoint "gcloud" google/cloud-sdk:alpine compute instances delete ${HOSTNAME}  --delete-disks=all --zone=${ZONE}

