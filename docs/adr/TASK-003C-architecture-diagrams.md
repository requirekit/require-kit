# TASK-003C: Architecture Diagrams
## Visual Reference for Phase 2.7 & 2.8 Integration

**Created**: 2025-10-10
**Purpose**: Visual representation of system architecture

---

## 1. Complete Workflow Diagram

```mermaid
flowchart TD
    Start([User: /task-work TASK-XXX]) --> Phase1[Phase 1: Requirements Analysis]
    Phase1 --> Phase2[Phase 2: Implementation Planning]
    Phase2 --> Phase25[Phase 2.5: Architectural Review]

    Phase25 --> Phase27[Phase 2.7: Plan Generation + Complexity]

    Phase27 --> ParsePlan[Parse Plan → ImplementationPlan]
    ParsePlan --> CalcComplexity[Calculate Complexity Score 1-10]
    CalcComplexity --> DetectTriggers[Detect Force-Review Triggers]
    DetectTriggers --> DetermineMode{Determine ReviewMode}

    DetermineMode -->|Score 1-3, No Triggers| AutoProceed[AUTO_PROCEED]
    DetermineMode -->|Score 4-6, No Triggers| QuickOptional[QUICK_OPTIONAL]
    DetermineMode -->|Score 7-10 OR Triggers| FullRequired[FULL_REQUIRED]

    AutoProceed --> Phase28Auto[Phase 2.8: Auto-Proceed Path]
    QuickOptional --> Phase28Quick[Phase 2.8: Quick Review Path]
    FullRequired --> Phase28Full[Phase 2.8: Full Review Path]

    Phase28Auto --> DisplaySummary[Display Complexity Summary]
    DisplaySummary --> Phase3A[Phase 3: Implementation]

    Phase28Quick --> Countdown[10-Second Countdown]
    Countdown -->|Timeout| AutoApprove[Auto-Approve]
    Countdown -->|Enter Key| Escalate[Escalate to Full Review]
    Countdown -->|C Key| CancelQuick[Cancel → Backlog]
    AutoApprove --> Phase3B[Phase 3: Implementation]
    Escalate --> Phase28Full

    Phase28Full --> FullCheckpoint[Display Comprehensive Checkpoint]
    FullCheckpoint --> UserDecision{User Decision?}

    UserDecision -->|A: Approve| ApproveAction[Approve Plan]
    UserDecision -->|C: Cancel| CancelAction[Cancel → Backlog]
    UserDecision -->|M: Modify| ModifyStub[Modify COMING SOON]
    UserDecision -->|V: View| ViewStub[View COMING SOON]
    UserDecision -->|Q: Question| QuestionStub[Question COMING SOON]

    ApproveAction --> Phase3C[Phase 3: Implementation]
    ModifyStub --> FullCheckpoint
    ViewStub --> FullCheckpoint
    QuestionStub --> FullCheckpoint

    Phase3A --> Phase4[Phase 4: Testing]
    Phase3B --> Phase4
    Phase3C --> Phase4

    Phase4 --> Phase5[Phase 5: Code Review]
    Phase5 --> Complete([Task Complete])

    CancelQuick --> Backlog[(tasks/backlog/)]
    CancelAction --> Backlog

    style Phase27 fill:#ffeb3b,stroke:#333,stroke-width:3px
    style Phase28Auto fill:#4caf50,stroke:#333,stroke-width:3px
    style Phase28Quick fill:#ff9800,stroke:#333,stroke-width:3px
    style Phase28Full fill:#f44336,stroke:#333,stroke-width:3px
    style Phase3A fill:#2196f3,stroke:#333,stroke-width:2px
    style Phase3B fill:#2196f3,stroke:#333,stroke-width:2px
    style Phase3C fill:#2196f3,stroke:#333,stroke-width:2px
```

---

## 2. Phase 2.7 Detail Diagram

```mermaid
flowchart TD
    Input[Phase 2 Output Free-Form Plan] --> DetectStack{Detect Technology Stack}

    DetectStack -->|Python| PythonParser[PythonPlanParser]
    DetectStack -->|React| ReactParser[ReactPlanParser]
    DetectStack -->|TypeScript| TSParser[TypeScriptPlanParser]
    DetectStack -->|.NET| DotNetParser[DotNetPlanParser]
    DetectStack -->|Unknown| GenericParser[GenericPlanParser]

    PythonParser --> StructuredPlan[ImplementationPlan Object]
    ReactParser --> StructuredPlan
    TSParser --> StructuredPlan
    DotNetParser --> StructuredPlan
    GenericParser --> StructuredPlan

    StructuredPlan --> CalcFactors[Calculate Complexity Factors]

    CalcFactors --> FileFactor[File Complexity 0-3 points]
    CalcFactors --> PatternFactor[Pattern Familiarity 0-2 points]
    CalcFactors --> RiskFactor[Risk Level 0-3 points]
    CalcFactors --> DepFactor[Dependencies 0-2 points]

    FileFactor --> AggregateFinal[Aggregate Total Score 1-10]
    PatternFactor --> AggregateFinal
    RiskFactor --> AggregateFinal
    DepFactor --> AggregateFinal

    AggregateFinal --> CheckTriggers{Force-Review Triggers?}

    CheckTriggers -->|Security Keywords| ForceReview[FULL_REQUIRED]
    CheckTriggers -->|Breaking Changes| ForceReview
    CheckTriggers -->|Schema Changes| ForceReview
    CheckTriggers -->|Hotfix Flag| ForceReview
    CheckTriggers -->|User --review Flag| ForceReview
    CheckTriggers -->|None| CheckScore{Total Score?}

    CheckScore -->|1-3| Auto[AUTO_PROCEED]
    CheckScore -->|4-6| Quick[QUICK_OPTIONAL]
    CheckScore -->|7-10| Full[FULL_REQUIRED]

    ForceReview --> SaveState[Save State to Filesystem]
    Auto --> SaveState
    Quick --> SaveState
    Full --> SaveState

    SaveState --> PlanFile[docs/state/TASK-XXX/implementation_plan_v1.json]
    SaveState --> ComplexityFile[docs/state/TASK-XXX/complexity_score_v1.json]

    PlanFile --> Output[Return ComplexityScore + ReviewMode]
    ComplexityFile --> Output

    Output --> Phase28[Phase 2.8 Routing]

    style StructuredPlan fill:#4caf50,stroke:#333,stroke-width:2px
    style AggregateFinal fill:#ff9800,stroke:#333,stroke-width:2px
    style SaveState fill:#2196f3,stroke:#333,stroke-width:2px
    style Output fill:#9c27b0,stroke:#333,stroke-width:3px
```

---

## 3. Phase 2.8 State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> Phase27Output: ComplexityScore calculated

    Phase27Output --> AUTO_PROCEED: Score 1-3, No triggers
    Phase27Output --> QUICK_OPTIONAL: Score 4-6, No triggers
    Phase27Output --> FULL_REQUIRED: Score 7-10 OR Triggers

    AUTO_PROCEED --> DisplaySummary: Display complexity summary
    DisplaySummary --> Phase3: Auto-proceed (no user input)

    QUICK_OPTIONAL --> QuickReview: Display summary + 10s countdown
    QuickReview --> Phase3: Timeout (no input)
    QuickReview --> FULL_REQUIRED: User presses Enter
    QuickReview --> Backlog: User presses C (cancel)

    FULL_REQUIRED --> FullCheckpoint: Display comprehensive review
    FullCheckpoint --> WaitDecision: Prompt for [A/M/V/Q/C]

    WaitDecision --> Phase3: User presses A (approve)
    WaitDecision --> Backlog: User presses C (cancel) + confirm
    WaitDecision --> ModifyMode: User presses M (modify)
    WaitDecision --> ViewMode: User presses V (view)
    WaitDecision --> QAMode: User presses Q (question)

    ModifyMode --> Phase27Output: Modified plan → Re-calculate
    ViewMode --> WaitDecision: Show plan in pager
    QAMode --> WaitDecision: Q&A session

    Phase3 --> [*]: Proceed to implementation
    Backlog --> [*]: Task moved to backlog

    note right of AUTO_PROCEED
        Score: 1-3
        No triggers
        Example: 1 file, no patterns, no risks
    end note

    note right of QUICK_OPTIONAL
        Score: 4-6
        No triggers
        Example: 4 files, 1 pattern, low risk
    end note

    note right of FULL_REQUIRED
        Score: 7-10 OR
        Any force-review trigger
        Example: 8 files, security, breaking changes
    end note
```

---

## 4. Component Architecture Diagram

```mermaid
graph TB
    subgraph "Task Work Command (task-work.md)"
        TaskWork[task-work.md Entry Point]
    end

    subgraph "Task Manager Orchestrator (task-manager.md)"
        TaskManager[Task Manager Agent]
        Phase27Orch[Phase 2.7 Orchestrator]
        Phase28Orch[Phase 2.8 Orchestrator]
    end

    subgraph "Phase 2.7 Components"
        TaskContext[TaskContext Shared State]
        PlanParser[PlanParser Factory]
        ComplexityCalc[ComplexityCalculator]

        PlanParser --> StackParsers[Stack-Specific Parsers]
        StackParsers --> PythonP[PythonPlanParser]
        StackParsers --> ReactP[ReactPlanParser]
        StackParsers --> GenericP[GenericPlanParser]
    end

    subgraph "Phase 2.8 Components"
        ReviewSM[ReviewStateMachine]
        ReviewCommands[ReviewCommands]
        Phase28Handler[Phase28Handler]

        ReviewCommands --> ApproveCmd[ApproveCommand]
        ReviewCommands --> CancelCmd[CancelCommand]
        ReviewCommands --> ModifyCmd[ModifyCommand STUB]
    end

    subgraph "UI Components (from TASK-003B-1)"
        QuickReview[QuickReviewHandler]
        FullReview[FullReviewHandler]
        Countdown[countdown_timer]

        QuickReview --> Countdown
    end

    subgraph "Data Models (from TASK-003A)"
        Models[ComplexityScore]
        Models2[ImplementationPlan]
        Models3[ReviewMode Enum]
    end

    subgraph "Filesystem State"
        StateFiles[(docs/state/TASK-XXX/)]
        StateFiles --> PlanJSON[implementation_plan_v1.json]
        StateFiles --> ComplexityJSON[complexity_score_v1.json]
        StateFiles --> SessionJSON[review_session.json]
    end

    TaskWork --> TaskManager
    TaskManager --> Phase27Orch
    Phase27Orch --> TaskContext
    Phase27Orch --> PlanParser
    Phase27Orch --> ComplexityCalc

    PlanParser --> Models2
    ComplexityCalc --> Models
    ComplexityCalc --> Models3

    Phase27Orch --> StateFiles

    TaskManager --> Phase28Orch
    Phase28Orch --> ReviewSM
    Phase28Orch --> Phase28Handler
    Phase28Handler --> QuickReview
    Phase28Handler --> FullReview

    Phase28Handler --> ReviewCommands
    Phase28Orch --> StateFiles

    style TaskWork fill:#e1bee7,stroke:#333,stroke-width:3px
    style TaskManager fill:#ce93d8,stroke:#333,stroke-width:2px
    style Phase27Orch fill:#ffeb3b,stroke:#333,stroke-width:3px
    style Phase28Orch fill:#ff9800,stroke:#333,stroke-width:3px
    style StateFiles fill:#2196f3,stroke:#333,stroke-width:2px
```

---

## 5. Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant TaskWork as task-work.md
    participant TaskMgr as task-manager.md
    participant Phase27 as Phase27Handler
    participant Parser as PlanParser
    participant Calculator as ComplexityCalculator
    participant Phase28 as Phase28Handler
    participant QuickUI as QuickReviewHandler
    participant FullUI as FullReviewHandler
    participant FS as Filesystem (docs/state/)

    User->>TaskWork: /task-work TASK-042
    TaskWork->>TaskMgr: Invoke Phase 1 (Requirements)
    TaskMgr-->>TaskWork: Requirements analyzed

    TaskWork->>TaskMgr: Invoke Phase 2 (Planning)
    TaskMgr-->>TaskWork: Plan created (free-form)

    TaskWork->>TaskMgr: Invoke Phase 2.5 (Arch Review)
    TaskMgr-->>TaskWork: Architecture approved

    rect rgb(255, 235, 59)
        Note over TaskWork,Phase27: Phase 2.7: Plan Generation + Complexity
        TaskWork->>TaskMgr: Invoke Phase 2.7
        TaskMgr->>Phase27: Execute Phase 2.7
        Phase27->>Parser: Parse free-form plan
        Parser-->>Phase27: ImplementationPlan object
        Phase27->>Calculator: Calculate complexity
        Calculator-->>Phase27: ComplexityScore (score + mode)
        Phase27->>FS: Save plan + complexity
        FS-->>Phase27: State saved
        Phase27-->>TaskMgr: Return ComplexityScore
        TaskMgr-->>TaskWork: Phase 2.7 complete
    end

    rect rgb(255, 152, 0)
        Note over TaskWork,FullUI: Phase 2.8: Human Plan Checkpoint
        TaskWork->>TaskMgr: Invoke Phase 2.8
        TaskMgr->>Phase28: Execute Phase 2.8

        alt ReviewMode = AUTO_PROCEED
            Phase28->>User: Display summary
            Phase28-->>TaskMgr: Auto-approved
        else ReviewMode = QUICK_OPTIONAL
            Phase28->>QuickUI: Show quick review
            QuickUI->>User: Display + 10s countdown
            alt Timeout
                User-->>QuickUI: (no input)
                QuickUI-->>Phase28: Auto-approved
            else Escalate
                User->>QuickUI: Press Enter
                QuickUI->>FullUI: Escalate to full
                FullUI->>User: Display checkpoint
                User->>FullUI: [A]pprove
                FullUI-->>Phase28: Approved
            end
        else ReviewMode = FULL_REQUIRED
            Phase28->>FullUI: Show full review
            FullUI->>User: Display checkpoint
            User->>FullUI: [A]pprove
            FullUI-->>Phase28: Approved
        end

        Phase28->>FS: Update task metadata
        FS-->>Phase28: Metadata updated
        Phase28-->>TaskMgr: Proceed to Phase 3
        TaskMgr-->>TaskWork: Phase 2.8 complete
    end

    rect rgb(33, 150, 243)
        Note over TaskWork,User: Phase 3: Implementation
        TaskWork->>TaskMgr: Invoke Phase 3
        TaskMgr-->>TaskWork: Implementation complete
    end

    TaskWork->>User: Task complete
```

---

## 6. Complexity Scoring Formula Diagram

```mermaid
flowchart LR
    subgraph "Factor 1: File Complexity (0-3 points)"
        F1[File Count]
        F1 -->|1-2 files| F1A[0.5 points]
        F1 -->|3-5 files| F1B[1.5 points]
        F1 -->|6-8 files| F1C[2.5 points]
        F1 -->|9+ files| F1D[3.0 points]
    end

    subgraph "Factor 2: Pattern Familiarity (0-2 points)"
        F2[Design Patterns]
        F2 -->|None/Simple| F2A[0 points]
        F2 -->|Common 1-2| F2B[1 point]
        F2 -->|Advanced 3+| F2C[2 points]
    end

    subgraph "Factor 3: Risk Level (0-3 points)"
        F3[Risk Indicators]
        F3 -->|None| F3A[0 points]
        F3 -->|Low| F3B[1 point]
        F3 -->|Medium| F3C[2 points]
        F3 -->|High| F3D[3 points]
    end

    subgraph "Factor 4: Dependencies (0-2 points)"
        F4[External Deps]
        F4 -->|0-1 deps| F4A[0 points]
        F4 -->|2-3 deps| F4B[1 point]
        F4 -->|4+ deps| F4C[2 points]
    end

    F1A --> Total[Total Score]
    F1B --> Total
    F1C --> Total
    F1D --> Total
    F2A --> Total
    F2B --> Total
    F2C --> Total
    F3A --> Total
    F3B --> Total
    F3C --> Total
    F3D --> Total
    F4A --> Total
    F4B --> Total
    F4C --> Total

    Total -->|1-3 points| Route1[AUTO_PROCEED]
    Total -->|4-6 points| Route2[QUICK_OPTIONAL]
    Total -->|7-10 points| Route3[FULL_REQUIRED]

    Triggers[Force-Review Triggers] -.Override.-> Route3

    style Total fill:#ff9800,stroke:#333,stroke-width:3px
    style Route1 fill:#4caf50,stroke:#333,stroke-width:2px
    style Route2 fill:#ffeb3b,stroke:#333,stroke-width:2px
    style Route3 fill:#f44336,stroke:#333,stroke-width:2px
    style Triggers fill:#9c27b0,stroke:#333,stroke-width:2px
```

---

## 7. Modification Loop Diagram

```mermaid
flowchart TD
    Start[User in Full Review] --> Choice{User Decision?}

    Choice -->|A: Approve| Approve[Approve Plan]
    Choice -->|C: Cancel| Cancel[Cancel Task]
    Choice -->|M: Modify| CheckCount{Modification Count?}

    CheckCount -->|< 5| EnterModify[Enter ModificationSession]
    CheckCount -->|>= 5| ForceDecision[Force Decision - No more modifications]

    ForceDecision --> Choice

    EnterModify --> Interactive[Interactive Plan Editor]
    Interactive --> AddFiles[Add/Remove Files?]
    Interactive --> AddDeps[Add/Remove Dependencies?]
    Interactive --> UpdateMeta[Update Metadata?]

    AddFiles --> ReviewChanges{Review Changes Summary}
    AddDeps --> ReviewChanges
    UpdateMeta --> ReviewChanges

    ReviewChanges -->|Apply| ApplyMod[Apply Modifications]
    ReviewChanges -->|Cancel| CancelMod[Cancel Modifications]

    CancelMod --> Start

    ApplyMod --> CreateVersion[Create Plan Version v2]
    CreateVersion --> RecalcComplexity[Re-calculate Complexity]
    RecalcComplexity --> SaveNewState[Save State v2]

    SaveNewState --> IncrementCount[Increment Modification Count]
    IncrementCount --> RedisplayCheckpoint[Re-display Full Checkpoint]

    RedisplayCheckpoint --> Start

    Approve --> Phase3[Phase 3: Implementation]
    Cancel --> Backlog[(tasks/backlog/)]

    style EnterModify fill:#9c27b0,stroke:#333,stroke-width:2px
    style ApplyMod fill:#ff9800,stroke:#333,stroke-width:2px
    style RecalcComplexity fill:#ffeb3b,stroke:#333,stroke-width:2px
    style RedisplayCheckpoint fill:#f44336,stroke:#333,stroke-width:2px
    style CheckCount fill:#e91e63,stroke:#333,stroke-width:3px
```

---

## 8. Error Handling Flow Diagram

```mermaid
flowchart TD
    Phase27Start[Phase 2.7 Start] --> TryParse{Try Parse Plan}

    TryParse -->|Success| ParsedPlan[ImplementationPlan Created]
    TryParse -->|Error| ParseError[PlanParsingError]

    ParseError --> Fallback1[Try GenericPlanParser]
    Fallback1 -->|Success| ParsedPlan
    Fallback1 -->|Error| EscalateReview1[Escalate to FULL_REQUIRED]

    ParsedPlan --> TryCalc{Try Calculate Complexity}

    TryCalc -->|Success| ComplexityScore[ComplexityScore Created]
    TryCalc -->|Error| CalcError[ComplexityCalculationError]

    CalcError --> EscalateReview2[Escalate to FULL_REQUIRED]

    ComplexityScore --> TrySave{Try Save State}
    EscalateReview1 --> TrySave
    EscalateReview2 --> TrySave

    TrySave -->|Success| StateFiles[State Saved]
    TrySave -->|Error| LogError[Log Error - Continue Anyway]

    StateFiles --> Phase28[Phase 2.8 Start]
    LogError --> Phase28

    Phase28 --> TryDisplay{Try Display UI}

    TryDisplay -->|Success| UserInteraction[User Interaction]
    TryDisplay -->|Error| DisplayError[UIRenderError]

    DisplayError --> EscalateReview3[Escalate to FullReview]

    UserInteraction -->|Ctrl+C| InterruptHandler[KeyboardInterrupt]
    InterruptHandler --> ConfirmCancel{Confirm Cancellation?}

    ConfirmCancel -->|Yes| MoveBacklog[Move to Backlog]
    ConfirmCancel -->|No| UserInteraction

    UserInteraction -->|Success| Decision[User Decision Made]

    Decision --> UpdateMetadata{Try Update Task Metadata}

    UpdateMetadata -->|Success| MetadataUpdated[Metadata Updated]
    UpdateMetadata -->|Error| LogMetadataError[Log Error - Phase 3 Still Proceeds]

    MetadataUpdated --> Phase3[Phase 3: Implementation]
    LogMetadataError --> Phase3

    MoveBacklog --> Exit[Exit Workflow]

    style ParseError fill:#f44336,stroke:#333,stroke-width:2px
    style CalcError fill:#f44336,stroke:#333,stroke-width:2px
    style DisplayError fill:#f44336,stroke:#333,stroke-width:2px
    style EscalateReview1 fill:#ff9800,stroke:#333,stroke-width:3px
    style EscalateReview2 fill:#ff9800,stroke:#333,stroke-width:3px
    style EscalateReview3 fill:#ff9800,stroke:#333,stroke-width:3px
    style InterruptHandler fill:#9c27b0,stroke:#333,stroke-width:2px
```

---

## 9. State File Structure Diagram

```mermaid
graph TD
    Root[docs/state/] --> TaskDir[TASK-XXX/]

    TaskDir --> PlanV1[implementation_plan_v1.json]
    TaskDir --> PlanV2[implementation_plan_v2.json]
    TaskDir --> ComplexityV1[complexity_score_v1.json]
    TaskDir --> ComplexityV2[complexity_score_v2.json]
    TaskDir --> ReviewSession[review_session.json]
    TaskDir --> ModSessions[modification_sessions/]
    TaskDir --> QASessions[qa_sessions/]

    ModSessions --> ModSession1[session_001.json]
    ModSessions --> ModSession2[session_002.json]

    QASessions --> QASession1[qa_001.json]
    QASessions --> QASession2[qa_002.json]

    PlanV1 --> PlanStructure[/"
    {
      'task_id': 'TASK-XXX',
      'files_to_create': [...],
      'patterns_used': [...],
      'external_dependencies': [...],
      'estimated_loc': 250,
      'risk_indicators': [...],
      'phases': [...],
      'raw_plan': '...'
    }
    "/]

    ComplexityV1 --> ComplexityStructure[/"
    {
      'total_score': 5,
      'factor_scores': [
        {'factor_name': 'file_complexity', 'score': 1.5, ...},
        ...
      ],
      'forced_review_triggers': [],
      'review_mode': 'quick_optional',
      'calculation_timestamp': '...'
    }
    "/]

    ReviewSession --> SessionStructure[/"
    {
      'task_id': 'TASK-XXX',
      'started_at': '...',
      'completed_at': '...',
      'review_mode': 'quick_optional',
      'escalated': false,
      'decisions': [
        {'action': 'timeout', 'timestamp': '...'}
      ]
    }
    "/]

    style Root fill:#2196f3,stroke:#333,stroke-width:3px
    style TaskDir fill:#64b5f6,stroke:#333,stroke-width:2px
    style PlanV1 fill:#4caf50,stroke:#333,stroke-width:2px
    style ComplexityV1 fill:#ff9800,stroke:#333,stroke-width:2px
    style ReviewSession fill:#9c27b0,stroke:#333,stroke-width:2px
```

---

## 10. Technology Stack Integration Diagram

```mermaid
graph LR
    subgraph "Planning Agents (Existing)"
        PythonPlanner[python-api-specialist]
        ReactPlanner[react-state-specialist]
        TSPlanner[nestjs-api-specialist]
        MAUIPlanner[maui-usecase-specialist]
    end

    subgraph "Phase 2.7: Plan Parsing"
        PlanParserFactory[PlanParser Factory]

        PlanParserFactory --> PythonParser[PythonPlanParser]
        PlanParserFactory --> ReactParser[ReactPlanParser]
        PlanParserFactory --> TSParser[TypeScriptPlanParser]
        PlanParserFactory --> DotNetParser[DotNetPlanParser]
        PlanParserFactory --> GenericParser[GenericPlanParser]
    end

    subgraph "Universal Data Models"
        ImplementationPlan[ImplementationPlan]
        ComplexityScore[ComplexityScore]
    end

    subgraph "Phase 2.8: Universal Review"
        QuickReview[QuickReviewHandler]
        FullReview[FullReviewHandler]
    end

    PythonPlanner -->|Free-form Plan| PlanParserFactory
    ReactPlanner -->|Free-form Plan| PlanParserFactory
    TSPlanner -->|Free-form Plan| PlanParserFactory
    MAUIPlanner -->|Free-form Plan| PlanParserFactory

    PythonParser --> ImplementationPlan
    ReactParser --> ImplementationPlan
    TSParser --> ImplementationPlan
    DotNetParser --> ImplementationPlan
    GenericParser --> ImplementationPlan

    ImplementationPlan --> ComplexityCalc[ComplexityCalculator]
    ComplexityCalc --> ComplexityScore

    ComplexityScore --> QuickReview
    ComplexityScore --> FullReview

    QuickReview --> Phase3[Phase 3: Implementation]
    FullReview --> Phase3

    style PlanParserFactory fill:#ffeb3b,stroke:#333,stroke-width:3px
    style ImplementationPlan fill:#4caf50,stroke:#333,stroke-width:3px
    style ComplexityScore fill:#ff9800,stroke:#333,stroke-width:3px
```

---

## Legend

### Color Coding

- 🟡 **Yellow** (#ffeb3b): Phase 2.7 components
- 🟠 **Orange** (#ff9800): Phase 2.8 components / Medium complexity
- 🟢 **Green** (#4caf50): Success paths / Auto-proceed
- 🔴 **Red** (#f44336): Full review / High complexity
- 🔵 **Blue** (#2196f3): Phase 3 / State storage
- 🟣 **Purple** (#9c27b0): Special actions / Modification

### Shape Meanings

- **Rectangles**: Processes/Components
- **Diamonds**: Decision points
- **Rounded rectangles**: Start/End states
- **Cylinders**: Data storage
- **Dashed lines**: Optional/Override paths

---

## How to Use These Diagrams

1. **Workflow Diagram (#1)**: High-level overview for stakeholders
2. **Phase 2.7 Detail (#2)**: For implementing Phase 2.7 components
3. **State Machine (#3)**: For understanding Phase 2.8 routing logic
4. **Component Architecture (#4)**: For understanding system structure
5. **Data Flow (#5)**: For understanding sequence of operations
6. **Complexity Scoring (#6)**: For understanding scoring algorithm
7. **Modification Loop (#7)**: For implementing future modification feature
8. **Error Handling (#8)**: For implementing robust error handling
9. **State Files (#9)**: For understanding filesystem structure
10. **Stack Integration (#10)**: For adding new technology stacks

---

**Document Version**: 1.0
**Created**: 2025-10-10
**Format**: Mermaid.js diagrams (render in GitHub, GitLab, or Mermaid Live Editor)
