# Agentic Flow - PowerShell Installation Script for Windows
# Complete Agentecflow Implementation - Enterprise Software Engineering Lifecycle System

param(
    [string]$InstallPath = "$env:USERPROFILE\.agenticflow",
    [switch]$TestMode = $false,
    [switch]$Force = $false
)

# Installation configuration
$AGENTICFLOW_VERSION = "2.0.0"
$INSTALL_DIR = $InstallPath
$CONFIG_DIR = "$env:USERPROFILE\.config\agenticflow"
$INSTALLER_DIR = Split-Path -Parent $PSScriptRoot

# Color output functions
function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColoredOutput "✓ $Message" -Color Green
}

function Write-Error {
    param([string]$Message)
    Write-ColoredOutput "✗ $Message" -Color Red
}

function Write-Warning {
    param([string]$Message)
    Write-ColoredOutput "⚠ $Message" -Color Yellow
}

function Write-Info {
    param([string]$Message)
    Write-ColoredOutput "ℹ $Message" -Color Blue
}

function Write-Header {
    Write-Host ""
    Write-ColoredOutput "╔════════════════════════════════════════════════════════╗" -Color Blue
    Write-ColoredOutput "║         Agentic Flow Installation System               ║" -Color Blue
    Write-ColoredOutput "║         Version: $AGENTICFLOW_VERSION (Windows)       ║" -Color Blue
    Write-ColoredOutput "╚════════════════════════════════════════════════════════╝" -Color Blue
    Write-Host ""
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."

    $missingDeps = @()

    # Check for required commands
    $requiredCommands = @("git", "powershell")
    foreach ($cmd in $requiredCommands) {
        if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
            $missingDeps += $cmd
        }
    }

    # Check for optional but recommended tools
    if (-not (Get-Command "node" -ErrorAction SilentlyContinue)) {
        Write-Warning "Node.js not found. Some features may be limited."
    } else {
        $nodeVersion = node --version
        Write-Success "Node.js found: $nodeVersion"
    }

    if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
        Write-Warning "Python not found. Some features may be limited."
    } else {
        $pythonVersion = python --version
        Write-Success "Python found: $pythonVersion"
    }

    if (-not (Get-Command "dotnet" -ErrorAction SilentlyContinue)) {
        Write-Warning ".NET CLI not found. .NET templates will be limited."
    } else {
        $dotnetVersion = dotnet --version
        Write-Success ".NET CLI found: $dotnetVersion"
    }

    if ($missingDeps.Count -gt 0) {
        Write-Error "Missing required dependencies: $($missingDeps -join ', ')"
        Write-Info "Please install missing dependencies and try again."

        Write-Info "Installation suggestions:"
        foreach ($dep in $missingDeps) {
            switch ($dep) {
                "git" { Write-Info "  Git: https://git-scm.com/download/win" }
                "node" { Write-Info "  Node.js: https://nodejs.org/en/download/" }
                "python" { Write-Info "  Python: https://www.python.org/downloads/" }
                "dotnet" { Write-Info "  .NET: https://dotnet.microsoft.com/download" }
            }
        }
        exit 1
    }

    Write-Success "All required prerequisites met"
}

# Backup existing installation
function Backup-ExistingInstallation {
    $existingDirs = @()

    if (Test-Path "$env:USERPROFILE\.agenticflow") { $existingDirs += ".agenticflow" }
    if (Test-Path "$env:USERPROFILE\.agentic-flow") { $existingDirs += ".agentic-flow" }
    if (Test-Path "$env:USERPROFILE\.claude") { $existingDirs += ".claude" }

    if ($existingDirs.Count -gt 0) {
        Write-Warning "Found existing installations: $($existingDirs -join ', ')"

        if (-not $Force) {
            $response = Read-Host "Create backup and continue? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Info "Installation cancelled"
                exit 0
            }
        }

        foreach ($dir in $existingDirs) {
            $fullPath = "$env:USERPROFILE\$dir"
            $backupDir = "$fullPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Write-Info "Creating backup of $dir at $backupDir"
            Move-Item $fullPath $backupDir
            Write-Success "Backup created: $backupDir"
        }
    }
}

# Create directory structure
function New-DirectoryStructure {
    Write-Info "Creating directory structure..."

    # Create main directories
    $directories = @(
        "$INSTALL_DIR\agents",
        "$INSTALL_DIR\bin",
        "$INSTALL_DIR\cache",
        "$INSTALL_DIR\commands",
        "$INSTALL_DIR\completions",
        "$INSTALL_DIR\docs",
        "$INSTALL_DIR\instructions",
        "$INSTALL_DIR\plugins",
        "$INSTALL_DIR\scripts",
        "$INSTALL_DIR\templates",
        "$INSTALL_DIR\versions",
        "$INSTALL_DIR\project-templates\epics",
        "$INSTALL_DIR\project-templates\features",
        "$INSTALL_DIR\project-templates\tasks",
        "$INSTALL_DIR\project-templates\portfolio",
        "$INSTALL_DIR\instructions\core",
        "$INSTALL_DIR\instructions\stacks",
        "$INSTALL_DIR\templates\default",
        "$INSTALL_DIR\templates\react",
        "$INSTALL_DIR\templates\python",
        "$INSTALL_DIR\templates\maui",
        "$INSTALL_DIR\templates\dotnet-microservice",
        "$INSTALL_DIR\templates\fullstack",
        "$INSTALL_DIR\templates\typescript-api",
        "$INSTALL_DIR\versions\$AGENTICFLOW_VERSION",
        "$CONFIG_DIR"
    )

    foreach ($dir in $directories) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    Write-Success "Directory structure created"
}

# Install global files
function Install-GlobalFiles {
    Write-Info "Installing global files..."

    # Copy instructions
    $instructionsPath = "$INSTALLER_DIR\global\instructions"
    if (Test-Path $instructionsPath) {
        Copy-Item -Path "$instructionsPath\*" -Destination "$INSTALL_DIR\instructions" -Recurse -Force
        Write-Success "Installed methodology instructions"
    }

    # Copy templates
    $templatesPath = "$INSTALLER_DIR\global\templates"
    if (Test-Path $templatesPath) {
        Get-ChildItem -Path $templatesPath -Directory | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination "$INSTALL_DIR\templates" -Recurse -Force
            New-Item -ItemType Directory -Path "$INSTALL_DIR\templates\$($_.Name)\agents" -Force | Out-Null
        }
        Write-Success "Installed project templates"
    }

    # Copy commands
    $commandsPath = "$INSTALLER_DIR\global\commands"
    if (Test-Path $commandsPath) {
        Copy-Item -Path "$commandsPath\*" -Destination "$INSTALL_DIR\commands" -Force
        Write-Success "Installed commands"
    }

    # Copy documentation
    $docsPath = "$INSTALLER_DIR\global\docs"
    if (Test-Path $docsPath) {
        Copy-Item -Path "$docsPath\*" -Destination "$INSTALL_DIR\docs" -Recurse -Force
        Write-Success "Installed documentation"
    }

    # Copy initialization script
    $initScript = "$INSTALLER_DIR\scripts\init-claude-project.sh"
    if (Test-Path $initScript) {
        Copy-Item -Path $initScript -Destination "$INSTALL_DIR\scripts\init-project.sh"
        Write-Success "Installed initialization script"
    }

    Write-Success "Global files installed"
}

# Install global agents
function Install-GlobalAgents {
    Write-Info "Installing global AI agents..."

    # Install core global agents
    $globalAgentsPath = "$INSTALLER_DIR\global\agents"
    if (Test-Path $globalAgentsPath) {
        Copy-Item -Path "$globalAgentsPath\*" -Destination "$INSTALL_DIR\agents" -Force
        Write-Success "Installed core global agents"
    }

    # Install stack-specific agents
    Get-ChildItem -Path "$INSTALLER_DIR\global\templates" -Directory | ForEach-Object {
        $agentsPath = "$($_.FullName)\agents"
        if (Test-Path $agentsPath) {
            $templateName = $_.Name
            $stackAgentsDir = "$INSTALL_DIR\stack-agents\$templateName"
            New-Item -ItemType Directory -Path $stackAgentsDir -Force | Out-Null
            Copy-Item -Path "$agentsPath\*" -Destination $stackAgentsDir -Force
            Write-Success "Installed $templateName stack agents"
        }
    }

    # Count agents
    $globalAgentCount = (Get-ChildItem -Path "$INSTALL_DIR\agents" -Filter "*.md").Count
    $stackAgentCount = (Get-ChildItem -Path "$INSTALL_DIR\stack-agents" -Filter "*.md" -Recurse).Count
    $totalAgents = $globalAgentCount + $stackAgentCount

    if ($totalAgents -gt 0) {
        Write-Success "Installed $totalAgents total agents ($globalAgentCount global + $stackAgentCount stack-specific)"

        if ($globalAgentCount -gt 0) {
            Write-Host "  Global agents:"
            Get-ChildItem -Path "$INSTALL_DIR\agents" -Filter "*.md" | ForEach-Object {
                Write-Host "    - $($_.BaseName)"
            }
        }
    } else {
        Write-Warning "No agents found to install"
        Write-Info "Creating placeholder agents..."

        # Create basic placeholder agents
        $placeholderAgents = @{
            "requirements-analyst" = "Specialist in gathering and formalizing requirements using EARS notation"
            "bdd-generator" = "Converts EARS requirements to BDD/Gherkin scenarios"
            "code-reviewer" = "Reviews code for quality, standards, and best practices"
            "test-orchestrator" = "Manages test execution and quality gates"
        }

        foreach ($agent in $placeholderAgents.GetEnumerator()) {
            $agentContent = @"
---
name: $($agent.Key)
description: $($agent.Value)
tools: Read, Write, Analyze
model: sonnet
---

You are a $($agent.Key) specialist.

## Your Responsibilities
1. Follow Agentic Flow methodology
2. Maintain quality standards
3. Ensure comprehensive coverage
4. Provide actionable insights
"@
            Set-Content -Path "$INSTALL_DIR\agents\$($agent.Key).md" -Value $agentContent
        }

        Write-Success "Created core placeholder agents"
    }

    # Create stack-agents directory structure
    $stackDirs = @("default", "react", "python", "maui", "dotnet-microservice", "fullstack", "typescript-api")
    foreach ($stackDir in $stackDirs) {
        New-Item -ItemType Directory -Path "$INSTALL_DIR\stack-agents\$stackDir" -Force | Out-Null
    }
}

# Create CLI commands (PowerShell modules)
function New-CLICommands {
    Write-Info "Creating CLI commands..."

    # Create main PowerShell module
    $moduleContent = @'
# Agentic Flow PowerShell Module

$AGENTICFLOW_HOME = "$env:USERPROFILE\.agenticflow"
$AGENTICFLOW_VERSION = "2.0.0"

function Invoke-AgenticFlow {
    param(
        [string]$Command,
        [string[]]$Arguments = @()
    )

    switch ($Command) {
        "init" {
            if ($Arguments.Count -eq 0) {
                & "$AGENTICFLOW_HOME\scripts\init-project.sh"
            } else {
                & "$AGENTICFLOW_HOME\scripts\init-project.sh" $Arguments[0]
            }
        }
        "doctor" {
            Write-Host "Running Agentic Flow diagnostics..." -ForegroundColor Blue
            Write-Host ""

            Write-Host "Installation:"
            if (Test-Path $AGENTICFLOW_HOME) {
                Write-Host "  ✓ Agentic Flow home: $AGENTICFLOW_HOME" -ForegroundColor Green

                $dirs = @("agents", "bin", "cache", "commands", "completions", "docs", "instructions", "plugins", "scripts", "templates", "versions")
                foreach ($dir in $dirs) {
                    if (Test-Path "$AGENTICFLOW_HOME\$dir") {
                        Write-Host "  ✓ Directory $dir exists" -ForegroundColor Green
                    } else {
                        Write-Host "  ✗ Directory $dir missing" -ForegroundColor Red
                    }
                }
            } else {
                Write-Host "  ✗ Agentic Flow home not found" -ForegroundColor Red
            }
        }
        "version" {
            Write-Host "Agentic Flow version $AGENTICFLOW_VERSION"
            Write-Host "Installation: $AGENTICFLOW_HOME"
        }
        "help" {
            Write-Host "Agentic Flow - AI-Powered Software Engineering Lifecycle System"
            Write-Host ""
            Write-Host "Usage: agenticflow <command> [options]"
            Write-Host ""
            Write-Host "Commands:"
            Write-Host "  init [template]     Initialize Agentic Flow in current directory"
            Write-Host "  doctor              Check system health and configuration"
            Write-Host "  version             Show version information"
            Write-Host "  help                Show this help message"
        }
        default {
            Write-Host "Unknown command: $Command" -ForegroundColor Red
            Write-Host "Run 'agenticflow help' for usage information"
        }
    }
}

# Create aliases
Set-Alias -Name agenticflow -Value Invoke-AgenticFlow
Set-Alias -Name af -Value Invoke-AgenticFlow

# Export functions
Export-ModuleMember -Function Invoke-AgenticFlow -Alias agenticflow, af
'@

    Set-Content -Path "$INSTALL_DIR\bin\AgenticFlow.psm1" -Value $moduleContent

    # Create batch wrapper for Windows compatibility
    $batchContent = @"
@echo off
powershell -ExecutionPolicy Bypass -Command "Import-Module '$INSTALL_DIR\bin\AgenticFlow.psm1'; Invoke-AgenticFlow %*"
"@

    Set-Content -Path "$INSTALL_DIR\bin\agenticflow.bat" -Value $batchContent

    Write-Success "Created CLI commands (agenticflow.bat, AgenticFlow.psm1)"
}

# Setup PowerShell profile integration
function Set-PowerShellIntegration {
    Write-Info "Setting up PowerShell integration..."

    $profilePath = $PROFILE.CurrentUserAllHosts
    if (-not $profilePath) {
        $profilePath = "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
    }

    # Create profile directory if it doesn't exist
    $profileDir = Split-Path -Path $profilePath
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    # Check if already configured
    $configLine = "Import-Module `"$INSTALL_DIR\bin\AgenticFlow.psm1`""

    if (Test-Path $profilePath) {
        $profileContent = Get-Content $profilePath -Raw
        if ($profileContent -match [regex]::Escape($configLine)) {
            Write-Info "PowerShell integration already configured"
            return
        }
    }

    # Add to profile
    $integrationContent = @"

# Agentic Flow
Import-Module "$INSTALL_DIR\bin\AgenticFlow.psm1"
`$env:PATH += ";$INSTALL_DIR\bin"
`$env:AGENTICFLOW_HOME = "$INSTALL_DIR"
"@

    Add-Content -Path $profilePath -Value $integrationContent

    Write-Success "PowerShell integration added to $profilePath"
    Write-Info "Please restart PowerShell or run: . `$PROFILE"
}

# Create global configuration
function New-GlobalConfiguration {
    Write-Info "Creating global configuration..."

    $configContent = @{
        version = $AGENTICFLOW_VERSION
        installation = @{
            home = $INSTALL_DIR
            installed = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        }
        defaults = @{
            template = "default"
            testing = @{
                coverage_threshold = 80
                quality_gates = $true
            }
            requirements = @{
                format = "EARS"
                validation = $true
            }
        }
        agents = @{
            core = @(
                "requirements-analyst",
                "bdd-generator",
                "code-reviewer",
                "test-orchestrator"
            )
        }
        plugins = @{
            auto_discover = $true
            directories = @(
                "$INSTALL_DIR\plugins"
            )
        }
    }

    $configContent | ConvertTo-Json -Depth 10 | Set-Content "$CONFIG_DIR\config.json"

    Write-Success "Global configuration created"
}

# Create version management
function New-VersionManagement {
    Write-Info "Setting up version management..."

    # Create version file
    Set-Content -Path "$INSTALL_DIR\versions\current" -Value $AGENTICFLOW_VERSION

    # Create version info
    $versionInfo = @{
        version = $AGENTICFLOW_VERSION
        released = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        features = @(
            "EARS requirements notation",
            "BDD/Gherkin generation",
            "Epic/Feature/Task hierarchy",
            "Portfolio management",
            "PM tool integration",
            "Quality gates",
            "Test orchestration",
            "10+ core AI agents",
            "7 project templates",
            "Agentecflow Stage 1-4 support"
        )
    }

    $versionInfo | ConvertTo-Json -Depth 5 | Set-Content "$INSTALL_DIR\versions\$AGENTICFLOW_VERSION\info.json"

    Write-Success "Version management configured"
}

# Setup cache directories
function Set-CacheDirectories {
    Write-Info "Setting up cache directories..."

    $cacheDirs = @("responses", "artifacts", "sessions")
    foreach ($dir in $cacheDirs) {
        New-Item -ItemType Directory -Path "$INSTALL_DIR\cache\$dir" -Force | Out-Null
    }

    $cacheConfig = @{
        max_size_mb = 100
        ttl_hours = 24
        auto_clean = $true
    }

    $cacheConfig | ConvertTo-Json | Set-Content "$INSTALL_DIR\cache\config.json"

    Write-Success "Cache directories created"
}

# Print installation summary
function Write-InstallationSummary {
    Write-Host ""
    Write-ColoredOutput "════════════════════════════════════════════════════════" -Color Green
    Write-ColoredOutput "✅ Agentic Flow installation complete!" -Color Green
    Write-ColoredOutput "════════════════════════════════════════════════════════" -Color Green
    Write-Host ""

    Write-ColoredOutput "Installation Summary:" -Color White
    Write-Host "  📁 Home Directory: $INSTALL_DIR"
    Write-Host "  🔧 Configuration: $CONFIG_DIR"
    Write-Host "  📦 Version: $AGENTICFLOW_VERSION"
    Write-Host ""

    Write-ColoredOutput "Installed Components:" -Color White

    # Count components
    $agentCount = (Get-ChildItem -Path "$INSTALL_DIR\agents" -Filter "*.md" -ErrorAction SilentlyContinue).Count
    $templateCount = (Get-ChildItem -Path "$INSTALL_DIR\templates" -Directory -ErrorAction SilentlyContinue).Count
    $commandCount = (Get-ChildItem -Path "$INSTALL_DIR\commands" -Filter "*.md" -ErrorAction SilentlyContinue).Count

    Write-Host "  🤖 AI Agents: $agentCount"
    Write-Host "  📋 Templates: $templateCount"
    Write-Host "  ⚡ Commands: $commandCount"
    Write-Host ""

    Write-ColoredOutput "Available Commands:" -Color White
    Write-Host "  • agenticflow init [template]  - Initialize a project"
    Write-Host "  • agenticflow doctor           - Check system health"
    Write-Host "  • af                           - Short for agenticflow"
    Write-Host ""

    Write-ColoredOutput "Available Templates:" -Color White
    $templateDescriptions = @{
        "default" = "Language-agnostic"
        "react" = "React with TypeScript"
        "python" = "Python with FastAPI"
        "maui" = ".NET MAUI mobile app"
        "dotnet-microservice" = ".NET microservice with FastEndpoints"
        "fullstack" = "React + Python"
        "typescript-api" = "NestJS TypeScript backend API"
    }

    Get-ChildItem -Path "$INSTALL_DIR\templates" -Directory | ForEach-Object {
        $name = $_.Name
        $description = $templateDescriptions[$name]
        if ($description) {
            Write-Host "  • $name - $description"
        } else {
            Write-Host "  • $name"
        }
    }

    Write-Host ""
    Write-ColoredOutput "Next Steps:" -Color Yellow
    Write-Host "  1. Restart PowerShell or run: . `$PROFILE"
    Write-Host "  2. Navigate to your project directory"
    Write-Host "  3. Run: agenticflow init [template-name]"
    Write-Host ""
    Write-ColoredOutput "Documentation: $INSTALL_DIR\docs" -Color Blue
    Write-ColoredOutput "Check health: agenticflow doctor" -Color Blue
}

# Main installation function
function Install-AgenticFlow {
    Write-Header

    Write-Info "Installing Agentic Flow to $INSTALL_DIR"
    Write-Host ""

    if ($TestMode) {
        Write-Warning "Running in test mode - some operations will be simulated"
    }

    try {
        Test-Prerequisites
        Backup-ExistingInstallation
        New-DirectoryStructure
        Install-GlobalFiles
        Install-GlobalAgents
        New-CLICommands
        Set-PowerShellIntegration
        New-GlobalConfiguration
        New-VersionManagement
        Set-CacheDirectories

        Write-InstallationSummary
    }
    catch {
        Write-Error "Installation failed: $($_.Exception.Message)"
        Write-Info "Please check the error and try again"
        exit 1
    }
}

# Run installation
Install-AgenticFlow