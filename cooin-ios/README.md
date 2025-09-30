# Cooin iOS App

A comprehensive peer-to-peer lending platform built with SwiftUI that connects to the Cooin backend API.

## Features

- **Authentication**: User registration and login with JWT token management
- **Dashboard**: Real-time analytics and platform overview
- **Loan Matching**: Browse lenders/borrowers and create loan requests/offers
- **Analytics**: Comprehensive platform statistics and insights
- **Profile Management**: User profiles with role-based features
- **Document Verification**: Camera and photo library integration for document uploads
- **File Upload**: Support for various document types with progress tracking

## Architecture

- **SwiftUI**: Modern declarative UI framework
- **Combine**: Reactive programming for API calls
- **MVVM**: Model-View-ViewModel architecture pattern
- **Environment Objects**: Dependency injection for shared state
- **REST API Integration**: Complete integration with Cooin backend

## Project Structure

```
Cooin/
├── CooinApp.swift              # Main app entry point
├── Services/
│   ├── APIClient.swift         # Network layer and API calls
│   ├── AuthenticationManager.swift # Authentication state management
│   └── FileUploadManager.swift # File upload functionality
├── Models/
│   └── Models.swift           # Data models for API responses
└── Views/
    ├── ContentView.swift      # Main content coordinator
    ├── WelcomeView.swift      # Landing page for unauthenticated users
    ├── LoginView.swift        # User login screen
    ├── RegisterView.swift     # User registration screen
    ├── MainTabView.swift      # Main tab navigation
    ├── AnalyticsView.swift    # Analytics dashboard
    ├── MatchingView.swift     # Loan matching interface
    ├── ProfileView.swift      # User profile and settings
    ├── DocumentVerificationView.swift # Document upload interface
    └── AppInfoView.swift      # App information and help
```

## Requirements

- iOS 14.0+
- Xcode 13.0+
- Swift 5.5+
- Active Cooin backend API (running at http://192.168.40.34:8000)

## Setup Instructions

1. **Open in Xcode**:
   ```bash
   # Navigate to the iOS project directory
   cd cooin-ios

   # Open the project in Xcode
   open Cooin.xcodeproj
   ```

2. **Configure Project Settings**:
   - Set your development team in project settings
   - Update bundle identifier if needed
   - Ensure deployment target is iOS 14.0+

3. **Backend Configuration**:
   - Ensure the Cooin backend is running at `http://192.168.40.34:8000`
   - The app is configured to connect to this endpoint
   - Update `APIClient.swift` if using a different backend URL

4. **Permissions**:
   - Camera access for document capture
   - Photo library access for document selection
   - Network access for API communication

## Building and Running

1. **Build the Project**:
   - Select your target device or simulator
   - Press Cmd+B to build
   - Fix any build errors if they occur

2. **Run the App**:
   - Press Cmd+R to build and run
   - The app will launch with the welcome screen
   - Create an account or login with existing credentials

## Key Components

### Authentication Flow
- Welcome screen with login/register options
- JWT token storage in UserDefaults
- Automatic token refresh and validation
- Role-based UI (borrower vs lender)

### Dashboard
- Real-time platform statistics
- Financial overview with formatted amounts
- Quick action buttons based on user role
- Pull-to-refresh functionality

### Loan Matching
- Create loan requests (borrowers)
- Create lending offers (lenders)
- Browse available opportunities
- View matched profiles with compatibility scores

### Document Verification
- Multiple document type support
- Camera integration for real-time capture
- Photo library selection
- Upload progress tracking
- Document status management

### File Upload System
- Multipart form data uploads
- Progress tracking with visual feedback
- Error handling and retry mechanisms
- Support for images and documents

## API Integration

The app integrates with the following backend endpoints:

- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /auth/me` - Get current user info
- `GET /analytics/mobile` - Mobile analytics data
- `GET /health` - Health check
- `POST /documents/upload` - Document upload

## Testing

### Manual Testing Checklist
- [ ] User registration with validation
- [ ] User login with error handling
- [ ] Dashboard data loading
- [ ] Analytics screen functionality
- [ ] Loan request/offer creation
- [ ] Browse lenders/borrowers
- [ ] Profile management
- [ ] Document upload with camera
- [ ] Document upload from photo library
- [ ] Logout functionality

### Simulator Testing
- Test on various device sizes (iPhone SE, iPhone 14, iPhone 14 Plus)
- Test orientation changes
- Test different iOS versions (14.0+)

## Troubleshooting

### Common Issues

1. **Network Connection Errors**:
   - Ensure backend is running on `http://192.168.40.34:8000`
   - Check that your device/simulator can reach the backend
   - Verify firewall settings allow connection on port 8000

2. **Build Errors**:
   - Clean build folder (Cmd+Shift+K)
   - Delete derived data
   - Restart Xcode

3. **Camera/Photo Library Access**:
   - Check that permissions are granted in device settings
   - Verify Info.plist contains usage descriptions

4. **Authentication Issues**:
   - Clear app data/reinstall app to reset stored tokens
   - Check backend logs for authentication errors

## Production Considerations

Before deploying to production:

1. **Security**:
   - Use HTTPS for all API communication
   - Implement certificate pinning
   - Add additional input validation

2. **Performance**:
   - Implement image caching for profile photos
   - Add offline support for critical features
   - Optimize API calls with pagination

3. **User Experience**:
   - Add loading states for all async operations
   - Implement proper error handling with user-friendly messages
   - Add accessibility support

4. **Backend Integration**:
   - Replace hardcoded API URL with configuration
   - Implement proper token refresh mechanism
   - Add API versioning support

## Contributing

1. Follow SwiftUI best practices
2. Maintain consistent code style
3. Add appropriate comments for complex logic
4. Test on multiple device sizes
5. Update this README for any significant changes