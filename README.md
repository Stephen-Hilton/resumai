# ResumAI Dohickey 🚀

**Automated Job Application System with AI-Powered Resume Tailoring**

ResumAI is a complete job application automation system that fetches jobs from LinkedIn alerts, generates tailored resumes using AI, creates professional PDFs, and helps you track applications through your entire job search journey.

## ✨ Features

- 📧 **Automatic Job Collection**: Fetch jobs from Gmail LinkedIn alerts
- 🧠 **AI-Powered Tailoring**: Use OpenAI to customize resumes for each job
- 📄 **Document Generation**: Create professional HTML and PDF resumes
- 🎯 **Application Tracking**: Manage jobs through 8 phases (Queued → Accepted)
- 🌐 **Web Dashboard**: Real-time interface with WebSocket updates
- ⚡ **Batch Processing**: Process multiple jobs simultaneously
- 🔄 **Error Recovery**: Automatic retry with detailed error reporting
- ☁️ **Cloud Storage**: Optional S3 integration for documents
- 📊 **Analytics**: Track statistics and monitor progress

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright for PDF generation
playwright install chromium
```

### Configuration

Create `.env` file:

```bash
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
OPENAI_API_KEY=sk-...
```

### Run

```bash
# Start web server
python src/ui/app.py

# Access dashboard
open http://localhost:5000
```

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)**: Complete usage instructions
- **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)**: Technical details and architecture
- **[PROJECT_DESIGN.md](PROJECT_DESIGN.md)**: System design and requirements

## 🎯 Workflow

```
1. Fetch Jobs → 2. Generate Content → 3. Create Documents → 4. Apply → Track
   (Gmail)         (AI/Static)           (HTML/PDF)         (Manual)  (Phases)
```

### Job Phases

1. **Queued**: New jobs ready for processing
2. **Data Generated**: Tailored content created
3. **Docs Generated**: PDFs ready to send
4. **Applied**: Application submitted
5. **Follow Up**: Awaiting response
6. **Interviewing**: In interview process
7. **Negotiating**: Discussing offer
8. **Accepted**: Offer accepted! 🎉

## 🖥️ Dashboard

![Dashboard Features](https://via.placeholder.com/800x400?text=ResumAI+Dashboard)

- **Resume Selector**: Choose which resume to use
- **Action Buttons**: Fetch jobs, add URLs, manual entry
- **Phase Sidebar**: Filter jobs by phase
- **Job Cards**: Interactive cards with phase-specific actions
- **Live Logs**: Real-time system activity

## 🧪 Testing

All 31 tests passing ✅

```bash
# Run all tests
python -m pytest tests/test_properties.py test_e2e_workflow.py test_flask_app.py -v

# Property tests (16)
python -m pytest tests/test_properties.py -v

# End-to-end test (1)
python -m pytest test_e2e_workflow.py -v

# Flask API tests (14)
python -m pytest test_flask_app.py -v
```

## 🏗️ Architecture

### Event-Driven System

- **40+ Events**: Modular async handlers for all operations
- **Event Bus**: Discovers and executes events with retry logic
- **Type-Safe**: Pydantic models for data validation
- **Tested**: Property-based + end-to-end + API tests

### Tech Stack

- **Backend**: Python 3.11+, asyncio
- **Web**: Flask, Flask-SocketIO, WebSockets
- **AI**: OpenAI GPT-4
- **Documents**: Playwright (PDF), Jinja2 (HTML)
- **Storage**: Local filesystem + optional S3
- **Testing**: pytest, hypothesis (property-based)

## 📊 System Capabilities

✅ Fetch jobs from Gmail LinkedIn alerts  
✅ Parse full job descriptions from LinkedIn  
✅ Generate tailored resume content (AI or static)  
✅ Create professional HTML and PDF documents  
✅ Track applications through 8 phases  
✅ Handle errors with automatic retry  
✅ Upload documents to S3 (optional)  
✅ Real-time web dashboard with WebSocket  
✅ Batch processing for multiple jobs  
✅ Log rotation and compression  
✅ Folder name validation  

## 🔧 API Endpoints

```bash
GET  /api/jobs              # List all jobs
GET  /api/job/{id}          # Get job details
POST /api/generate_data     # Generate content
POST /api/generate_docs     # Create documents
POST /api/move_phase        # Move between phases
POST /api/batch_process     # Process all jobs
POST /api/fetch_email       # Fetch from Gmail
GET  /api/logs              # View logs
GET  /api/job_stats         # Get statistics
```

## 📁 Project Structure

```
resumai/
├── src/
│   ├── events/          # 40+ event handlers
│   ├── lib/             # Utilities and types
│   ├── ui/              # Flask web app
│   │   ├── templates/   # HTML templates
│   │   └── static/      # CSS and JavaScript
│   └── templates/       # Job/resume templates
├── jobs/                # Job folders by phase
├── resumes/             # Resume YAML files
├── tests/               # Test suite
└── requirements.txt     # Dependencies
```

## 🎨 Customization

### Resume Sections

Customize any section:
- Contacts
- Summary
- Skills
- Highlights
- Experience
- Education
- Awards
- Cover Letter

### Generation Modes

Choose per section:
- **🧠 LLM**: AI-tailored to job description
- **⚙️ Static**: Direct copy from resume

### Custom Prompts

Edit `src/lib/prompts.py` to customize AI behavior.

## 🔒 Security

- Environment variables for secrets
- Input validation on all endpoints
- Path sanitization
- CORS configuration
- No hardcoded credentials

## 📈 Performance

- Async event execution
- Parallel processing where possible
- Efficient file I/O
- WebSocket for real-time updates
- Compressed log storage

## 🐛 Troubleshooting

### Gmail Issues
- Enable 2FA and use App Password
- Check IMAP is enabled

### OpenAI Issues
- Verify API key
- Check rate limits
- Use static generation as fallback

### PDF Issues
- Install Playwright: `playwright install chromium`
- Ensure HTML exists before PDF

See [USER_GUIDE.md](USER_GUIDE.md) for detailed troubleshooting.

## 📝 Requirements

- Python 3.11+
- Gmail account with IMAP
- OpenAI API key
- Playwright (for PDFs)
- Optional: AWS S3 bucket

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🎯 Use Cases

- **Active Job Seekers**: Automate application process
- **Passive Candidates**: Track opportunities
- **Career Changers**: Tailor resumes for different roles
- **Recruiters**: Manage candidate applications

## 🌟 Highlights

- **Complete System**: End-to-end automation
- **Production Ready**: Fully tested and documented
- **User Friendly**: Intuitive web interface
- **Extensible**: Event-driven architecture
- **Reliable**: Error handling and retry logic
- **Fast**: Batch processing and async execution

## 📞 Support

- Read [USER_GUIDE.md](USER_GUIDE.md) for usage
- Check [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for technical details
- Review logs in `src/logs/` for debugging
- Check `error.md` files in job folders for specific issues

## 🎉 Status

**✅ ALL TASKS COMPLETE**

- 32/32 tasks implemented
- 31/31 tests passing
- Full documentation
- Production ready

---

**Made with ❤️ for job seekers everywhere**

*Good luck with your job search!* 🚀
