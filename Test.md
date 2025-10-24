# Real Estate RAG Chatbot – Candidate Assessment

## Objective

Build an intelligent real estate chatbot using RAG (Retrieval-Augmented Generation) that:

* **Answers property inquiries** accurately using factual data
* **Converts conversations into qualified leads** by capturing user intent and contact information
* **Maintains trust** through accurate, grounded responses with zero hallucinations
* **Guides users toward engagement** (scheduling viewings, requesting callbacks, etc.)

## Business Context

In real estate, every conversation is a potential lead. The chatbot must:
- Provide accurate property information to build trust
- Identify buying signals and capture lead information naturally
- Encourage next steps (property tours, agent calls, brochure downloads)
- Never provide false information that could damage credibility

## Requirements

### 1. Data Ingestion & RAG Pipeline

**Document Processing:**
- Ingest the **Al Badia Villas Floorplans PDF** (`data/ABV Final Floorplans.pdf`) containing:
  - Property details for Al Badia Villas in Dubai Festival City
  - 3, 4, and 5 bedroom villa configurations (Types: MIA, SHADEA, MODEA)
  - Floor plans, room dimensions, plot areas, built-up areas (BUA)
  - Villa specifications and layouts

**Multimodal Image Handling:**
- Ingest and index **floorplan images** from `data/WebP/` directory (use Rev11 versions)
- Map each image to corresponding villa type and specifications
- Implement image retrieval logic to return relevant floorplan images based on query
- **CRITICAL:** Response must include appropriate image paths when discussing specific villas


### 2. API Endpoint: `/chat`

**POST /chat**

```json
{
  "message": "I'm looking for a 4-bedroom villa with a pool in Dubai",
  "session_id": "user-123",
  "context": {
    "previous_properties_viewed": [],
    "lead_status": "new"
  }
}
```

**Response**

```json
{
  "response": "Great choice! Al Badia Villas in Dubai Festival City offers 4-bedroom villas (SHADEA model) with swimming pool options. These villas have 344 SQM total built-up area with spacious layouts including a master bedroom with walk-in closet, family area, and covered parking. The plot sizes range from 401-664 SQM. Would you like to see the floor plans?",
  "properties_mentioned": ["SHADEA-4BR-TYPE-B"],
  "citations": [{"source": "floorplans_pdf", "page": 7, "villa_type": "4BR Type B with Pool"}],
  "images": [
    {
      "path": "data/WebP/AlBadia_Floorplans_A3_Rev11-7.webp",
      "description": "4BR SHADEA Type B with swimming pool - Ground and first floor layout",
      "relevance": "floorplan"
    }
  ],
  "lead_signals": {
    "intent": "medium",
    "signals_detected": ["specific_requirements", "location_preference", "luxury_feature_interest"],
    "recommended_action": "show_floorplans_and_qualify"
  },
  "follow_up_prompt": "I can send you detailed floor plans and arrange a site visit. What's your preferred timeline for moving?"
}
```

### 3. Lead Generation Requirements

The chatbot must intelligently:

**Detect Buying Signals:**
- Budget mentions
- Specific property requirements (bedrooms, location, amenities)
- Timeline indicators ("looking to move by...", "need soon")
- Comparison questions between properties
- Questions about financing, documentation, or purchase process

**Capture Lead Information:**
- Name, phone, email (request naturally in conversation)
- Budget range
- Property preferences
- Timeline
- Current living situation (renting, selling existing property)

**Guide Toward Conversion:**
- Suggest property viewings
- Offer to connect with agents
- Provide downloadable brochures (email required)
- Schedule callbacks
- Send property comparisons via email

### 4. Retrieval Strategy & Guardrails

**Priority hierarchy:**
1. **Floorplans PDF first** → Always query the Al Badia Villas PDF for:
   - Villa configurations and types
   - Exact dimensions and areas (SQM/SQFT)
   - Room layouts and counts
   - Plot sizes and built-up areas
2. **Visual references** → Use floorplan images from `data/WebP/` to:
   - Show visual layout references
   - Validate spatial information
   - Provide visual confirmation of features
3. **General knowledge fallback** → Use LLM knowledge only for:
   - Dubai Festival City location information
   - General real estate guidance
   - Amenities in the area
   - Market context
4. **Refuse when uncertain** → Never hallucinate pricing, availability, or features not in the PDF

**Critical guardrails:**
- ❌ Never invent villa prices or availability (not in the PDF)
- ❌ Never contradict the floorplan specifications
- ❌ Never provide square footage outside the documented ranges
- ❌ Never add features not shown in the floorplans
- ✅ Always cite the PDF page number for villa specifications
- ✅ Acknowledge when pricing/availability needs agent confirmation
- ✅ Provide exact dimensions from the floorplans
- ✅ Offer to connect with sales team for pricing and availability

### 5. LLM Integration

- Use any LLM (OpenAI, Anthropic, open-source)
- Implement prompt engineering for:
  - Conversational, helpful tone
  - Lead qualification questions
  - Natural information capture
  - Urgency creation without being pushy


## Deliverables

### 1. Code Implementation
- Data ingestion pipeline (PDF + image processing, vector DB setup)
- `/chat` API endpoint with full functionality including image responses
- Lead tracking and scoring system
- Session management for conversation continuity
- Image retrieval and mapping logic

### 2. Documentation
- **README.md**: Setup and run instructions
- **DESIGN.md**: Architecture decisions including:
  - RAG strategy (chunking, retrieval, ranking)
  - Multimodal handling (PDF + image processing and retrieval)
  - Image-to-villa mapping strategy
  - Lead detection logic
  - Guardrail implementation
  - Prompt engineering approach
  - Lead scoring methodology

### 3. Testing & Examples
- Sample conversation flows demonstrating:
  - Accurate property information retrieval
  - **Correct floorplan image responses**
  - Natural lead capture
  - Appropriate refusals when data is missing
  - Citation accuracy (PDF page numbers)
- Test cases covering edge cases
- Image response validation tests

## Evaluation Rubric (100 pts)

| Area                        | Points | Evaluation Criteria                                                                 |
| --------------------------- | -----: | ----------------------------------------------------------------------------------- |
| **RAG Accuracy**            |     20 | Accurate retrieval; proper citations; no hallucinations on property data            |
| **Lead Generation**         |     25 | Detects buying signals; captures contact info naturally; suggests relevant actions  |
| **Multimodal Response**     |     15 | Returns relevant floorplan images; correct image-to-villa mapping; visual context   |
| **Guardrails & Safety**     |     20 | Never invents prices/availability; appropriate refusals; facts override external    |
| **Conversation Quality**    |     10 | Natural dialogue; helpful tone; guides toward conversion without being pushy        |
| **Code Quality**            |      7 | Clean, modular, testable; proper error handling; scalable design                    |
| **Documentation**           |      3 | Clear setup instructions; design rationale; lead scoring explanation                |

### Pass Criterion

**Score ≥ 80** with:
- ✅ Zero hallucinations on critical data (pricing, availability, property features)
- ✅ At least 3 successful lead captures in test conversations
- ✅ Proper citation for all property-specific claims (PDF page numbers)
- ✅ **Correct floorplan images returned in 100% of villa-specific queries**
- ✅ Natural conversation flow with appropriate lead qualification

## Bonus Points (+15)

- **Multi-property comparison feature with side-by-side images** (+3)
- **Visual Q&A**: Answer questions about room layouts using image analysis (+4)
- Lead scoring algorithm with explanation (+2)
- A/B testing framework for conversion optimization (+2)
- Integration with CRM system (mock API) (+2)
- Multilingual support (+2)

## Important Notes

### Multimodal Requirements
⚠️ **CRITICAL:** Your chatbot MUST return relevant floorplan images in responses when discussing specific villas. This is not optional - it's a core requirement worth 15 points in the evaluation rubric.

### Data Integrity
- All villa specifications must come from the PDF (pages 4-8)
- Use only Rev11 images from `data/WebP/` directory
- Never use superseded versions from `_Superati/` folder
- Always cite PDF page numbers for factual claims

### Lead Generation Focus
This is a **conversion-focused** chatbot. Every response should:
1. Provide accurate information from the PDF
2. Show relevant floorplan images
3. Move the conversation toward capturing lead information
4. Create urgency without being pushy

Good luck! 🏡


