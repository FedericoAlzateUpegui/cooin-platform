# Cooin Backend Testing Guide

This guide will help you test your Cooin backend API to ensure everything is working correctly.

## 🚀 Quick Start Testing

### Prerequisites
1. **Python 3.9+ installed**
2. **PostgreSQL running** with a database created
3. **Virtual environment activated** (recommended)

### Step 1: Set Up the Environment

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# 3. Run database migrations
alembic upgrade head
```

### Step 2: Start the Server

**Option A: Using the startup script**
```bash
python start_dev.py
```

**Option B: Manual start**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Test the API

**Option A: Automated Testing**
```bash
python test_api.py
```

**Option B: Manual Testing (Interactive Docs)**
Visit: http://localhost:8000/api/v1/docs

## 📋 What Gets Tested

### ✅ Authentication System
- ✅ User Registration
- ✅ User Login
- ✅ Token Refresh
- ✅ Get Current User
- ✅ Session Management
- ✅ User Logout

### ✅ Profile Management
- ✅ Create Profile
- ✅ Get My Profile
- ✅ Update Profile
- ✅ Profile Completion Status
- ✅ Search Public Profiles
- ✅ Financial Information Updates
- ✅ Lending/Borrowing Preferences

## 🔧 Testing Each Feature

### 1. Authentication Testing

**Register a New User:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "role": "borrower",
    "agree_to_terms": true
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

**Get Current User (requires token):**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. Profile Testing

**Create Profile:**
```bash
curl -X POST "http://localhost:8000/api/v1/profiles/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "display_name": "JohnD",
    "bio": "Looking for home improvement loan",
    "city": "San Francisco",
    "country": "United States"
  }'
```

**Get Profile Completion:**
```bash
curl -X GET "http://localhost:8000/api/v1/profiles/me/completion" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Search Profiles:**
```bash
curl -X GET "http://localhost:8000/api/v1/profiles/?role=lender&limit=10"
```

### 3. Financial Information

**Update Financial Info:**
```bash
curl -X PUT "http://localhost:8000/api/v1/profiles/me/financial" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "income_range": "75k_100k",
    "employment_status": "employed_full_time",
    "monthly_income": 8500.00
  }'
```

**Update Borrowing Preferences:**
```bash
curl -X PUT "http://localhost:8000/api/v1/profiles/me/borrowing" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "loan_purpose": "home_improvement",
    "requested_loan_amount": 25000.00,
    "preferred_loan_term": 60,
    "max_acceptable_rate": 8.5
  }'
```

## 🐛 Troubleshooting

### Common Issues and Solutions

**1. Database Connection Error**
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution:**
- Check PostgreSQL is running: `sudo service postgresql status`
- Verify database exists: `psql -h localhost -U postgres -l`
- Check DATABASE_URL in `.env` file

**2. Import Errors**
```
ModuleNotFoundError: No module named 'app'
```
**Solution:**
- Ensure you're in the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run from project root directory

**3. Migration Errors**
```
alembic.util.exc.CommandError: Target database is not up to date.
```
**Solution:**
- Run migrations: `alembic upgrade head`
- If issues persist: `alembic stamp head` then `alembic upgrade head`

**4. Token Validation Errors**
```
401 Unauthorized: Could not validate credentials
```
**Solution:**
- Check token format: `Bearer YOUR_TOKEN_HERE`
- Verify SECRET_KEY in `.env` matches what was used to create token
- Token may have expired - get a new one via login

**5. Profile Creation Errors**
```
400 Bad Request: Profile already exists for this user
```
**Solution:**
- User profiles are created automatically during registration
- Use PUT `/profiles/me` to update instead of POST to create

## 📊 Expected Test Results

When running `python test_api.py`, you should see:

```
✅ Health check passed
✅ Registration passed
✅ Login passed
✅ Get current user passed
✅ Get sessions passed
✅ Profile operations passed
✅ Refresh token passed
✅ Logout passed

🎉 All API tests completed!
```

## 🔍 Manual Testing Checklist

### Authentication Flow
- [ ] User can register with valid data
- [ ] User cannot register with duplicate email
- [ ] User can login with correct credentials
- [ ] User cannot login with wrong credentials
- [ ] Access token works for protected endpoints
- [ ] Refresh token can generate new access token
- [ ] User can logout and invalidate tokens

### Profile Management
- [ ] User can create profile after registration
- [ ] Profile completion percentage updates correctly
- [ ] User can update profile information
- [ ] Privacy settings are respected
- [ ] Search returns only public profiles
- [ ] Financial information updates work
- [ ] Role-based preferences work (lending/borrowing)

### Security
- [ ] Invalid tokens are rejected
- [ ] Expired tokens are rejected
- [ ] Users can only access their own data
- [ ] Password requirements are enforced
- [ ] Input validation prevents bad data

## 📚 Interactive API Documentation

Visit these URLs when your server is running:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

The interactive docs let you:
- Try all endpoints directly
- See request/response schemas
- Authenticate and test protected endpoints
- View detailed error responses

## 🚀 Next Steps After Testing

Once your tests pass, you can:

1. **Connect React Native Frontend**: Use the API endpoints from your mobile app
2. **Add More Features**: Implement connections, ratings, file uploads
3. **Deploy to Production**: Use the production deployment guide in README.md
4. **Monitor Performance**: Add logging and monitoring tools

## 🆘 Getting Help

If tests are failing:
1. Check the console output for specific error messages
2. Verify your `.env` configuration
3. Ensure PostgreSQL is running and accessible
4. Check the application logs in the terminal
5. Review the troubleshooting section above

The Cooin backend is designed to be robust and provide clear error messages to help you debug any issues quickly!