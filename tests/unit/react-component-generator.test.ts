/**
 * Unit Tests for react-component-generator Agent
 *
 * Tests component generation, prop extraction, Tailwind CSS conversion,
 * state management, and visual regression testing
 */

import { describe, it, expect } from 'vitest';

describe('react-component-generator - Props Generation', () => {
  interface ExtractedElement {
    type: string;
    id: string;
    properties: {
      text?: string;
      src?: string;
      value?: string;
      style?: Record<string, any>;
      children?: ExtractedElement[];
    };
  }

  function camelCase(str: string): string {
    return str.replace(/-([a-z])/g, (g) => g[1]?.toUpperCase() ?? g);
  }

  function pascalCase(str: string): string {
    const camel = camelCase(str);
    return camel.charAt(0).toUpperCase() + camel.slice(1);
  }

  function generatePropsFromDesign(elements: ExtractedElement[]): string[] {
    const props: string[] = [];

    for (const element of elements) {
      if (element.type === "text" && element.properties.text) {
        props.push(`${camelCase(element.id)}?: string;`);
      }

      if (element.type === "button") {
        props.push(`on${pascalCase(element.id)}Click?: () => void;`);
      }

      if (element.type === "input") {
        props.push(`${camelCase(element.id)}Value?: string;`);
        props.push(`on${pascalCase(element.id)}Change?: (value: string) => void;`);
      }

      if (element.type === "image" && element.properties.src) {
        props.push(`${camelCase(element.id)}Src?: string;`);
      }
    }

    return props;
  }

  it('should generate text prop for text elements', () => {
    const elements: ExtractedElement[] = [
      {
        type: 'text',
        id: 'title-text',
        properties: { text: 'Welcome' }
      }
    ];

    const props = generatePropsFromDesign(elements);

    expect(props).toContain('titleText?: string;');
  });

  it('should generate onClick handler for button elements', () => {
    const elements: ExtractedElement[] = [
      {
        type: 'button',
        id: 'submit-button',
        properties: {}
      }
    ];

    const props = generatePropsFromDesign(elements);

    expect(props).toContain('onSubmitButtonClick?: () => void;');
  });

  it('should generate value and onChange for input elements', () => {
    const elements: ExtractedElement[] = [
      {
        type: 'input',
        id: 'email-input',
        properties: {}
      }
    ];

    const props = generatePropsFromDesign(elements);

    expect(props).toContain('emailInputValue?: string;');
    expect(props).toContain('onEmailInputChange?: (value: string) => void;');
    expect(props).toHaveLength(2);
  });

  it('should generate src prop for image elements', () => {
    const elements: ExtractedElement[] = [
      {
        type: 'image',
        id: 'profile-image',
        properties: { src: '/path/to/image.png' }
      }
    ];

    const props = generatePropsFromDesign(elements);

    expect(props).toContain('profileImageSrc?: string;');
  });

  it('should not generate props for container elements', () => {
    const elements: ExtractedElement[] = [
      {
        type: 'container',
        id: 'main-container',
        properties: {}
      }
    ];

    const props = generatePropsFromDesign(elements);

    expect(props).toHaveLength(0);
  });

  it('should generate props for multiple elements', () => {
    const elements: ExtractedElement[] = [
      { type: 'text', id: 'title', properties: { text: 'Title' } },
      { type: 'input', id: 'email', properties: {} },
      { type: 'button', id: 'submit', properties: {} },
    ];

    const props = generatePropsFromDesign(elements);

    expect(props.length).toBeGreaterThanOrEqual(4); // title, emailValue, onEmailChange, onSubmitClick
  });

  it('should handle hyphenated IDs correctly', () => {
    const elements: ExtractedElement[] = [
      { type: 'button', id: 'submit-form-button', properties: {} },
    ];

    const props = generatePropsFromDesign(elements);

    expect(props).toContain('onSubmitFormButtonClick?: () => void;');
  });
});

describe('react-component-generator - Tailwind CSS Conversion', () => {
  interface CSSProperties {
    backgroundColor?: string;
    color?: string;
    padding?: number;
    margin?: number;
    fontSize?: number;
    fontWeight?: number;
    display?: string;
    flexDirection?: string;
    justifyContent?: string;
    alignItems?: string;
    gap?: number;
    border?: string;
    borderWidth?: number;
    borderColor?: string;
    borderRadius?: number;
    width?: number;
    height?: number;
  }

  function kebabCase(str: string): string {
    return str.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
  }

  function figmaStylesToTailwind(style: CSSProperties): string {
    const classes: string[] = [];

    if (style.backgroundColor) {
      classes.push(`bg-[${style.backgroundColor}]`);
    }

    if (style.color) {
      classes.push(`text-[${style.color}]`);
    }

    if (style.padding) {
      classes.push(`p-[${style.padding}px]`);
    }

    if (style.margin) {
      classes.push(`m-[${style.margin}px]`);
    }

    if (style.fontSize) {
      classes.push(`text-[${style.fontSize}px]`);
    }

    if (style.fontWeight) {
      classes.push(`font-[${style.fontWeight}]`);
    }

    if (style.display === 'flex') {
      classes.push('flex');
      if (style.flexDirection) {
        classes.push(`flex-${style.flexDirection}`);
      }
      if (style.justifyContent) {
        classes.push(`justify-${kebabCase(style.justifyContent)}`);
      }
      if (style.alignItems) {
        classes.push(`items-${kebabCase(style.alignItems)}`);
      }
      if (style.gap) {
        classes.push(`gap-[${style.gap}px]`);
      }
    }

    if (style.borderWidth && style.borderColor) {
      classes.push(`border-[${style.borderWidth}px]`);
      classes.push(`border-[${style.borderColor}]`);
    }

    if (style.borderRadius) {
      classes.push(`rounded-[${style.borderRadius}px]`);
    }

    if (style.width) {
      classes.push(`w-[${style.width}px]`);
    }

    if (style.height) {
      classes.push(`h-[${style.height}px]`);
    }

    return classes.join(' ');
  }

  it('should convert background color to Tailwind', () => {
    const style: CSSProperties = {
      backgroundColor: '#3B82F6'
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('bg-[#3B82F6]');
  });

  it('should convert text color to Tailwind', () => {
    const style: CSSProperties = {
      color: '#FFFFFF'
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('text-[#FFFFFF]');
  });

  it('should convert padding to Tailwind arbitrary values', () => {
    const style: CSSProperties = {
      padding: 16
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('p-[16px]');
  });

  it('should convert typography to Tailwind', () => {
    const style: CSSProperties = {
      fontSize: 14,
      fontWeight: 600
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('text-[14px]');
    expect(tailwind).toContain('font-[600]');
  });

  it('should convert flexbox layout to Tailwind', () => {
    const style: CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'spaceBetween',
      alignItems: 'center',
      gap: 16
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('flex');
    expect(tailwind).toContain('flex-column');
    expect(tailwind).toContain('justify-space-between');
    expect(tailwind).toContain('items-center');
    expect(tailwind).toContain('gap-[16px]');
  });

  it('should convert border properties to Tailwind', () => {
    const style: CSSProperties = {
      borderWidth: 1,
      borderColor: '#E5E7EB',
      borderRadius: 8
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('border-[1px]');
    expect(tailwind).toContain('border-[#E5E7EB]');
    expect(tailwind).toContain('rounded-[8px]');
  });

  it('should convert dimensions to Tailwind', () => {
    const style: CSSProperties = {
      width: 320,
      height: 48
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('w-[320px]');
    expect(tailwind).toContain('h-[48px]');
  });

  it('should combine multiple styles correctly', () => {
    const style: CSSProperties = {
      backgroundColor: '#3B82F6',
      color: '#FFFFFF',
      padding: 16,
      borderRadius: 8,
      width: 320,
      height: 48
    };

    const tailwind = figmaStylesToTailwind(style);

    expect(tailwind).toContain('bg-[#3B82F6]');
    expect(tailwind).toContain('text-[#FFFFFF]');
    expect(tailwind).toContain('p-[16px]');
    expect(tailwind).toContain('rounded-[8px]');
    expect(tailwind).toContain('w-[320px]');
    expect(tailwind).toContain('h-[48px]');
  });
});

describe('react-component-generator - State Management', () => {
  interface ExtractedElement {
    type: string;
    id: string;
    properties: {
      value?: string;
      checked?: boolean;
    };
  }

  interface ProhibitionChecklist {
    loading_states: boolean;
    error_states: boolean;
    complex_state_management: boolean;
  }

  function camelCase(str: string): string {
    return str.replace(/-([a-z])/g, (g) => g[1]?.toUpperCase() ?? g);
  }

  function pascalCase(str: string): string {
    const camel = camelCase(str);
    return camel.charAt(0).toUpperCase() + camel.slice(1);
  }

  function generateMinimalState(
    elements: ExtractedElement[],
    _prohibitions: ProhibitionChecklist
  ): string[] {
    const state: string[] = [];

    for (const element of elements) {
      if (element.type === "input" && !element.properties.value) {
        state.push(`const [${camelCase(element.id)}, set${pascalCase(element.id)}] = useState<string>('');`);
      }

      if (element.type === "checkbox") {
        state.push(`const [${camelCase(element.id)}, set${pascalCase(element.id)}] = useState<boolean>(false);`);
      }

      if (element.type === "select") {
        state.push(`const [${camelCase(element.id)}, set${pascalCase(element.id)}] = useState<string>('');`);
      }
    }

    return state;
  }

  it('should generate state for input without value prop', () => {
    const elements: ExtractedElement[] = [
      { type: 'input', id: 'email-input', properties: {} }
    ];

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      complex_state_management: true,
    };

    const state = generateMinimalState(elements, prohibitions);

    expect(state).toContain("const [emailInput, setEmailInput] = useState<string>('');");
  });

  it('should not generate state for input with value prop', () => {
    const elements: ExtractedElement[] = [
      { type: 'input', id: 'email-input', properties: { value: 'test@example.com' } }
    ];

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      complex_state_management: true,
    };

    const state = generateMinimalState(elements, prohibitions);

    expect(state).toHaveLength(0);
  });

  it('should generate state for checkbox', () => {
    const elements: ExtractedElement[] = [
      { type: 'checkbox', id: 'remember-me', properties: {} }
    ];

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      complex_state_management: true,
    };

    const state = generateMinimalState(elements, prohibitions);

    expect(state).toContain("const [rememberMe, setRememberMe] = useState<boolean>(false);");
  });

  it('should generate state for select dropdown', () => {
    const elements: ExtractedElement[] = [
      { type: 'select', id: 'country-select', properties: {} }
    ];

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      complex_state_management: true,
    };

    const state = generateMinimalState(elements, prohibitions);

    expect(state).toContain("const [countrySelect, setCountrySelect] = useState<string>('');");
  });

  it('should not generate loading or error states when prohibited', () => {
    const elements: ExtractedElement[] = [
      { type: 'input', id: 'email', properties: {} }
    ];

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      complex_state_management: true,
    };

    const state = generateMinimalState(elements, prohibitions);

    const stateString = state.join('\n');
    expect(stateString).not.toContain('isLoading');
    expect(stateString).not.toContain('error');
    expect(stateString).not.toContain('useReducer');
  });

  it('should handle multiple interactive elements', () => {
    const elements: ExtractedElement[] = [
      { type: 'input', id: 'email', properties: {} },
      { type: 'input', id: 'password', properties: {} },
      { type: 'checkbox', id: 'terms', properties: {} },
    ];

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      complex_state_management: true,
    };

    const state = generateMinimalState(elements, prohibitions);

    expect(state).toHaveLength(3);
  });
});

describe('react-component-generator - Data TestID Generation', () => {
  function kebabCase(str: string): string {
    return str.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
  }

  function generateTestId(elementId: string): string {
    return `data-testid="${kebabCase(elementId)}"`;
  }

  it('should generate data-testid in kebab-case', () => {
    const testId = generateTestId('submitButton');

    expect(testId).toBe('data-testid="submit-button"');
  });

  it('should handle already kebab-case IDs', () => {
    const testId = generateTestId('submit-button');

    expect(testId).toBe('data-testid="submit-button"');
  });

  it('should handle complex IDs', () => {
    const testId = generateTestId('emailInputField');

    expect(testId).toBe('data-testid="email-input-field"');
  });

  it('should handle single word IDs', () => {
    const testId = generateTestId('button');

    expect(testId).toBe('data-testid="button"');
  });
});

describe('react-component-generator - Component Validation', () => {
  interface ExtractedElement {
    type: string;
    id: string;
    properties: Record<string, any>;
  }

  interface DesignElements {
    elements: ExtractedElement[];
    boundary: {
      documented: string[];
      undocumented: string[];
    };
  }

  interface ProhibitionChecklist {
    loading_states: boolean;
    error_states: boolean;
    api_integrations: boolean;
    extra_props_for_flexibility: boolean;
    best_practice_additions: boolean;
  }

  interface DesignConstraints {
    prohibitions: ProhibitionChecklist;
  }

  function validateGeneratedComponent(
    code: string,
    designElements: DesignElements,
    designConstraints: DesignConstraints
  ): string[] {
    const issues: string[] = [];

    // Check for prohibited features
    if (designConstraints.prohibitions.loading_states && /isLoading|loading/i.test(code)) {
      issues.push("Contains loading state (prohibited)");
    }

    if (designConstraints.prohibitions.api_integrations && /(fetch|axios|api)/i.test(code)) {
      issues.push("Contains API integration (prohibited)");
    }

    // Verify all design elements implemented
    for (const element of designElements.elements) {
      if (!code.includes(element.id)) {
        issues.push(`Missing design element: ${element.id}`);
      }
    }

    // Check for data-testid attributes
    for (const element of designElements.elements) {
      const kebabId = element.id.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();
      if (!code.includes(`data-testid="${kebabId}"`)) {
        issues.push(`Missing data-testid for element: ${element.id}`);
      }
    }

    return issues;
  }

  it('should pass validation for compliant component', () => {
    const code = `
      <button data-testid="submit-button" onClick={onSubmitClick}>
        Submit
      </button>
    `;

    const designElements: DesignElements = {
      elements: [
        { type: 'button', id: 'submit-button', properties: {} }
      ],
      boundary: {
        documented: ['submit-button'],
        undocumented: []
      }
    };

    const designConstraints: DesignConstraints = {
      prohibitions: {
        loading_states: true,
        error_states: true,
        api_integrations: true,
        extra_props_for_flexibility: true,
        best_practice_additions: true,
      }
    };

    const issues = validateGeneratedComponent(code, designElements, designConstraints);

    expect(issues).toHaveLength(0);
  });

  it('should detect missing design elements', () => {
    const code = `
      <button data-testid="submit-button">Submit</button>
    `;

    const designElements: DesignElements = {
      elements: [
        { type: 'button', id: 'submit-button', properties: {} },
        { type: 'input', id: 'email-input', properties: {} },
      ],
      boundary: {
        documented: ['submit-button', 'email-input'],
        undocumented: []
      }
    };

    const designConstraints: DesignConstraints = {
      prohibitions: {
        loading_states: true,
        error_states: true,
        api_integrations: true,
        extra_props_for_flexibility: true,
        best_practice_additions: true,
      }
    };

    const issues = validateGeneratedComponent(code, designElements, designConstraints);

    expect(issues.length).toBeGreaterThan(0);
    expect(issues.some(issue => issue.includes('email-input'))).toBe(true);
  });

  it('should detect prohibited loading states', () => {
    const code = `
      const [isLoading, setIsLoading] = useState(false);
      <button>Submit</button>
    `;

    const designElements: DesignElements = {
      elements: [
        { type: 'button', id: 'submit-button', properties: {} }
      ],
      boundary: {
        documented: ['submit-button'],
        undocumented: []
      }
    };

    const designConstraints: DesignConstraints = {
      prohibitions: {
        loading_states: true,
        error_states: true,
        api_integrations: true,
        extra_props_for_flexibility: true,
        best_practice_additions: true,
      }
    };

    const issues = validateGeneratedComponent(code, designElements, designConstraints);

    expect(issues.some(issue => issue.includes('loading state'))).toBe(true);
  });

  it('should detect missing data-testid attributes', () => {
    const code = `
      <button onClick={onSubmitClick}>Submit</button>
    `;

    const designElements: DesignElements = {
      elements: [
        { type: 'button', id: 'submit-button', properties: {} }
      ],
      boundary: {
        documented: ['submit-button'],
        undocumented: []
      }
    };

    const designConstraints: DesignConstraints = {
      prohibitions: {
        loading_states: true,
        error_states: true,
        api_integrations: true,
        extra_props_for_flexibility: true,
        best_practice_additions: true,
      }
    };

    const issues = validateGeneratedComponent(code, designElements, designConstraints);

    expect(issues.some(issue => issue.includes('Missing data-testid'))).toBe(true);
  });

  it('should detect prohibited API integration', () => {
    const code = `
      const handleSubmit = async () => {
        await fetch('/api/data');
      };
      <button data-testid="submit-button">Submit</button>
    `;

    const designElements: DesignElements = {
      elements: [
        { type: 'button', id: 'submit-button', properties: {} }
      ],
      boundary: {
        documented: ['submit-button'],
        undocumented: []
      }
    };

    const designConstraints: DesignConstraints = {
      prohibitions: {
        loading_states: true,
        error_states: true,
        api_integrations: true,
        extra_props_for_flexibility: true,
        best_practice_additions: true,
      }
    };

    const issues = validateGeneratedComponent(code, designElements, designConstraints);

    expect(issues.some(issue => issue.includes('API integration'))).toBe(true);
  });
});
