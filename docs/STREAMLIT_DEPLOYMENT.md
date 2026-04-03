# Streamlit Deployment Guide

**Version**: 0.5.0  
**Last Updated**: 2026-04-03

---

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# Access in browser
# http://localhost:8501
```

### Streamlit Cloud (Recommended)

**Step 1: Push to GitHub**

```bash
cd agent-monte-carlo
git init
git add .
git commit -m "feat: Add Streamlit deployment support"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agent-monte-carlo.git
git push -u origin main
```

**Step 2: Connect to Streamlit Cloud**

1. Visit https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `agent-monte-carlo`
5. Main file path: `app.py`
6. Python version: 3.11
7. Click "Deploy!"

**Step 3: Share Your App**

Your app will be live at:
```
https://YOUR_USERNAME-agent-monte-carlo-app-abc123.streamlit.app/
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t agent-monte-carlo:streamlit .
```

### Run Container

```bash
docker run -d \
  -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  agent-monte-carlo:streamlit
```

### Access

```
http://localhost:8501
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAMLIT_SERVER_PORT` | 8501 | Server port |
| `STREAMLIT_SERVER_ADDRESS` | localhost | Server address |
| `STREAMLIT_THEME_PRIMARY_COLOR` | #3498db | Primary theme color |

### Custom Configuration

Create `.streamlit/secrets.toml` for sensitive data:

```toml
[api_keys]
yahoo_finance = "your_api_key"
```

Access in app:
```python
import streamlit as st
api_key = st.secrets["api_keys"]["yahoo_finance"]
```

---

## 📊 App Features

### Tabs

1. **📊 Overview**: Project introduction, key metrics, quick start
2. **🏗️ Architecture**: Interactive system architecture diagram
3. **📈 Results**: Tail risk metrics comparison with empirical data
4. **⚡ Performance**: Computational benchmarks and hardware specs
5. **🗺️ Roadmap**: Project timeline and milestones

### Interactive Elements

- Real-time metric displays
- SVG chart rendering
- Code snippets with syntax highlighting
- Responsive layout

---

## 🔧 Troubleshooting

### Issue: Charts Not Displaying

**Solution**: Ensure SVG files exist in `docs/images/`:
```bash
ls docs/images/*.svg
```

### Issue: Port Already in Use

**Solution**: Use different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow Loading

**Solution**: Enable caching:
```python
@st.cache_data
def load_chart(chart_name: str):
    # Load and return chart
```

---

## 📈 Performance Optimization

### Caching

```python
@st.cache_data
def load_svg_chart(chart_name: str) -> str:
    """Cached SVG loading."""
    chart_path = Path(__file__).parent / "docs" / "images" / chart_name
    return chart_path.read_text(encoding='utf-8')
```

### Lazy Loading

Load charts only when tab is selected:
```python
if selected_tab == "Architecture":
    svg_content = load_svg_chart("architecture.svg")
```

---

## 🔒 Security

### Best Practices

1. **No hardcoded secrets** - Use `.streamlit/secrets.toml`
2. **Enable XSRF protection** - Default in config.toml
3. **CORS disabled** - For production, set allowed origins
4. **Input validation** - Validate all user inputs

### Production Checklist

- [ ] Enable HTTPS (Streamlit Cloud provides this)
- [ ] Set strong passwords if authentication needed
- [ ] Limit access to authorized users
- [ ] Monitor usage and errors
- [ ] Regular dependency updates

---

## 📊 Analytics

### Streamlit Cloud Analytics

Streamlit Cloud provides:
- User visits
- App performance
- Error tracking

### Self-Hosted Analytics

Add Google Analytics:

```python
st.components.v1.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
""", height=0)
```

---

## 🎯 Next Steps

### Phase 2 Enhancements

1. **Interactive Simulations**: Run actual Monte Carlo simulations from UI
2. **Parameter Tuning**: Sliders for n_simulations, confidence_level, etc.
3. **Real-time Charts**: Plotly interactive visualizations
4. **Data Upload**: Allow users to upload their own data
5. **Export Results**: Download simulation results as CSV/JSON

### Phase 3 Enhancements

1. **User Authentication**: Multi-user support
2. **API Integration**: REST API for programmatic access
3. **Batch Processing**: Queue system for large simulations
4. **GPU Acceleration**: Optional GPU backend

---

## 📞 Support

- **Issues**: https://github.com/YOUR_USERNAME/agent-monte-carlo/issues
- **Discussions**: https://github.com/YOUR_USERNAME/agent-monte-carlo/discussions
- **Documentation**: https://agent-monte-carlo.readthedocs.io

---

**Deployed with ❤️ using Streamlit**
