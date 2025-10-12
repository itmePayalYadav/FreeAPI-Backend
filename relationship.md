# API Models Relationship Diagram

## Model Relationships

### 1. APICategory
- `APICategory` has many `API`s.  
- **Relationship:** One-to-Many (`APICategory` → `API`)  

### 2. API
- `API` belongs to a category (`category` ForeignKey).  
- `API` has many examples (`APIExample`), responses (`APIResponse`), media (`APIMedia`), and subscriptions (`Subscription`).  
- **Relationships:**  
  - One-to-Many: `API` → `APIExample`  
  - One-to-Many: `API` → `APIResponse`  
  - One-to-Many: `API` → `APIMedia`  
  - One-to-Many: `API` → `Subscription`  

### 3. APIExample
- `APIExample` belongs to an `API`.  
- **Relationship:** Many examples per API (1 API → Many examples)  

### 4. APIResponse
- `APIResponse` belongs to an `API`.  
- **Relationship:** Many responses per API (1 API → Many responses)  

### 5. APIMedia
- `APIMedia` belongs to an `API`.  
- **Relationship:** Many media files per API (1 API → Many media)  

### 6. Subscription
- `Subscription` links a `User` to an `API`.  
- One user can subscribe to many APIs.  
- One API can have many subscribers.  
- **Relationship:** Many-to-Many (via Subscription table: User ↔ API)  

### 7. APIUsage
- `APIUsage` belongs to a `Subscription`.  
- Each subscription can have many usage records.  
- **Relationship:** One-to-Many (`Subscription` → `APIUsage`)  

---

## Diagram Representation (Text / UML Style)

