# Streamlit Cloud Deployment Guide

## 🚀 Deployment Steps

### 1. **Prepare Your Repository**
Make sure your repository contains:
- `app.py` (main application file)
- `requirements.txt` (dependencies)
- `.streamlit/config.toml` (optional configuration)

### 2. **Deploy to Streamlit Cloud**

#### Option A: Using requirements.txt (Recommended)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set the main file path to: `app.py`
4. Streamlit will automatically detect `requirements.txt`

#### Option B: If requirements.txt fails, try requirements-simple.txt
1. Rename `requirements-simple.txt` to `requirements.txt`
2. Commit and push to your repository
3. Redeploy on Streamlit Cloud

### 3. **Common Issues and Solutions**

#### Issue: Prophet installation fails
**Solution**: Use the simplified requirements or add these to packages.txt:
```
build-essential
libgomp1
```

#### Issue: XGBoost installation fails
**Solution**: The simplified requirements.txt uses XGBoost 1.7.6 which is more stable

#### Issue: Memory issues
**Solution**: 
- Reduce the number of properties generated
- Optimize the ML models
- Use smaller datasets

### 4. **Alternative Deployment Options**

#### If Streamlit Cloud continues to fail:
1. **Heroku**: Use the provided requirements.txt
2. **Railway**: Works well with Python apps
3. **Render**: Good alternative to Streamlit Cloud
4. **Local deployment**: Run `streamlit run app.py`

### 5. **Testing Locally**
Before deploying, test locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 6. **Environment Variables (if needed)**
If you need environment variables, add them in Streamlit Cloud settings:
- No sensitive data should be hardcoded
- Use Streamlit secrets for API keys

## 🔧 Troubleshooting

### Dependencies Installation Issues:
1. **Try the simplified requirements first**
2. **Check Python version compatibility** (Streamlit Cloud uses Python 3.9+)
3. **Remove problematic packages temporarily** and add them back one by one

### Memory Issues:
1. **Reduce data generation** in the app
2. **Optimize ML model training**
3. **Use smaller datasets**

### Build Timeout:
1. **Use lighter dependencies**
2. **Pre-compile models** if possible
3. **Optimize import statements**

## 📝 Notes
- Streamlit Cloud has a 1GB memory limit
- Build time is limited to 10 minutes
- Some ML libraries can be resource-intensive
- Consider using lighter alternatives for production

## 🆘 If All Else Fails
Use the minimal requirements:
```
streamlit
pandas
numpy
plotly
streamlit-option-menu
faker
reportlab
```

And gradually add back the ML libraries one by one to identify the problematic dependency.

