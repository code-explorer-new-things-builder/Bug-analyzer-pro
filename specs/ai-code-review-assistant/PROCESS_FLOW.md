# AI-Powered Code Review Assistant - Process Flow

## Simple Process Flow Diagram

```mermaid
flowchart TD
    START([User Submits Code]) --> PARSE[Parse Code to AST]
    PARSE --> ANALYZE[Analyze Code]
    ANALYZE --> BUG[Detect Bugs]
    ANALYZE --> SEC[Scan Security]
    ANALYZE --> STYLE[Check Style]
    BUG --> AI{AI Available?}
    SEC --> AI
    STYLE --> AI
    AI -->|Yes| ENHANCE[AI Enhancement]
    AI -->|No| REPORT[Generate Report]
    ENHANCE --> REPORT
    REPORT --> END([Display Results])
    
    style START fill:#90EE90
    style END fill:#FFB6C1
    style AI fill:#FFD700
    style ENHANCE fill:#87CEEB
```

---

## Detailed Flow (Without AI)

```mermaid
flowchart LR
    A([Code Input]) --> B[Detect Language]
    B --> C[Parse to AST]
    C --> D[Rule-Based Analysis]
    D --> E[Bug Detection]
    D --> F[Security Scan]
    D --> G[Style Check]
    E --> H[Generate Report]
    F --> H
    G --> H
    H --> I([Output])
    
    style A fill:#90EE90
    style I fill:#FFB6C1
```

---

## Detailed Flow (With AI)

```mermaid
flowchart LR
    A([Code Input]) --> B[Detect Language]
    B --> C[Parse to AST]
    C --> D[Rule-Based Analysis]
    D --> E[AI Enhancement]
    E --> F[Context Analysis]
    F --> G[Smart Explanations]
    G --> H[Generate Report]
    H --> I([Output])
    
    style A fill:#90EE90
    style I fill:#FFB6C1
    style E fill:#FFD700
    style F fill:#87CEEB
```

---

## Complete System Flow

```mermaid
graph TD
    USER[User] --> CLI[CLI/Web/IDE]
    CLI --> PARSER[Language Parser]
    PARSER --> ANALYZER[Code Analyzer]
    ANALYZER --> RULES[Rule Engine]
    ANALYZER --> AI[AI Service]
    RULES --> FINDINGS[Findings]
    AI --> FINDINGS
    FINDINGS --> REPORT[Report Generator]
    REPORT --> USER
    
    style USER fill:#90EE90
    style AI fill:#FFD700
    style REPORT fill:#FFB6C1
```

---

## Step-by-Step Process

1. **Input**: User submits code file
2. **Parse**: Detect language and parse to AST
3. **Analyze**: Run bug, security, and style checks
4. **Enhance**: AI adds context and explanations (optional)
5. **Report**: Generate formatted report
6. **Output**: Display results to user

---

## Key Components

```mermaid
graph LR
    A[Code] --> B[Parser]
    B --> C[Analyzer]
    C --> D[AI Optional]
    D --> E[Report]
    
    style A fill:#90EE90
    style D fill:#FFD700
    style E fill:#FFB6C1
```


---

## System Architecture Diagram

```mermaid
graph TB
    subgraph "User Layer"
        CLI[CLI Interface]
        WEB[Web Interface]
        IDE[IDE Plugin]
    end
    
    subgraph "Core Engine"
        ORCH[Orchestrator]
        PARSER[Language Parser]
    end
    
    subgraph "Analysis Layer"
        BUG[Bug Detector]
        SEC[Security Scanner]
        STYLE[Style Checker]
    end
    
    subgraph "AI Layer"
        AI[AI Service<br/>GPT-4/Claude]
    end
    
    subgraph "Output Layer"
        EDU[Educational Engine]
        REPORT[Report Generator]
    end
    
    CLI --> ORCH
    WEB --> ORCH
    IDE --> ORCH
    
    ORCH --> PARSER
    PARSER --> BUG
    PARSER --> SEC
    PARSER --> STYLE
    
    BUG --> EDU
    SEC --> EDU
    STYLE --> EDU
    
    BUG -.Optional.-> AI
    SEC -.Optional.-> AI
    STYLE -.Optional.-> AI
    AI -.Enhance.-> EDU
    
    EDU --> REPORT
    REPORT --> CLI
    REPORT --> WEB
    REPORT --> IDE
    
    style AI fill:#FFD700
    style ORCH fill:#87CEEB
    style REPORT fill:#90EE90
```

---

## Layered Architecture

```mermaid
graph TD
    subgraph "Layer 1: Interface"
        L1[CLI / Web / IDE]
    end
    
    subgraph "Layer 2: Orchestration"
        L2[Analysis Orchestrator]
    end
    
    subgraph "Layer 3: Parsing"
        L3[Language Parser<br/>Python | JavaScript | Java]
    end
    
    subgraph "Layer 4: Analysis"
        L4A[Bug Detector]
        L4B[Security Scanner]
        L4C[Style Checker]
    end
    
    subgraph "Layer 5: AI Enhancement"
        L5[AI Service Optional]
    end
    
    subgraph "Layer 6: Output"
        L6A[Educational Engine]
        L6B[Report Generator]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> L4A
    L3 --> L4B
    L3 --> L4C
    L4A --> L5
    L4B --> L5
    L4C --> L5
    L5 --> L6A
    L4A --> L6A
    L4B --> L6A
    L4C --> L6A
    L6A --> L6B
    L6B --> L1
    
    style L5 fill:#FFD700
    style L6B fill:#90EE90
```

---

## Component Interaction

```mermaid
graph LR
    A[User Input] --> B[Parser]
    B --> C[AST]
    C --> D[Analyzers]
    D --> E{AI?}
    E -->|Yes| F[AI Enhancement]
    E -->|No| G[Report]
    F --> G
    G --> H[User Output]
    
    style A fill:#90EE90
    style E fill:#FFD700
    style H fill:#FFB6C1
```

---

## Data Flow Architecture

```mermaid
flowchart TD
    INPUT[Code File] --> DETECT[Language Detection]
    DETECT --> PARSE[AST Generation]
    PARSE --> RULES[Rule Database]
    RULES --> FINDINGS[Findings List]
    FINDINGS --> AI{AI Available?}
    AI -->|Yes| ENHANCE[AI Enhancement]
    AI -->|No| FORMAT[Format Report]
    ENHANCE --> FORMAT
    FORMAT --> OUTPUT[Final Report]
    
    style INPUT fill:#90EE90
    style AI fill:#FFD700
    style OUTPUT fill:#FFB6C1
```
