# Print next steps
print_next_steps() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Claude project successfully initialized!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Project Structure Created:${NC}"
    echo "  .claude/       - Project configuration"
    echo "  docs/          - Requirements, BDD, ADRs"
    
    case "$TEMPLATE" in
        maui|dotnet-microservice)
            echo "  src/           - .NET solution directory"
            ;;
        *)
            echo "  tests/         - Test suites"
            echo "  src/           - Source code"
            ;;
    esac
    
    echo ""
    echo -e "${BOLD}Next Steps:${NC}"
    echo ""
    
    case "$TEMPLATE" in
        maui)
            echo "1. Create your .NET MAUI project in the src/ directory:"
            echo -e "   ${BLUE}cd src${NC}"
            echo -e "   ${BLUE}dotnet new maui -n YourApp${NC}"
            echo -e "   ${BLUE}dotnet new xunit -n YourApp.Tests${NC}"
            echo -e "   ${BLUE}dotnet new sln -n YourApp${NC}"
            echo -e "   ${BLUE}dotnet sln add YourApp/YourApp.csproj${NC}"
            echo -e "   ${BLUE}dotnet sln add YourApp.Tests/YourApp.Tests.csproj${NC}"
            echo -e "   ${BLUE}cd ..${NC}"
            echo ""
            echo "2. Open the project root (not src) in your IDE:"
            echo -e "   ${BLUE}code .${NC}  or  ${BLUE}cursor .${NC}"
            echo ""
            echo "3. Start gathering requirements:"
            echo -e "   ${BLUE}/gather-requirements${NC}"
            echo ""
            echo -e "${YELLOW}⚠️  Important:${NC} Always work from the project root, not from src/"
            echo "   The .claude directory should remain at the root level."
            ;;
        dotnet-microservice)
            echo "1. Create your .NET microservice in the src/ directory:"
            echo -e "   ${BLUE}cd src${NC}"
            echo -e "   ${BLUE}dotnet new webapi -n YourService${NC}"
            echo -e "   ${BLUE}dotnet new xunit -n YourService.Tests${NC}"
            echo -e "   ${BLUE}dotnet new sln -n YourService${NC}"
            echo -e "   ${BLUE}dotnet sln add YourService/YourService.csproj${NC}"
            echo -e "   ${BLUE}dotnet sln add YourService.Tests/YourService.Tests.csproj${NC}"
            echo -e "   ${BLUE}cd ..${NC}"
            echo ""
            echo "2. Open the project root (not src) in your IDE:"
            echo -e "   ${BLUE}code .${NC}  or  ${BLUE}cursor .${NC}"
            echo ""
            echo "3. Start gathering requirements:"
            echo -e "   ${BLUE}/gather-requirements${NC}"
            ;;
        *)
            echo "1. Open in your IDE with Claude:"
            echo -e "   ${BLUE}code .${NC}  or  ${BLUE}cursor .${NC}"
            echo ""
            echo "2. Start gathering requirements:"
            echo -e "   ${BLUE}/gather-requirements${NC}"
            ;;
    esac
    
    echo ""
    echo "3. Follow the workflow:"
    echo "   • Gather → Formalize → Generate → Implement → Test"
    echo ""
    echo -e "${BOLD}Available Commands in Claude:${NC}"
    echo "  /gather-requirements - Start requirements session"
    echo "  /formalize-ears     - Convert to EARS notation"
    echo "  /generate-bdd       - Create test scenarios"
    echo "  /execute-tests      - Run test suite"
    echo "  /update-state       - Update progress"
    echo ""
    echo -e "${BLUE}📚 Documentation:${NC} $CLAUDE_HOME/instructions/"
    echo -e "${BLUE}📋 Templates:${NC} .claude/templates/"
    echo -e "${BLUE}⚙️  Configuration:${NC} .claude/settings.json"
}
