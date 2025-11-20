# Tickets/Offers Feature - Technical Documentation

**Feature Name**: Tickets/Offers Marketplace
**Implemented**: 2025-11-19 (Session Current)
**Status**: Working ✅
**Last Updated**: 2025-11-19

---

## 📋 Quick Overview

**What It Does**: Allows users to create and browse lending offers and borrowing requests in a marketplace-style interface. Users can convert tickets into "deals" (connections with source tracking).

**Key Components**:
- Backend: Database model, API endpoints, service layer
- Frontend: Marketplace UI, 4-step creation wizard, enhanced connection cards
- Integration: Tickets → Deals → Connections workflow

**Use Cases**:
- Lenders post available funds with terms
- Borrowers post funding needs
- Parties create deals from tickets
- Track deal terms separately from original tickets

---

## 🗂️ File Structure

```
cooin-backend/
├── app/
│   ├── models/
│   │   └── ticket.py                    # Database model + enums
│   ├── schemas/
│   │   └── ticket.py                    # Pydantic validation schemas
│   ├── services/
│   │   └── ticket_service.py            # Business logic layer
│   └── api/v1/
│       └── tickets.py                   # REST API endpoints
└── alembic/versions/
    └── 402fa75d35c2_add_tickets_*.py    # Database migration

cooin-frontend/
├── src/
│   ├── screens/tickets/
│   │   ├── TicketsScreen.tsx            # 3-tab marketplace (654 lines)
│   │   └── CreateTicketModal.tsx        # 4-step wizard (715 lines)
│   ├── components/
│   │   └── ConnectionCard.tsx           # Enhanced with deals display
│   ├── navigation/
│   │   └── AppNavigator.tsx             # Added Tickets tab
│   ├── types/
│   │   └── api.ts                       # TypeScript interfaces
│   └── i18n/locales/
│       └── en.json                      # i18n translations
```

---

## 🔧 Backend Architecture

### Database Schema (`app/models/ticket.py`)

**Ticket Model Fields**:
```python
# Identity
id: Integer (Primary Key)
user_id: Integer (Foreign Key → users)

# Core Fields
ticket_type: Enum('lending_offer', 'borrowing_request')
title: String(200) - required
description: Text - required
status: Enum('active', 'pending', 'closed', 'expired')

# Financial Terms (Base)
amount: Float - required
interest_rate: Float - required (0-100 APR)
term_months: Integer - required (1-360)

# Financial Terms (Flexible Ranges - Optional)
min_amount, max_amount: Float
min_interest_rate, max_interest_rate: Float
min_term_months, max_term_months: Integer
flexible_terms: Boolean (enables ranges)

# Loan Details
loan_type: Enum('personal', 'business', 'mortgage', 'auto', 'education', 'medical', 'other')
loan_purpose: Text - required
warranty_type: Enum('none', 'property', 'vehicle', 'equipment', 'investments', 'cosigner', 'other')
warranty_description: Text - optional
warranty_value: Float - optional

# Additional
requirements: Text - optional
preferred_location: String(100) - optional
is_public: Boolean - default True

# Engagement Tracking
views_count: Integer - default 0
responses_count: Integer - default 0
deals_created: Integer - default 0

# Timestamps
created_at, updated_at: DateTime (auto)
expires_at: DateTime
```

**Connection Model Extension**:
```python
# New fields added to existing Connection model
source_ticket_id: Integer (Foreign Key → tickets, nullable)
proposed_amount: Float - nullable
proposed_interest_rate: Float - nullable
proposed_term_months: Integer - nullable
```

**Indexes Created**:
- `ix_tickets_user_id` - For user's tickets queries
- `ix_tickets_ticket_type` - For type filtering
- `ix_tickets_status` - For status filtering
- `ix_tickets_created_at` - For chronological sorting
- `ix_connections_source_ticket_id` - For deal lookups

---

### API Endpoints (`app/api/v1/tickets.py`)

**8 RESTful Endpoints**:

#### 1. Create Ticket
```http
POST /api/v1/tickets/
Authorization: Bearer {token}
Content-Type: application/json

Request Body: TicketCreate schema
Response: 201 Created - TicketResponse
```

#### 2. List Public Tickets
```http
GET /api/v1/tickets/?ticket_type=lending_offer&min_amount=10000
Authorization: Bearer {token}

Query Params:
  - ticket_type: 'lending_offer' | 'borrowing_request'
  - status: 'active' | 'pending' | 'closed' | 'expired'
  - loan_type: enum value
  - min_amount, max_amount: number
  - min_interest_rate, max_interest_rate: number
  - location: string
  - skip, limit: pagination

Response: 200 OK - TicketListResponse
```

#### 3. Get My Tickets
```http
GET /api/v1/tickets/my-tickets?skip=0&limit=50
Authorization: Bearer {token}

Response: 200 OK - TicketListResponse
```

#### 4. Get Ticket Stats
```http
GET /api/v1/tickets/stats
Authorization: Bearer {token}

Response: 200 OK - TicketStats
{
  "total_tickets": 10,
  "active_tickets": 7,
  "total_views": 156,
  "total_responses": 23,
  "deals_created": 5
}
```

#### 5. Get Single Ticket
```http
GET /api/v1/tickets/{ticket_id}
Authorization: Bearer {token}

Response: 200 OK - TicketWithUser
```

#### 6. Update Ticket
```http
PUT /api/v1/tickets/{ticket_id}
Authorization: Bearer {token}
Content-Type: application/json

Request Body: TicketUpdate schema (all fields optional)
Response: 200 OK - TicketResponse
Validation: Only ticket owner can update
```

#### 7. Delete Ticket
```http
DELETE /api/v1/tickets/{ticket_id}
Authorization: Bearer {token}

Response: 200 OK - {"message": "Ticket deleted successfully"}
Validation: Only ticket owner can delete
```

#### 8. Create Deal from Ticket
```http
POST /api/v1/tickets/create-deal
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "ticket_id": 123,
  "message": "Interested in your offer",
  "proposed_amount": 35000,         # optional - override ticket amount
  "proposed_interest_rate": 7.5,    # optional - override ticket rate
  "proposed_term_months": 24        # optional - override ticket term
}

Response: 201 Created - ConnectionResponse
Creates: Connection with source_ticket_id set
```

---

### Business Logic (`app/services/ticket_service.py`)

**8 Service Methods**:

1. `create_ticket(db, ticket_data, user_id)` → Ticket
   - Validates user exists
   - Creates ticket with auto-expiry (30 days)
   - Returns created ticket

2. `get_ticket(db, ticket_id)` → TicketWithUser
   - Fetches ticket with user relationship
   - Increments views_count
   - Raises NotFoundError if missing

3. `update_ticket(db, ticket_id, user_id, ticket_data)` → Ticket
   - Authorization check (owner only)
   - Partial update support
   - Raises AuthorizationError if not owner

4. `delete_ticket(db, ticket_id, user_id)` → None
   - Authorization check (owner only)
   - Hard delete from database
   - Raises NotFoundError or AuthorizationError

5. `list_tickets(db, filters, skip, limit)` → List[TicketWithUser]
   - Supports 8+ filter combinations
   - Public tickets only (unless viewing own)
   - Chronological ordering (newest first)

6. `create_deal_from_ticket(db, ticket_id, requester_id, deal_data)` → Connection
   - Validates ticket exists and is active
   - Prevents self-deals (ticket owner can't create deal with own ticket)
   - Determines connection_type based on ticket_type:
     - LENDING_OFFER → borrowing_request
     - BORROWING_REQUEST → lending_inquiry
   - Creates Connection with:
     - source_ticket_id = ticket.id
     - proposed_amount, proposed_interest_rate, proposed_term_months
   - Increments ticket.deals_created counter
   - Returns created connection

7. `get_ticket_stats(db, user_id)` → TicketStats
   - Aggregates user's ticket metrics
   - Returns counts and totals

8. Filtering Logic:
   - ticket_type filter
   - status filter (defaults to 'active')
   - loan_type filter
   - Amount range (min_amount, max_amount)
   - Interest rate range
   - Location matching (case-insensitive contains)
   - Public visibility filter
   - User ownership filter

---

## 🎨 Frontend Architecture

### Screens

#### TicketsScreen (`src/screens/tickets/TicketsScreen.tsx` - 654 lines)

**3-Tab Marketplace Interface**:

**Tab 1: Lending Offers**
- Displays all active lending offer tickets
- Shows lender's available funds and terms
- "Create Deal" button for borrowers

**Tab 2: Borrowing Requests**
- Displays all active borrowing request tickets
- Shows borrower's funding needs
- "Create Deal" button for lenders

**Tab 3: My Tickets**
- Shows user's own created tickets
- View/edit/delete capabilities
- Status tracking

**Key Features**:
- Pull-to-refresh functionality
- Ticket cards display:
  - Title, description
  - Financial terms (amount, rate, term)
  - Loan type and purpose
  - Warranty information
  - Days since created
- Floating "Create Ticket" button
- Details modal for full ticket view
- Alert.prompt for deal creation message
- Loading states and error handling

**State Management**:
```typescript
const [tickets, setTickets] = useState<Ticket[]>([]);
const [myTickets, setMyTickets] = useState<Ticket[]>([]);
const [selectedTab, setSelectedTab] = useState(0); // 0=Lending, 1=Borrowing, 2=Mine
const [loading, setLoading] = useState(true);
const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
const [showModal, setShowModal] = useState(false);
const [showCreateModal, setShowCreateModal] = useState(false);
```

**API Integration**:
- `loadTickets()` - Fetches public tickets by type
- `loadMyTickets()` - Fetches user's tickets
- `handleCreateDeal(ticketId)` - Creates connection from ticket
- Auto-refresh on tab change
- Error handling with user-friendly messages

---

#### CreateTicketModal (`src/screens/tickets/CreateTicketModal.tsx` - 715 lines)

**4-Step Wizard Form**:

**Step 1: Basic Information**
- Ticket type selection (Lending Offer / Borrowing Request)
  - Shown only if user.role === 'BOTH'
  - Auto-selected based on user.role otherwise
- Title input (10-200 characters)
  - Character counter
  - Placeholder examples
- Description textarea (50+ characters)
  - Character counter
  - Multiline support

**Step 2: Financial Terms**
- Amount input (required, > 0)
- Interest rate input (0-100%)
- Term in months (1-360)
- "Flexible Terms" toggle
  - When enabled: Shows min/max range inputs
  - min_amount, max_amount
  - min_interest_rate, max_interest_rate
  - min_term_months, max_term_months

**Step 3: Loan Details**
- Loan type picker (dropdown):
  - Personal, Business, Mortgage, Auto, Education, Medical, Other
- Loan purpose textarea (20+ characters)
  - Character counter
- Warranty type picker:
  - None, Property, Vehicle, Equipment, Investments, Cosigner, Other
- Warranty description (shown if warranty_type !== 'NONE')
- Warranty value input (shown if warranty_type !== 'NONE')

**Step 4: Additional Details & Review**
- Requirements textarea (optional)
- Preferred location input (optional)
- Public/Private toggle
- Summary review of all entered data:
  - Type and title
  - Financial terms
  - Loan details
  - Additional info

**Validation System**:
```typescript
validateStep1(): boolean {
  // Title: 10-200 characters
  // Description: 50+ characters
  return title.length >= 10 && description.length >= 50;
}

validateStep2(): boolean {
  // Amount: valid number > 0
  // Interest rate: 0-100
  // Term: 1-360 months
  // Flexible terms range validation
  return isValidAmount && isValidRate && isValidTerm;
}

validateStep3(): boolean {
  // Loan purpose: 20+ characters
  // Warranty value required if warranty_type !== 'NONE'
  return loanPurpose.length >= 20 && warrantyValidation;
}
```

**User Feedback**:
- Step progress indicators (1/4, 2/4, 3/4, 4/4)
- Real-time character counters
- Validation error alerts
- Back/Next navigation
- Loading state on submit
- Success alert on creation
- Console logging for debugging

---

### Components

#### ConnectionCard Enhancement (`src/components/ConnectionCard.tsx`)

**New Features for Deals**:

**Deal Badge**:
```typescript
if (connection.source_ticket_id) {
  return (
    <View style={[styles.dealBadge, { backgroundColor: `${COLORS.warning}20` }]}>
      <Ionicons name="ticket" size={14} color={COLORS.warning} />
      <Text style={styles.typeText}>Deal</Text>
    </View>
  );
}
```

**Proposed Terms Display**:
```typescript
// Prioritize proposed terms from deal
const amount = connection.proposed_amount || connection.loan_amount_requested;
const rate = connection.proposed_interest_rate || connection.interest_rate_proposed;
const term = connection.proposed_term_months || connection.loan_term_months;

// Show "Deal Terms from Ticket" header
if (connection.source_ticket_id) {
  <View style={styles.dealHeader}>
    <Ionicons name="information-circle" size={16} color={COLORS.warning} />
    <Text style={styles.dealHeaderText}>Deal Terms from Ticket</Text>
  </View>
}
```

**Styles Added**:
```typescript
dealBadge: {
  flexDirection: 'row',
  alignItems: 'center',
  paddingHorizontal: SPACING.sm,
  paddingVertical: SPACING.xs,
  borderRadius: 6,
},
dealHeader: {
  flexDirection: 'row',
  alignItems: 'center',
  marginBottom: SPACING.sm,
  paddingBottom: SPACING.xs,
  borderBottomWidth: 1,
  borderBottomColor: COLORS.border,
},
dealHeaderText: {
  fontSize: 13,
  fontFamily: FONTS.medium,
  color: COLORS.warning,
  marginLeft: 6,
},
```

---

### Navigation Integration

**AppNavigator.tsx Changes**:
```typescript
// Added to navigation items array
{
  name: 'Tickets',
  component: TicketsScreen,
  iconFocused: 'ticket',
  iconOutline: 'ticket-outline',
  labelKey: 'navigation.tickets'
}
```

**Available in**:
- Desktop sidebar navigation
- Mobile bottom tab navigation

**i18n Translation** (`src/i18n/locales/en.json`):
```json
{
  "navigation": {
    "tickets": "Tickets"
  }
}
```

---

### Type Definitions (`src/types/api.ts`)

**Connection Interface Update**:
```typescript
export interface Connection {
  // ... existing fields
  source_ticket_id?: number;          // NEW: Links to originating ticket
  proposed_amount?: number;            // NEW: Deal-specific amount
  proposed_interest_rate?: number;     // NEW: Deal-specific rate
  proposed_term_months?: number;       // NEW: Deal-specific term
}
```

---

## 🗄️ Database Migration

**Migration File**: `alembic/versions/402fa75d35c2_add_tickets_table_and_source_ticket_id_.py`

**Changes Made**:

1. **Created `tickets` table**:
   - All fields defined above
   - 5 indexes for performance
   - Foreign key to users table
   - Enum types for ticket_type, status, loan_type, warranty_type

2. **Modified `connections` table**:
   - Added `source_ticket_id` column (nullable)
   - Added index on `source_ticket_id`
   - Added foreign key constraint to tickets table

**SQLite Compatibility Fixes**:
```python
# Used batch_alter_table for SQLite
with op.batch_alter_table('connections', schema=None) as batch_op:
    batch_op.add_column(sa.Column('source_ticket_id', sa.Integer(), nullable=True))
    batch_op.create_index('ix_connections_source_ticket_id', ['source_ticket_id'])
    batch_op.create_foreign_key('fk_connections_source_ticket', 'tickets',
                                 ['source_ticket_id'], ['id'])

# Conditional table creation (handles partial migrations)
inspector = sa.inspect(op.get_bind())
existing_tables = inspector.get_table_names()
if 'tickets' not in existing_tables:
    op.create_table('tickets', ...)
```

**Run Migration**:
```bash
cd cooin-backend
alembic upgrade head
```

**Rollback** (if needed):
```bash
alembic downgrade -1
```

---

## 🔌 API Client Integration

**Frontend API Service** (`src/services/api.ts`):

**Singleton Pattern**:
```typescript
import { apiClient } from '../../services/api';
```

**Auto-Features**:
- Automatic token injection from secure storage
- Token refresh on 401 errors
- Request/response interceptors
- Centralized error handling
- Retry logic

**Usage in Tickets**:
```typescript
// Create ticket
const response = await apiClient.post('/tickets/', ticketData);

// List tickets with filters
const tickets = await apiClient.get('/tickets/', {
  params: { ticket_type: 'lending_offer', min_amount: 10000 }
});

// Create deal
const connection = await apiClient.post('/tickets/create-deal', dealData);
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "Cannot read properties of undefined (reading 'post')"

**Error**:
```
TypeError: Cannot read properties of undefined (reading 'post')
at handleSubmit (CreateTicketModal.tsx:222:17)
```

**Cause**: Incorrect API import
**Solution**:
```typescript
// ❌ Wrong
import { api } from '../../services/api';

// ✅ Correct
import { apiClient } from '../../services/api';
```

---

### Issue 2: 422 Validation Error - Enum Values

**Error**:
```json
{
  "detail": "body -> ticket_type: Input should be 'lending_offer' or 'borrowing_request'",
  "status_code": 422
}
```

**Cause**: Backend expects lowercase enum values
**Solution**:
```typescript
// Convert to lowercase before sending
const ticketData = {
  ticket_type: ticketType.toLowerCase(),  // LENDING_OFFER → lending_offer
  loan_type: loanType.toLowerCase(),      // PERSONAL → personal
  warranty_type: warrantyType.toLowerCase(), // NONE → none
  // ...
};
```

---

### Issue 3: Next Button Not Working in Wizard

**Symptoms**: Clicking "Next" does nothing

**Validation Requirements**:
- **Step 1**: Title ≥ 10 chars, Description ≥ 50 chars
- **Step 2**: Valid numbers for amount/rate/term
- **Step 3**: Loan purpose ≥ 20 chars

**Debug**:
```typescript
// Check browser console (F12)
// Look for validation logs:
console.log('Validating step 1 - title:', title, 'description:', description);
console.log('Validation failed:', message);
```

**Solution**: Fill all required fields meeting minimum character counts

---

### Issue 4: CORS Error - Cannot Connect to Backend

**Error**: "Cannot connect to server. Please check your internet connection."

**Cause**: Frontend port not in CORS allowlist
**Solution**:

**Backend** (`cooin-backend/.env`):
```bash
BACKEND_CORS_ORIGINS=["http://localhost:19000","http://localhost:19006","http://localhost:8081"]
```

**Restart Backend**:
```bash
# Kill existing backend server
# Restart with:
cd cooin-backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Issue 5: Alert Dialogs Not Showing on Web

**Cause**: React Native Alert doesn't render on web platform
**Debug**: Check browser console for validation messages

**Temporary Solution**: Console logs added for debugging
**Future Enhancement**: Replace Alert with web-friendly modal component

---

## ✅ Testing Checklist

### Backend API Testing

```bash
# Set token variable
TOKEN="your_jwt_token_here"

# 1. Create lending offer
curl -X POST http://localhost:8000/api/v1/tickets/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_type": "lending_offer",
    "title": "Offering $50,000 for small businesses",
    "description": "I have $50,000 available for established small businesses with good credit. Flexible terms and competitive rates.",
    "amount": 50000,
    "interest_rate": 7.5,
    "term_months": 36,
    "loan_type": "business",
    "loan_purpose": "Small business expansion and working capital",
    "warranty_type": "property",
    "flexible_terms": true,
    "is_public": true
  }'

# 2. List lending offers
curl http://localhost:8000/api/v1/tickets/?ticket_type=lending_offer \
  -H "Authorization: Bearer $TOKEN"

# 3. Create deal from ticket
curl -X POST http://localhost:8000/api/v1/tickets/create-deal \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": 1,
    "message": "Interested in your lending offer",
    "proposed_amount": 35000,
    "proposed_interest_rate": 7.5,
    "proposed_term_months": 24
  }'

# 4. Verify connection created
curl http://localhost:8000/api/v1/connections/ \
  -H "Authorization: Bearer $TOKEN"
```

### Frontend UI Testing

**Checklist**:
- [ ] Navigate to Tickets tab
- [ ] View Lending Offers tab (shows lending tickets)
- [ ] View Borrowing Requests tab (shows borrowing tickets)
- [ ] View My Tickets tab (shows user's tickets)
- [ ] Click "Create Ticket" floating button
- [ ] **Step 1**: Fill title (10+ chars) and description (50+ chars)
- [ ] Click "Next" → Navigate to Step 2
- [ ] **Step 2**: Fill amount, rate, term
- [ ] Toggle "Flexible Terms" → See min/max inputs
- [ ] Click "Next" → Navigate to Step 3
- [ ] **Step 3**: Select loan type, fill purpose (20+ chars)
- [ ] Select warranty type
- [ ] Click "Next" → Navigate to Step 4
- [ ] **Step 4**: Review summary, toggle public
- [ ] Click "Create Ticket" → Success alert
- [ ] Verify ticket appears in "My Tickets"
- [ ] Switch to appropriate tab → See created ticket
- [ ] Click "Create Deal" on a ticket
- [ ] Enter message → Deal created
- [ ] Navigate to Connections → See deal
- [ ] Verify "Deal" badge appears
- [ ] Verify proposed terms display
- [ ] Verify "Deal Terms from Ticket" header

---

## 🚀 Deployment Checklist

**Backend**:
- [ ] Run database migration (`alembic upgrade head`)
- [ ] Verify tickets table created
- [ ] Verify connections.source_ticket_id column added
- [ ] Test all 8 API endpoints
- [ ] Check CORS configuration
- [ ] Verify authentication works

**Frontend**:
- [ ] Install @react-native-picker/picker dependency
- [ ] Verify navigation shows Tickets tab
- [ ] Test on web platform
- [ ] Test on mobile (iOS/Android if applicable)
- [ ] Verify API client integration
- [ ] Check error handling

---

## 📊 Performance Considerations

**Database Queries**:
- Tickets list queries use indexes (ticket_type, status, created_at)
- Pagination implemented (skip, limit parameters)
- User relationship loaded with joinedload for N+1 prevention

**Frontend Optimization**:
- Pull-to-refresh prevents stale data
- Loading states prevent multiple simultaneous requests
- Tab-based filtering reduces data transfer
- Modal-based creation prevents navigation overhead

**Future Optimizations**:
- [ ] Add caching for frequently accessed tickets
- [ ] Implement infinite scroll for ticket lists
- [ ] Add search debouncing
- [ ] Optimize image loading (if ticket images added)

---

## 🔮 Future Enhancements

1. **Search & Filtering**
   - Full-text search on title/description
   - Advanced filter combinations
   - Saved search preferences
   - Filter presets

2. **Matching Algorithm**
   - Auto-match borrowers with lenders
   - Compatibility scoring based on:
     - Amount alignment
     - Rate compatibility
     - Term matching
     - Location proximity
   - Smart recommendations

3. **Negotiation System**
   - Counter-offers on deals
   - Terms comparison view
   - Negotiation history tracking
   - In-app chat integration

4. **Analytics & Insights**
   - Ticket performance dashboard
   - View-to-deal conversion rate
   - Market rate analysis
   - Trend visualization

5. **Verification & Trust**
   - Verified ticket badge
   - User ratings on tickets
   - Ticket reporting/flagging system
   - Identity verification integration

6. **Notifications**
   - New tickets matching preferences
   - Deal creation alerts
   - Ticket expiry warnings
   - Response notifications

---

## 📚 Related Documentation

- **Main README**: `README.md` - Project overview
- **Launch Guide**: `HOW-TO-LAUNCH-WEB-APP.md` - How to start the app
- **Development Process**: `DP.md` - Documentation standards
- **Session History**: `HISTORY.md` - Change log
- **Current Tasks**: `TODO.md` - Pending work

---

## 🎓 Key Learnings

**Architecture Decisions**:
1. **Why source_ticket_id?**: Maintains relationship between deals and original tickets without tight coupling
2. **Why proposed_* fields?**: Allows deal terms to differ from original ticket terms
3. **Why 4-step wizard?**: Reduces cognitive load, improves data quality, better UX
4. **Why separate tickets from connections?**: Tickets are public marketplace listings, connections are private relationships

**Technical Gotchas**:
1. Enum values must be lowercase (backend expects 'lending_offer' not 'LENDING_OFFER')
2. Alert.alert doesn't render on web - use console.log for debugging
3. apiClient vs api import - use correct export name
4. SQLite requires batch_alter_table for foreign key additions
5. CORS must include all frontend ports (19000, 19006, 8081, etc.)

---

## 👥 Contributors

**Implementation**: Claude Code
**Date**: November 2025
**Session**: Current
**Review Status**: Working ✅

---

**Last Updated**: 2025-11-19
**Maintained By**: Development Team
**Next Review**: After user testing
