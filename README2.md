# 🚀 Edu.ai - AI-Powered Programming Education Platform

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Azure](https://img.shields.io/badge/Azure-Powered-blue)
![AI](https://img.shields.io/badge/AI-GPT--4.1-purple)

## 📖 Overview

**Edu.ai** is an innovative AI-powered educational platform designed to teach programming to children aged 6-18. The platform leverages cutting-edge Azure services to deliver personalized, interactive learning experiences through AI-driven avatars and intelligent content generation.

![Edu.ai Platform](https://via.placeholder.com/800x400/0066cc/ffffff?text=Edu.ai+Platform+Preview)

## ✨ Key Features

### 🎯 Personalized Learning
- **AI-Powered Content Generation**: Dynamic lesson creation using GPT-4.1
- **Adaptive Learning Paths**: Tailored curriculum based on individual progress
- **Multi-Age Support**: Content suitable for ages 6-18

### 🎭 Interactive Avatar System
- **Animated Teaching Characters**: Engaging avatars with lip-sync technology
- **Voice Narration**: Natural text-to-speech with multiple language support
- **Gesture Recognition**: Interactive responses to student engagement

### 🔍 Smart Q&A System
- **"Raise Hand" Feature**: Interactive question submission
- **Real-time AI Responses**: Intelligent answers using RAG technology
- **Context-Aware Help**: Responses based on current lesson content

### 📊 Progress Tracking
- **Learning Analytics**: Comprehensive progress monitoring
- **Performance Insights**: Detailed reports for educators and parents
- **Gamification**: Achievement badges and progress rewards

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Services   │
│                 │    │                 │    │                 │
│ • React/HTML    │◄──►│ • FastAPI       │◄──►│ • Azure OpenAI  │
│ • CSS/JavaScript│    │ • Azure Functions│    │ • GPT-4.1       │
│ • Static Web App│    │ • REST APIs     │    │ • Azure AI Search│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Hosting       │    │   Database      │    │   Media Services │
│                 │    │                 │    │                 │
│ • Azure Static  │    │ • Azure Cosmos  │    │ • Azure Speech  │
│   Web Apps      │    │   DB            │    │ • TTS Avatar    │
│ • CDN           │    │ • Document Store│    │ • Audio Controls│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3/JavaScript**: Core web technologies
- **React.js**: Modern UI framework
- **Azure Static Web Apps**: Hosting and deployment

### Backend
- **FastAPI**: High-performance Python API framework
- **Azure Functions**: Serverless compute
- **Azure Cosmos DB**: NoSQL database

### AI & ML
- **Azure OpenAI Service**: GPT-4.1 integration
- **Azure AI Search**: RAG implementation
- **Azure Speech Services**: Text-to-speech
- **Azure TTS Avatar**: Animated characters

### DevOps
- **GitHub Actions**: CI/CD pipeline
- **Azure Monitor**: Application monitoring
- **Azure Key Vault**: Secrets management

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- Azure subscription
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/edu.ai.git
   cd edu.ai
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

5. **Run the application**
   ```bash
   # Frontend (Terminal 1)
   cd frontend
   npm start

   # Backend (Terminal 2)
   cd backend
   uvicorn app.main:app --reload
   ```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=your_openai_endpoint

# Azure Cosmos DB
COSMOS_DB_CONNECTION_STRING=your_cosmos_connection

# Azure Speech Services
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_speech_region

# Azure AI Search
AZURE_SEARCH_ENDPOINT=your_search_endpoint
AZURE_SEARCH_KEY=your_search_key
```

## 📅 Development Roadmap

### 📊 8-Week Sprint Plan

| Sprint | Week | Focus | Key Deliverables |
|--------|------|-------|------------------|
| 🎨 **Sprint 1** | Jul 12-18 | UI Design & Setup | Figma prototypes, Azure environment |
| 💻 **Sprint 2** | Jul 19-25 | Frontend Development | Working UI, navigation system |
| 🔧 **Sprint 3** | Jul 26-Aug 1 | Backend & Database | API endpoints, database schema |
| 🔍 **Sprint 4** | Aug 2-8 | RAG Implementation | Knowledge base, search functionality |
| 🤖 **Sprint 5** | Aug 9-15 | GPT-4.1 Integration | AI content generation, lesson templates |
| 🎭 **Sprint 6** | Aug 16-22 | Avatar & TTS | Voice narration, animated characters |
| 🙋 **Sprint 7** | Aug 23-29 | Interactive Features | Q&A system, analytics dashboard |
| 🚀 **Sprint 8** | Aug 30-Sep 5 | Testing & Launch | Production deployment, monitoring |

## 💰 Cost Management

### Monthly Budget Breakdown (Target: $150/month)

- **Azure Static Web Apps**: $9/month
- **Azure Functions**: $25/month
- **Azure Cosmos DB**: $35/month
- **Azure OpenAI (GPT-4.1)**: $40/month
- **Azure AI Search**: $15/month
- **Azure Speech Services**: $15/month
- **Azure TTS Avatar**: $8/month
- **Data Transfer**: $3/month

**Total Estimated Cost**: $150/month

## 🔒 Privacy & Compliance

### COPPA Compliance
- **Age Verification**: Parental consent for users under 13
- **Data Minimization**: Collect only necessary information
- **Secure Storage**: Encrypted data with retention policies
- **Transparency**: Clear privacy policies and opt-out options

### Security Measures
- **Azure AD Integration**: Secure authentication
- **Data Encryption**: End-to-end encryption
- **Regular Audits**: Security assessments and penetration testing
- **Compliance Monitoring**: GDPR and FERPA compliance

## 📈 Performance Metrics

### Technical KPIs
- **System Uptime**: >99.5%
- **Response Time**: <2 seconds
- **AI Accuracy**: >85%
- **User Engagement**: >10 minutes/session

### Educational KPIs
- **User Satisfaction**: >4.0/5.0
- **Course Completion**: >60%
- **Question Accuracy**: >90%
- **Multi-language Usage**: >20%

## 🧪 Testing

### Running Tests
```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Load testing
python -m pytest tests/load/
```

### Test Coverage
- **Unit Tests**: 90%+ coverage
- **Integration Tests**: All API endpoints
- **End-to-End Tests**: Critical user journeys
- **Performance Tests**: Load testing for 100+ concurrent users

## 🚢 Deployment

### Development Environment
```bash
# Deploy to dev environment
az staticwebapp create \
  --name edu-ai-dev \
  --resource-group edu-ai-rg \
  --source https://github.com/your-org/edu.ai \
  --branch develop
```

### Production Deployment
1. **Push to main branch** → Triggers CI/CD pipeline
2. **Azure Static Web Apps** → Deploys frontend automatically
3. **Azure Functions** → Deploys backend from `/api` folder
4. **Environment Variables** → Configure in Azure Portal

### Monitoring
- **Azure Monitor**: Application insights and logging
- **Azure Application Insights**: Performance monitoring
- **Cost Alerts**: Budget monitoring and alerts
- **Security Alerts**: Threat detection and response

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- **ESLint**: Frontend code linting
- **Black**: Python code formatting
- **Prettier**: Code formatting
- **Pre-commit hooks**: Automated quality checks

## 📞 Support

### Getting Help
- **Documentation**: [Wiki](https://github.com/your-org/edu.ai/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-org/edu.ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/edu.ai/discussions)
- **Email**: support@edu.ai

### Community
- **Discord**: [Join our community](https://discord.gg/edu-ai)
- **Twitter**: [@EduAI_Platform](https://twitter.com/EduAI_Platform)
- **LinkedIn**: [Edu.ai Company Page](https://linkedin.com/company/edu-ai)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Microsoft Azure**: For providing the cloud infrastructure
- **OpenAI**: For the powerful GPT-4.1 language model
- **Our Contributors**: For their valuable contributions
- **The Open Source Community**: For inspiration and support

---

**Made with ❤️ by the Edu.ai Team**

*Empowering the next generation of programmers through AI-powered education*

![Footer](https://via.placeholder.com/800x100/f0f0f0/666666?text=Edu.ai+%7C+Building+the+Future+of+Education)