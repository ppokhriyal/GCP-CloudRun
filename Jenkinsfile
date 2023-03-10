pipeline {
	agent any
	environment {
		GCP_PROJECT_ID = "jenkins-lab-376212"
		GCP_SERVICE_ACCOUNT_EMAIL = "jenkins-gcloud@jenkins-lab-376212.iam.gserviceaccount.com"
		GCP_ARTIFACT_REG = "flask-app-arti-reg"
	}
	stages {
		stage("GCLOUD Version check") {	
			steps {
				sh '''
					gcloud version
				 '''
			}
		}
		stage("Set GCP Project") {
			steps {
				withCredentials([file(credentialsId: 'gcloud-creds', variable: 'GCLOUD_SECRET')]) {
					sh '''
						gcloud auth activate-service-account --key-file="$GCLOUD_SECRET"
						gcloud config set project "$GCP_PROJECT_ID"
					'''
				}
			}
		}
		stage("Create Artifact Registry") {
			steps {
				sh '''
					gcloud artifacts repositories create "$GCP_ARTIFACT_REG" --location us-central1 --repository-format=docker
				 '''
			}
		}
		stage("Create Docker image") {
			steps {
				sh ''' 
					docker build -t us-central1-docker.pkg.dev/"$GCP_PROJECT_ID"/"$GCP_ARTIFACT_REG"/webapp:v1 .
				'''
			}
		}
		stage("Push Docker image to GCP Artifcat Registry"){
			steps{
				sh '''
					echo Y | gcloud auth configure-docker us-central1-docker.pkg.dev
					docker push us-central1-docker.pkg.dev/"$GCP_PROJECT_ID"/"$GCP_ARTIFACT_REG"/webapp:v1
				 '''
			}
		}
		stage("Deploy Cloud Run Container"){
			steps{
				sh '''
					gcloud run deploy mywebapp --max-instances=5 --min-instances=1 --region=us-central1 --allow-unauthenticated --image us-central1-docker.pkg.dev/"$GCP_PROJECT_ID"/"$GCP_ARTIFACT_REG"/webapp:v1
				 '''
			}
		}
	}
}
