#!/bin/bash
# BRAINBLUE URBAIN - Deployment Script
# This script handles deployment to various platforms

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================="
echo "BRAINBLUE URBAIN - Deployment"
echo "==================================${NC}"

# Check arguments
if [ -z "$1" ]; then
  echo -e "${RED}Usage: ./deploy.sh <platform> [environment]${NC}"
  echo "Platforms: docker, heroku, aws, digitalocean, local"
  echo "Environment: development, staging, production"
  exit 1
fi

PLATFORM=$1
ENVIRONMENT=${2:-production}

echo -e "${BLUE}Platform: $PLATFORM${NC}"
echo -e "${BLUE}Environment: $ENVIRONMENT${NC}"

# Function to deploy to Docker
deploy_docker() {
  echo -e "${BLUE}🐳 Deploying with Docker...${NC}"
  
  docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml build
  docker-compose -f docker-compose.yml -f docker-compose.$ENVIRONMENT.yml up -d
  
  echo -e "${GREEN}✅ Docker deployment complete${NC}"
  echo "Service URLs:"
  echo "- Frontend: http://localhost"
  echo "- API: http://localhost:5000/api"
  echo "- Health: http://localhost:5000/api/health"
}

# Function to deploy to Heroku
deploy_heroku() {
  echo -e "${BLUE}🚀 Deploying to Heroku...${NC}"
  
  if ! command -v heroku &> /dev/null; then
    echo -e "${RED}Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli${NC}"
    exit 1
  fi
  
  # Login to Heroku
  heroku login
  
  # Create app if not exists
  APP_NAME="brainblue-urbain-$ENVIRONMENT"
  heroku create $APP_NAME --region eu || true
  
  # Set environment variables
  heroku config:set --app=$APP_NAME \
    FLASK_ENV=$ENVIRONMENT \
    DATABASE_URL="your-database-url-here" \
    REDIS_URL="your-redis-url-here" \
    JWT_SECRET_KEY="$(openssl rand -base64 32)" \
    SECRET_KEY="$(openssl rand -base64 32)"
  
  # Add PostgreSQL addon
  heroku addons:create heroku-postgresql:standard-0 --app=$APP_NAME || true
  
  # Add Redis addon
  heroku addons:create heroku-redis:premium-0 --app=$APP_NAME || true
  
  # Deploy
  git push heroku main
  
  # Run migrations
  heroku run python backend/migrate.py upgrade --app=$APP_NAME
  
  echo -e "${GREEN}✅ Heroku deployment complete${NC}"
  echo -e "App URL: ${BLUE}https://$APP_NAME.herokuapp.com${NC}"
}

# Function to deploy to AWS
deploy_aws() {
  echo -e "${BLUE}☁️  Deploying to AWS...${NC}"
  
  if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI not found. Install from: https://aws.amazon.com/cli/${NC}"
    exit 1
  fi
  
  # Build Docker image
  AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
  AWS_REGION=${AWS_REGION:-us-east-1}
  ECR_REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/brainblue-urbain"
  
  echo "AWS Account: $AWS_ACCOUNT_ID"
  echo "ECR Repository: $ECR_REPO"
  
  # Login to ECR
  aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ECR_REPO
  
  # Build and tag image
  docker build -t brainblue-urbain:latest .
  docker tag brainblue-urbain:latest $ECR_REPO:latest
  docker tag brainblue-urbain:latest $ECR_REPO:$ENVIRONMENT
  
  # Push to ECR
  docker push $ECR_REPO:latest
  docker push $ECR_REPO:$ENVIRONMENT
  
  echo -e "${GREEN}✅ AWS deployment complete${NC}"
  echo "Image pushed to: $ECR_REPO"
  echo "Next: Deploy to ECS, Elastic Beanstalk, or Kubernetes"
}

# Function to deploy to DigitalOcean
deploy_digitalocean() {
  echo -e "${BLUE}💧 Deploying to DigitalOcean...${NC}"
  
  if ! command -v doctl &> /dev/null; then
    echo -e "${RED}DigitalOcean CLI (doctl) not found. Install from: https://docs.digitalocean.com/reference/doctl/${NC}"
    exit 1
  fi
  
  # Build Docker image
  docker build -t brainblue-urbain:latest .
  
  # Tag for Docker Hub (or your registry)
  docker tag brainblue-urbain:latest your-registry/brainblue-urbain:latest
  docker push your-registry/brainblue-urbain:latest
  
  echo -e "${GREEN}✅ Docker image pushed${NC}"
  echo "Next: Deploy with App Platform or Kubernetes"
}

# Function to deploy locally
deploy_local() {
  echo -e "${BLUE}🖥️  Deploying locally...${NC}"
  
  # Install dependencies
  pip install -r requirements.txt
  
  # Run migrations
  python backend/migrate.py upgrade
  
  # Seed database if needed
  python backend/seeds.py || true
  
  # Start application
  gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
}

# Deploy based on platform
case $PLATFORM in
  docker)
    deploy_docker
    ;;
  heroku)
    deploy_heroku
    ;;
  aws)
    deploy_aws
    ;;
  digitalocean)
    deploy_digitalocean
    ;;
  local)
    deploy_local
    ;;
  *)
    echo -e "${RED}Unknown platform: $PLATFORM${NC}"
    exit 1
    ;;
esac

echo -e "${GREEN}✅ Deployment script completed!${NC}"
