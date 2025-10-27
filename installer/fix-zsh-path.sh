#!/bin/bash

# Fix PATH for zsh users after Agentecflow installation

echo "Fixing Agentecflow PATH configuration for zsh..."

# Check if zsh config exists
if [ ! -f "$HOME/.zshrc" ]; then
    echo "Creating ~/.zshrc..."
    touch "$HOME/.zshrc"
fi

# Check if already configured
if grep -q "\.agentecflow/bin" "$HOME/.zshrc" 2>/dev/null; then
    echo "✓ Agentecflow already configured in ~/.zshrc"
else
    echo "Adding Agentecflow to ~/.zshrc..."
    
    # Add to zsh config
    cat >> "$HOME/.zshrc" << 'EOF'

# Agentecflow
export PATH="$HOME/.agentecflow/bin:$PATH"
export AGENTECFLOW_HOME="$HOME/.agentecflow"

# Agentecflow completions (if available)
if [ -f "$HOME/.agentecflow/completions/agentecflow.bash" ]; then
    source "$HOME/.agentecflow/completions/agentecflow.bash"
fi
EOF
    
    echo "✓ Added Agentecflow to PATH in ~/.zshrc"
fi

echo ""
echo "✅ Configuration complete!"
echo ""
echo "Now run ONE of these commands:"
echo "  1. source ~/.zshrc                    (reload current terminal)"
echo "  2. Close and reopen your terminal     (start fresh)"
echo ""
echo "Then you can use:"
echo "  agentec-init dotnet-microservice"
echo ""

# Also test if the commands are available directly
if [ -f "$HOME/.agentecflow/bin/agentec-init" ]; then
    echo "✓ agentec-init is installed at: $HOME/.agentecflow/bin/agentec-init"
    echo ""
    echo "You can also run it directly right now without reloading:"
    echo "  ~/.agentecflow/bin/agentec-init dotnet-microservice"
fi
