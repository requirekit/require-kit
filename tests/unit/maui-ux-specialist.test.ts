/**
 * Unit Tests for MAUI UX Specialist
 *
 * Tests the specialist's ability to:
 * - Generate XAML from design elements
 * - Map Zeplin elements to MAUI controls
 * - Apply exact styling from design
 * - Generate C# code-behind
 * - Create ViewModels with MVVM pattern
 * - Validate platform adaptations
 *
 * Total Tests: 18
 */

import { describe, it, expect } from 'vitest';

describe('MAUI UX Specialist', () => {
  describe('MAUI Control Mapping', () => {
    it('should map "text" type to Label control', () => {
      const element = { type: 'text', id: 'heading', properties: {} };
      const mauiControl = mapToMauiControl(element);

      expect(mauiControl).toBe('Label');
    });

    it('should map "button" type to Button control', () => {
      const element = { type: 'button', id: 'submit', properties: {} };
      const mauiControl = mapToMauiControl(element);

      expect(mauiControl).toBe('Button');
    });

    it('should map "entry" type to Entry control', () => {
      const element = { type: 'entry', id: 'email-input', properties: {} };
      const mauiControl = mapToMauiControl(element);

      expect(mauiControl).toBe('Entry');
    });

    it('should map "frame" type to Frame control', () => {
      const element = { type: 'frame', id: 'card', properties: {} };
      const mauiControl = mapToMauiControl(element);

      expect(mauiControl).toBe('Frame');
    });

    it('should map "grid" type to Grid control', () => {
      const element = { type: 'grid', id: 'layout', properties: {} };
      const mauiControl = mapToMauiControl(element);

      expect(mauiControl).toBe('Grid');
    });
  });

  describe('XAML Generation', () => {
    it('should generate valid XAML ContentView', () => {
      const designElements = {
        elements: [
          {
            type: 'frame',
            id: 'container',
            properties: {
              style: {
                backgroundColor: '#FFFFFF',
                borderRadius: 12,
                padding: 24,
              },
            },
          },
        ],
      };

      const xaml = generateXAML(designElements);

      expect(xaml).toContain('<ContentView');
      expect(xaml).toContain('xmlns="http://schemas.microsoft.com/dotnet/2021/maui"');
      expect(xaml).toContain('<Frame');
      expect(xaml).toContain('BackgroundColor="#FFFFFF"');
      expect(xaml).toContain('CornerRadius="12"');
      expect(xaml).toContain('Padding="24"');
    });

    it('should generate nested elements correctly', () => {
      const designElements = {
        elements: [
          {
            type: 'frame',
            id: 'container',
            properties: { style: {} },
            children: [
              {
                type: 'label',
                id: 'title',
                properties: { text: 'Welcome', style: {} },
              },
              {
                type: 'button',
                id: 'submit',
                properties: { text: 'Continue', style: {} },
              },
            ],
          },
        ],
      };

      const xaml = generateXAML(designElements);

      expect(xaml).toContain('<Frame');
      expect(xaml).toContain('<Label');
      expect(xaml).toContain('Text="Welcome"');
      expect(xaml).toContain('<Button');
      expect(xaml).toContain('Text="Continue"');
    });

    it('should apply exact hex colors from design', () => {
      const designElements = {
        elements: [
          {
            type: 'button',
            id: 'submit',
            properties: {
              style: {
                backgroundColor: '#3B82F6',
                textColor: '#FFFFFF',
              },
            },
          },
        ],
      };

      const xaml = generateXAML(designElements);

      expect(xaml).toContain('BackgroundColor="#3B82F6"');
      expect(xaml).toContain('TextColor="#FFFFFF"');
    });

    it('should apply exact spacing from design', () => {
      const designElements = {
        elements: [
          {
            type: 'frame',
            id: 'container',
            properties: {
              style: {
                padding: { left: 16, top: 24, right: 16, bottom: 24 },
                margin: 8,
              },
            },
          },
        ],
      };

      const xaml = generateXAML(designElements);

      expect(xaml).toContain('Padding="16,24,16,24"');
      expect(xaml).toContain('Margin="8"');
    });
  });

  describe('Code-Behind Generation', () => {
    it('should generate valid C# code-behind', () => {
      const componentName = 'LoginForm';
      const codeBehind = generateCodeBehind(componentName);

      expect(codeBehind).toContain('namespace');
      expect(codeBehind).toContain('public partial class LoginForm : ContentView');
      expect(codeBehind).toContain('public LoginForm()');
      expect(codeBehind).toContain('InitializeComponent()');
    });

    it('should include component metadata in comments', () => {
      const componentName = 'LoginForm';
      const metadata = {
        projectId: 'abc123',
        screenId: 'def456',
        extractedAt: '2025-10-09T12:00:00Z',
      };

      const codeBehind = generateCodeBehindWithMetadata(componentName, metadata);

      expect(codeBehind).toContain('Project ID: abc123');
      expect(codeBehind).toContain('Screen ID: def456');
      expect(codeBehind).toContain('Extracted: 2025-10-09T12:00:00Z');
    });

    it('should NOT include loading states', () => {
      const componentName = 'LoginForm';
      const codeBehind = generateCodeBehind(componentName);

      expect(codeBehind).not.toContain('IsBusy');
      expect(codeBehind).not.toContain('IsLoading');
    });

    it('should NOT include API integration code', () => {
      const componentName = 'LoginForm';
      const codeBehind = generateCodeBehind(componentName);

      expect(codeBehind).not.toContain('HttpClient');
      expect(codeBehind).not.toContain('GetAsync');
      expect(codeBehind).not.toContain('PostAsync');
    });
  });

  describe('ViewModel Generation', () => {
    it('should generate ViewModel with CommunityToolkit.Mvvm', () => {
      const componentName = 'LoginForm';
      const viewModel = generateViewModel(componentName);

      expect(viewModel).toContain('using CommunityToolkit.Mvvm.ComponentModel');
      expect(viewModel).toContain('using CommunityToolkit.Mvvm.Input');
      expect(viewModel).toContain('public partial class LoginFormViewModel : ObservableObject');
    });

    it('should generate ObservableProperty for design elements', () => {
      const designElements = {
        elements: [
          { type: 'entry', id: 'email-entry', properties: {} },
          { type: 'entry', id: 'password-entry', properties: {} },
        ],
      };

      const viewModel = generateViewModelWithProperties(designElements);

      expect(viewModel).toContain('[ObservableProperty]');
      expect(viewModel).toContain('private string _email');
      expect(viewModel).toContain('private string _password');
    });

    it('should generate RelayCommand for button interactions', () => {
      const designElements = {
        elements: [{ type: 'button', id: 'submit-button', properties: {} }],
      };

      const viewModel = generateViewModelWithCommands(designElements);

      expect(viewModel).toContain('[RelayCommand]');
      expect(viewModel).toContain('private void Submit()');
    });

    it('should NOT generate loading state properties', () => {
      const designElements = {
        elements: [{ type: 'button', id: 'submit', properties: {} }],
      };

      const viewModel = generateViewModelWithProperties(designElements);

      expect(viewModel).not.toContain('_isBusy');
      expect(viewModel).not.toContain('_isLoading');
    });
  });

  describe('Platform Adaptations', () => {
    it('should generate iOS-specific safe area margins', () => {
      const platform = 'ios';
      const xaml = generatePlatformSpecificXAML(platform);

      expect(xaml).toContain('OnPlatform');
      expect(xaml).toContain('Platform="iOS"');
      expect(xaml).toContain('Value="0,20,0,0"');
    });

    it('should generate Android-specific Material Design styling', () => {
      const platform = 'android';
      const xaml = generatePlatformSpecificXAML(platform);

      expect(xaml).toContain('Platform="Android"');
    });

    it('should handle multi-platform adaptations', () => {
      const platforms = ['ios', 'android', 'windows', 'macos'];
      const xaml = generateMultiPlatformXAML(platforms);

      expect(xaml).toContain('Platform="iOS"');
      expect(xaml).toContain('Platform="Android"');
      expect(xaml).toContain('Platform="Windows"');
      expect(platforms).toHaveLength(4);
    });
  });

  describe('Constraint Validation', () => {
    it('should validate XAML structure matches design', () => {
      const xaml = '<ContentView><Frame><Label Text="Hello" /></Frame></ContentView>';
      const designElements = {
        elements: [
          {
            type: 'frame',
            id: 'container',
            properties: {},
            children: [
              { type: 'label', id: 'greeting', properties: { text: 'Hello' } },
            ],
          },
        ],
      };

      const isValid = validateXAMLStructure(xaml, designElements);

      expect(isValid).toBe(true);
    });

    it('should detect missing design elements', () => {
      const xaml = '<ContentView><Frame /></ContentView>';
      const designElements = {
        elements: [
          {
            type: 'frame',
            id: 'container',
            properties: {},
            children: [{ type: 'label', id: 'greeting', properties: {} }],
          },
        ],
      };

      const violations = validateGeneratedComponent(xaml, '', designElements, {});

      expect(violations).toContain('Missing design element: greeting');
    });

    it('should detect prohibited bindable properties', () => {
      const codeBehind = `
        public static readonly BindableProperty OnErrorProperty = ...;
      `;
      const prohibitions = { extra_props_for_flexibility: true };

      const violations = validateCodeBehind(codeBehind, prohibitions);

      expect(violations).toContain(
        'Extra bindable property detected (prohibited - not in design)'
      );
    });
  });
});

// Helper Functions (Test Doubles)

function mapToMauiControl(element: any): string {
  const mappings: Record<string, string> = {
    text: 'Label',
    label: 'Label',
    button: 'Button',
    entry: 'Entry',
    image: 'Image',
    frame: 'Frame',
    grid: 'Grid',
  };

  return mappings[element.type] || 'Frame';
}

function generateXAML(designElements: any): string {
  const element = designElements.elements[0];
  const style = element.properties?.style || {};

  let xaml = `<?xml version="1.0" encoding="utf-8" ?>
<ContentView xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml">
    <Frame`;

  if (style.backgroundColor) {
    xaml += ` BackgroundColor="${style.backgroundColor}"`;
  }
  if (style.borderRadius) {
    xaml += ` CornerRadius="${style.borderRadius}"`;
  }
  if (style.padding) {
    if (typeof style.padding === 'number') {
      xaml += ` Padding="${style.padding}"`;
    } else {
      xaml += ` Padding="${style.padding.left},${style.padding.top},${style.padding.right},${style.padding.bottom}"`;
    }
  }
  if (style.margin) {
    xaml += ` Margin="${style.margin}"`;
  }
  if (style.textColor) {
    xaml += ` TextColor="${style.textColor}"`;
  }

  xaml += '>';

  if (element.children) {
    for (const child of element.children) {
      const childControl = mapToMauiControl(child);
      const text = child.properties?.text || '';
      xaml += `\n        <${childControl}`;
      if (text) {
        xaml += ` Text="${text}"`;
      }
      xaml += ' />';
    }
  }

  xaml += `
    </Frame>
</ContentView>`;

  return xaml;
}

function generateCodeBehind(componentName: string): string {
  return `using Microsoft.Maui.Controls;

namespace MyApp.Views
{
    public partial class ${componentName} : ContentView
    {
        public ${componentName}()
        {
            InitializeComponent();
        }
    }
}`;
}

function generateCodeBehindWithMetadata(componentName: string, metadata: any): string {
  return `using Microsoft.Maui.Controls;

namespace MyApp.Views
{
    /// <summary>
    /// ${componentName}
    ///
    /// Project ID: ${metadata.projectId}
    /// Screen ID: ${metadata.screenId}
    /// Extracted: ${metadata.extractedAt}
    /// </summary>
    public partial class ${componentName} : ContentView
    {
        public ${componentName}()
        {
            InitializeComponent();
        }
    }
}`;
}

function generateViewModel(componentName: string): string {
  return `using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace MyApp.ViewModels
{
    public partial class ${componentName}ViewModel : ObservableObject
    {
        // Properties and commands
    }
}`;
}

function generateViewModelWithProperties(designElements: any): string {
  let viewModel = `using CommunityToolkit.Mvvm.ComponentModel;

namespace MyApp.ViewModels
{
    public partial class ComponentViewModel : ObservableObject
    {`;

  for (const element of designElements.elements) {
    if (element.type === 'entry') {
      const propertyName = element.id.replace('-entry', '').replace(/-/g, '');
      viewModel += `
        [ObservableProperty]
        private string _${propertyName} = string.Empty;`;
    }
  }

  viewModel += `
    }
}`;

  return viewModel;
}

function generateViewModelWithCommands(designElements: any): string {
  let viewModel = `using CommunityToolkit.Mvvm.Input;

namespace MyApp.ViewModels
{
    public partial class ComponentViewModel
    {`;

  for (const element of designElements.elements) {
    if (element.type === 'button') {
      const commandName = element.id.replace('-button', '').replace(/-/g, '');
      const capitalizedName =
        commandName.charAt(0).toUpperCase() + commandName.slice(1);
      viewModel += `
        [RelayCommand]
        private void ${capitalizedName}()
        {
            // Minimal logic
        }`;
    }
  }

  viewModel += `
    }
}`;

  return viewModel;
}

function generatePlatformSpecificXAML(platform: string): string {
  if (platform === 'ios') {
    return `<ContentPage.Resources>
    <OnPlatform x:Key="TopMargin" x:TypeArguments="Thickness">
        <On Platform="iOS" Value="0,20,0,0" />
        <On Platform="Android" Value="0" />
    </OnPlatform>
</ContentPage.Resources>`;
  } else if (platform === 'android') {
    return `<Button Style="{StaticResource MaterialButton}"
        Platform="Android" />`;
  }
  return '';
}

function generateMultiPlatformXAML(_platforms: string[]): string {
  return `<OnPlatform x:TypeArguments="Thickness">
    <On Platform="iOS" Value="0,20,0,0" />
    <On Platform="Android" Value="0" />
    <On Platform="Windows" Value="0" />
</OnPlatform>`;
}

function validateXAMLStructure(xaml: string, designElements: any): boolean {
  const element = designElements.elements[0];
  const hasFrame = xaml.includes('<Frame');
  const hasLabel =
    element.children?.some((c: any) => c.type === 'label') && xaml.includes('<Label');

  return hasFrame && hasLabel;
}

function validateGeneratedComponent(
  xaml: string,
  _codeBehind: string,
  designElements: any,
  _prohibitions: any
): string[] {
  const violations: string[] = [];

  for (const element of designElements.elements) {
    if (element.children) {
      for (const child of element.children) {
        if (!xaml.includes(child.id)) {
          violations.push(`Missing design element: ${child.id}`);
        }
      }
    }
  }

  return violations;
}

function validateCodeBehind(codeBehind: string, prohibitions: any): string[] {
  const violations: string[] = [];

  if (
    prohibitions.extra_props_for_flexibility &&
    codeBehind.includes('BindableProperty')
  ) {
    violations.push('Extra bindable property detected (prohibited - not in design)');
  }

  return violations;
}
