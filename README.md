# Agent Development Kit (ADK) Hackathon Corporate Professional Development Agent #adkhackathon

Hey! I'm [Balint Kubik](https://www.linkedin.com/in/balintkubik/). Welcome to the GitHub repository of my submission to the [Agent Development Kit Hackathon with Google Cloud](https://googlecloudmultiagents.devpost.com/)!

This project implements a sophisticated multi-agent system for **corporate professional development** using [Google Cloud's Agent Development Kit (ADK)](https://google.github.io/adk-docs/). The system demonstrates **automation of complex business processes** through collaborative AI agents with Google ADK.

## Core Components

### 1. Intent Detection Agent
- Acts as the system's orchestrator
- Analyzes user queries to determine the appropriate agent for handling the request
- Routes queries to specialized agents based on intent classification

### 2. Employee Development Agents
- **Employee Profile Agent**: Manages employee information and skills
- **Training History & Budget Agent**: Tracks training history and budget utilization
- **Training Finder Agent**: Identifies relevant training opportunities
- **Training Registerer Agent**: Handles training registration and approvals
- **Skills Development Agent**: Provides personalized skills development recommendations

### 3. Company Information Agents
- **Professional Development Policy Agent**: Explains company policies and guidelines
- **Company Information Agent**: Provides general company information and resources

## Key Features

1. **Intelligent Process Automation**
   - Automated training registration workflow
   - Budget tracking and management
   - Skills assessment and development planning

2. **Data-Driven Insights**
   - Training history analysis
   - Budget utilization tracking
   - Skills gap identification
   - Personalized development recommendations

3. **Natural Language Interaction**
   - Conversational interface for all operations
   - Context-aware responses
   - Multi-turn conversations for complex tasks

4. **Integration with Google Cloud Services**
   - BigQuery for data storage and analytics
   - Vertex AI Search for document retrieval
   - Cloud Storage for document management

## Technical Implementation

The system leverages:
- Google's [Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
- [Google BigQuery](https://cloud.google.com/bigquery?hl=en) for structured data management
- [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction) for document search and retrieval
- [Google Cloud Storage](https://cloud.google.com/storage?hl=en) for document storage
- [Google Gemini](https://ai.google.dev/gemini-api/docs) for natural language understanding and intelligence

## Use Cases

1. **Employee Development**
   - Training registration and tracking
   - Budget management
   - Skills development planning

2. **HR Operations**
   - Policy clarification
   - Training program management
   - Employee development tracking

3. **Management Support**
   - Team skills assessment
   - Training budget oversight
   - Development program monitoring

This implementation aligns with the hackathon's focus on building multi-agent systems that automate complex processes and provide intelligent data analysis, while maintaining a strong emphasis on practical business applications.

## Example prompts
- How can I improve my current skills? My email is: priya.sharma@amazincorp.com
- Please find me a training that helps me develop my current skills. My email is priya.sharma@amazincorp.com
- What skills should I learn to serve our existing and future customers better? My email is priya.sharma@amazincorp.com
- How much training budget do I have left? My email is priya.sharma@amazincorp.com
- I am interested in learning Spanish as foreign language. Does our corporate professional development policy allow for that?

## Running it locally

### Prerequisites

#### Pass environment variables
Make sure to customize the contents of [`adk_hackathon_professional_development_agent/.env`](adk_hackathon_professional_development_agent/.env) so that the application will use the correct environment variables.

You can also set the environment variables in your local session by running:
```bash
set -a                                                    
source adk_hackathon_professional_development_agent/.env
set +a
```

#### Install Python dependencies

##### Install Poetry
[Poetry](https://python-poetry.org/) is used for Python dependency management.

Follow [the official instructions](https://python-poetry.org/) to install Poetry.

##### Install dependencies with Poetry
Run the below command:
```bash
poetry install
```

#### Google Cloud project
![Google Cloud logo](https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Google_Cloud_logo.svg/2560px-Google_Cloud_logo.svg.png)

Make sure to create/have a Google Cloud project and that you know its project ID.

#### Google Cloud CLI (`gcloud`)
Make sure to install the Google Cloud CLI tool called `gcloud`. Installation instructions [here](https://cloud.google.com/sdk/docs/install).

Once you've successfully installed `gcloud`, make sure to login using the below command:

```bash
gcloud auth application-default login
```

Set the default project using:
```bash
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

Set the default quota project using:
```bash
gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
```

### Enable necessary Google Cloud APIs
```bash
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable discoveryengine.googleapis.com
```

#### Google BigQuery
![Google BigQuery logo](https://syncari.com/wp-content/uploads/2021/03/Google-Big-Query.png)

Since multiple agents use [Google BigQuery](https://cloud.google.com/bigquery?hl=en), Google Cloud's serverless enterprise data warehouse, to store and access data, you'll need to load some initial data there.

##### Create dataset
First, we need to create the Google BigQuery dataset.

```bash
bq --location=$GOOGLE_CLOUD_LOCATION mk \
    --dataset $GOOGLE_CLOUD_PROJECT:$BIGQUERY_DATASET_ID
```

##### Load input data
Secondly, let's load the CSV files under [`input_data/bigquery`](input_data/bigquery/) into separate tables using the below commands:

```bash
bq load \
    --source_format=CSV \
    --field_delimiter='|' \
    --skip_leading_rows=1 \
    $GOOGLE_CLOUD_PROJECT:$BIGQUERY_DATASET_ID.employee_profiles \
    input_data/bigquery/employee_profiles.csv \
    name:STRING,email:STRING,department:STRING,role:STRING,skills:STRING

bq load \
    --source_format=CSV \
    --field_delimiter='|' \
    --skip_leading_rows=1 \
    $GOOGLE_CLOUD_PROJECT:$BIGQUERY_DATASET_ID.employee_trainings \
    input_data/bigquery/employee_trainings.csv \
    email:STRING,name:STRING,description:STRING,skills:STRING,date:DATE,cost_usd:FLOAT,url:STRING

bq load \
    --source_format=CSV \
    --field_delimiter='|' \
    --skip_leading_rows=1 \
    $GOOGLE_CLOUD_PROJECT:$BIGQUERY_DATASET_ID.project_portfolio \
    input_data/bigquery/project_portfolio.csv \
    name:STRING,customer:STRING,customer_profile:STRING,customer_location:STRING,description:STRING,skills_needed:STRING,status:STRING
```

#### Google Cloud Storage
![Google Cloud Storage logo](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT14eINB-AaTBCsGDf2vKnG73RCWAxVaw2t0A&s)

[Google Cloud Storage](https://cloud.google.com/storage?hl=en), Google Cloud's object storage service, is used to store the PDF files stored in [input_data/vertex_ai_search](input_data/vertex_ai_search/). These PDF files on GCS will be later exposed to the agents through Vertex AI Search data stores.

##### Create bucket
```bash
gcloud storage buckets create gs://$VERTEX_AI_SEARCH_DATA_STORE_BUCKET --location=$GOOGLE_CLOUD_LOCATION
```

##### Upload files
```bash
gsutil -m cp -r input_data/vertex_ai_search/** gs://$VERTEX_AI_SEARCH_DATA_STORE_BUCKET/
```

#### Vertex AI Search data store
![Vertex AI logo](https://miro.medium.com/v2/resize:fit:1400/1*6Qe6HxbxDsnrxlpgz5BGIA.png)

As mentioned before, the PDFs uploaded to GCS will be used by the agents using a Vertex AI Search data store. [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction) enables users to build Google-quality search apps on users' own data.

Run the below script to create the data store and load the GCS files.

```bash
poetry run python adk_hackathon_professional_development_agent/create_vertex_ai_search_data_store.py
```

#### Run it
```bash
poetry run adk web
```

Navigate to `localhost:8000`.

## Testing

The agent includes a comprehensive test suite that verifies its behavior across different scenarios:

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run specific test scenarios
poetry run pytest tests/improve_current_skills.test.json  # Test skills improvement recommendations
poetry run pytest tests/improve_future_skills.test.json   # Test future skills development
poetry run pytest tests/training_budget.test.json         # Test budget inquiries
poetry run pytest tests/professional_development_policy_question.test.json  # Test policy interpretations
```

### Test Scenarios
The test suite covers key user interactions:
- Skills improvement recommendations
- Future skills development planning
- Training budget inquiries
- Professional development policy questions
- Input validation (e.g., queries without email)

## Deployment

### Deploy to Cloud Run
The agent can be deployed to [Cloud Run](https://cloud.google.com/run?hl=en), a fully managed platform of Google Cloud that enables you to run your code directly on top of Google's scalable infrastructure.

Run the below command:
```bash
gcloud run deploy $SERVICE_NAME \
   --source . \
   --region $GOOGLE_CLOUD_LOCATION \
   --project $GOOGLE_CLOUD_PROJECT \
   --allow-unauthenticated \
   --max-instances 1 \
   --cpu 4 \
   --memory 8Gi \
   --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI,BIGQUERY_DATASET_ID=$BIGQUERY_DATASET_ID,VERTEX_AI_SEARCH_DATA_STORE_LOCATION=$VERTEX_AI_SEARCH_DATA_STORE_LOCATION,VERTEX_AI_SEARCH_DATA_STORE_BUCKET=$VERTEX_AI_SEARCH_DATA_STORE_BUCKET,VERTEX_AI_SEARCH_DATA_STORE_ID=$VERTEX_AI_SEARCH_DATA_STORE_ID,VERTEX_AI_STAGING_BUCKET=$VERTEX_AI_STAGING_BUCKET"
```

### Deploy to Vertex AI Agent Engine
We can deploy the agent to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview), a set of services in Google Cloud that enables developers to deploy, manage, and scale AI agents in production.

#### Create Google Cloud Storage staging bucket
gcloud storage buckets create gs://$VERTEX_AI_SEARCH_DATA_STORE_BUCKET --location=$GOOGLE_CLOUD_LOCATION

#### Run the deployment script
```bash
poetry run python adk_hackathon_professional_development_agent/deploy_to_vertex_ai_agent_engine.py
```
