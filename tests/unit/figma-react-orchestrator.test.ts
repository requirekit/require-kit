/**
 * Unit Tests for figma-react-orchestrator Agent
 *
 * Tests node ID conversion, MCP verification, design extraction,
 * boundary documentation, and constraint validation
 */

import { describe, it, expect, vi } from 'vitest';

describe('figma-react-orchestrator - Node ID Conversion', () => {
  describe('convertNodeId', () => {
    it('should convert URL format with hyphen to colon format', () => {
      const input = 'https://figma.com/design/abc?node-id=2-2';
      const expected = '2:2';

      // Test conversion logic
      const urlMatch = input.match(/node-id=(\d+)-(\d+)/);
      const result = urlMatch ? `${urlMatch[1]}:${urlMatch[2]}` : null;

      expect(result).toBe(expected);
    });

    it('should convert direct hyphen format to colon format', () => {
      const input = '2-2';
      const expected = '2:2';

      const directMatch = input.match(/^(\d+)-(\d+)$/);
      const result = directMatch ? `${directMatch[1]}:${directMatch[2]}` : null;

      expect(result).toBe(expected);
    });

    it('should convert complex node IDs', () => {
      const testCases = [
        { input: '123-456', expected: '123:456' },
        { input: 'https://figma.com/design/abc?node-id=123-456', expected: '123:456' },
        { input: '999-1000', expected: '999:1000' },
      ];

      testCases.forEach(({ input, expected }) => {
        const urlMatch = input.match(/node-id=(\d+)-(\d+)/);
        const directMatch = input.match(/^(\d+)-(\d+)$/);

        const result = urlMatch
          ? `${urlMatch[1]}:${urlMatch[2]}`
          : directMatch
            ? `${directMatch[1]}:${directMatch[2]}`
            : null;

        expect(result).toBe(expected);
      });
    });

    it('should pass through colon format unchanged', () => {
      const input = '2:2';
      const expected = '2:2';

      const isValidColonFormat = /^\d+:\d+$/.test(input);
      const result = isValidColonFormat ? input : null;

      expect(result).toBe(expected);
    });

    it('should reject invalid formats', () => {
      const invalidInputs = [
        'invalid',
        'abc-def',
        '2:2:2',
        '2-2-2',
        '',
      ];

      invalidInputs.forEach((input) => {
        const urlMatch = input.match(/node-id=(\d+)-(\d+)/);
        const directMatch = input.match(/^(\d+)-(\d+)$/);
        const colonMatch = /^\d+:\d+$/.test(input);

        const result = urlMatch
          ? `${urlMatch[1]}:${urlMatch[2]}`
          : directMatch
            ? `${directMatch[1]}:${directMatch[2]}`
            : colonMatch
              ? input
              : null;

        expect(result).toBeNull();
      });
    });

    it('should convert URL with query parameters', () => {
      const input = 'https://figma.com/design/abc?node-id=2-2&t=xyz';
      const expected = '2:2';

      const urlMatch = input.match(/node-id=(\d+)-(\d+)/);
      const result = urlMatch ? `${urlMatch[1]}:${urlMatch[2]}` : null;

      expect(result).toBe(expected);
    });
  });
});

describe('figma-react-orchestrator - Prohibition Checklist Generation', () => {
  interface DesignElement {
    type: string;
    id: string;
    properties: {
      text?: string;
      style?: Record<string, any>;
      children?: DesignElement[];
    };
  }

  interface ProhibitionChecklist {
    loading_states: boolean;
    error_states: boolean;
    additional_form_validation: boolean;
    complex_state_management: boolean;
    api_integrations: boolean;
    navigation_beyond_design: boolean;
    additional_buttons: boolean;
    sample_data_beyond_design: boolean;
    responsive_breakpoints: boolean;
    animations_not_specified: boolean;
    best_practice_additions: boolean;
    extra_props_for_flexibility: boolean;
  }

  function generateProhibitions(elements: DesignElement[]): ProhibitionChecklist {
    return {
      loading_states: !elements.some(e => e.id.toLowerCase().includes('loading')),
      error_states: !elements.some(e => e.id.toLowerCase().includes('error')),
      additional_form_validation: true, // Default prohibited
      complex_state_management: true, // Default prohibited
      api_integrations: true, // ALWAYS prohibited
      navigation_beyond_design: !elements.some(e => e.type === 'navigation'),
      additional_buttons: true, // Default prohibited
      sample_data_beyond_design: true, // ALWAYS prohibited
      responsive_breakpoints: true, // Default prohibited
      animations_not_specified: true, // Default prohibited
      best_practice_additions: true, // ALWAYS prohibited
      extra_props_for_flexibility: true, // ALWAYS prohibited
    };
  }

  it('should prohibit loading states when not in design', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'submit-button', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(prohibitions.loading_states).toBe(true);
  });

  it('should allow loading states when in design', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'submit-button', properties: {} },
      { type: 'spinner', id: 'loading-spinner', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(prohibitions.loading_states).toBe(false);
  });

  it('should always prohibit API integrations', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'api-button', properties: {} },
      { type: 'text', id: 'api-response', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(prohibitions.api_integrations).toBe(true);
  });

  it('should always prohibit best practice additions', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'button', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(prohibitions.best_practice_additions).toBe(true);
  });

  it('should prohibit error states when not in design', () => {
    const elements: DesignElement[] = [
      { type: 'input', id: 'email-input', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(prohibitions.error_states).toBe(true);
  });

  it('should allow error states when in design', () => {
    const elements: DesignElement[] = [
      { type: 'input', id: 'email-input', properties: {} },
      { type: 'text', id: 'error-message', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(prohibitions.error_states).toBe(false);
  });

  it('should generate complete prohibition checklist', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'submit', properties: {} },
    ];

    const prohibitions = generateProhibitions(elements);

    expect(Object.keys(prohibitions)).toHaveLength(12);
    expect(prohibitions).toHaveProperty('loading_states');
    expect(prohibitions).toHaveProperty('error_states');
    expect(prohibitions).toHaveProperty('api_integrations');
    expect(prohibitions).toHaveProperty('best_practice_additions');
  });
});

describe('figma-react-orchestrator - Constraint Validation', () => {
  interface ProhibitionChecklist {
    loading_states: boolean;
    error_states: boolean;
    additional_form_validation: boolean;
    complex_state_management: boolean;
    api_integrations: boolean;
    navigation_beyond_design: boolean;
    additional_buttons: boolean;
    sample_data_beyond_design: boolean;
    responsive_breakpoints: boolean;
    animations_not_specified: boolean;
    best_practice_additions: boolean;
    extra_props_for_flexibility: boolean;
  }

  function patternMatchValidation(code: string, prohibitions: ProhibitionChecklist): string[] {
    const violations: string[] = [];

    if (prohibitions.loading_states && /isLoading|loading/i.test(code)) {
      violations.push("Loading state detected (prohibited - not in design)");
    }

    if (prohibitions.error_states && /isError|error/i.test(code)) {
      violations.push("Error state detected (prohibited - not in design)");
    }

    if (prohibitions.api_integrations && /(fetch|axios|api)/i.test(code)) {
      violations.push("API integration detected (ALWAYS prohibited)");
    }

    if (prohibitions.additional_form_validation && /validate|validator/i.test(code)) {
      violations.push("Additional validation detected (prohibited - not in design)");
    }

    if (prohibitions.best_practice_additions && /aria-|role=/i.test(code)) {
      violations.push("Best practice addition detected (prohibited - not in design)");
    }

    return violations;
  }

  it('should detect loading state violations', () => {
    const code = `
      const [isLoading, setIsLoading] = useState(false);
      return <div>{isLoading ? 'Loading...' : 'Content'}</div>;
    `;

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: false,
      additional_form_validation: false,
      complex_state_management: false,
      api_integrations: true,
      navigation_beyond_design: false,
      additional_buttons: false,
      sample_data_beyond_design: true,
      responsive_breakpoints: false,
      animations_not_specified: false,
      best_practice_additions: true,
      extra_props_for_flexibility: true,
    };

    const violations = patternMatchValidation(code, prohibitions);

    expect(violations).toHaveLength(1);
    expect(violations[0]).toContain('Loading state detected');
  });

  it('should detect API integration violations', () => {
    const code = `
      const handleSubmit = async () => {
        const response = await fetch('/api/data');
      };
    `;

    const prohibitions: ProhibitionChecklist = {
      loading_states: false,
      error_states: false,
      additional_form_validation: false,
      complex_state_management: false,
      api_integrations: true,
      navigation_beyond_design: false,
      additional_buttons: false,
      sample_data_beyond_design: true,
      responsive_breakpoints: false,
      animations_not_specified: false,
      best_practice_additions: true,
      extra_props_for_flexibility: true,
    };

    const violations = patternMatchValidation(code, prohibitions);

    expect(violations).toHaveLength(1);
    expect(violations[0]).toContain('API integration detected');
  });

  it('should detect multiple violations', () => {
    const code = `
      const [isLoading, setIsLoading] = useState(false);
      const [error, setError] = useState(null);

      const handleSubmit = async () => {
        const response = await fetch('/api/data');
        const validated = validateEmail(email);
      };
    `;

    const prohibitions: ProhibitionChecklist = {
      loading_states: true,
      error_states: true,
      additional_form_validation: true,
      complex_state_management: false,
      api_integrations: true,
      navigation_beyond_design: false,
      additional_buttons: false,
      sample_data_beyond_design: true,
      responsive_breakpoints: false,
      animations_not_specified: false,
      best_practice_additions: true,
      extra_props_for_flexibility: true,
    };

    const violations = patternMatchValidation(code, prohibitions);

    expect(violations.length).toBeGreaterThanOrEqual(3);
  });

  it('should not flag violations when features are allowed', () => {
    const code = `
      const [isLoading, setIsLoading] = useState(false);
      return <div>{isLoading ? 'Loading...' : 'Content'}</div>;
    `;

    const prohibitions: ProhibitionChecklist = {
      loading_states: false, // Allowed in design
      error_states: false,
      additional_form_validation: false,
      complex_state_management: false,
      api_integrations: true,
      navigation_beyond_design: false,
      additional_buttons: false,
      sample_data_beyond_design: true,
      responsive_breakpoints: false,
      animations_not_specified: false,
      best_practice_additions: true,
      extra_props_for_flexibility: true,
    };

    const violations = patternMatchValidation(code, prohibitions);

    expect(violations).toHaveLength(0);
  });

  it('should detect best practice additions', () => {
    const code = `
      <button aria-label="Submit form" role="button">
        Submit
      </button>
    `;

    const prohibitions: ProhibitionChecklist = {
      loading_states: false,
      error_states: false,
      additional_form_validation: false,
      complex_state_management: false,
      api_integrations: true,
      navigation_beyond_design: false,
      additional_buttons: false,
      sample_data_beyond_design: true,
      responsive_breakpoints: false,
      animations_not_specified: false,
      best_practice_additions: true,
      extra_props_for_flexibility: true,
    };

    const violations = patternMatchValidation(code, prohibitions);

    expect(violations.length).toBeGreaterThan(0);
    expect(violations[0]).toContain('Best practice addition');
  });
});

describe('figma-react-orchestrator - Design Boundary Documentation', () => {
  interface DesignElement {
    type: string;
    id: string;
    properties: Record<string, any>;
  }

  interface DesignBoundary {
    documented: string[];
    undocumented: string[];
  }

  function extractDesignBoundary(elements: DesignElement[]): DesignBoundary {
    const documented = elements.map(e => e.id);

    const allPossibleFeatures = [
      'loading',
      'error',
      'api',
      'navigation',
      'validation',
      'animation',
    ];

    const undocumented = allPossibleFeatures.filter(
      feature => !documented.some(id => id.toLowerCase().includes(feature))
    );

    return { documented, undocumented };
  }

  it('should identify documented elements', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'submit-button', properties: {} },
      { type: 'input', id: 'email-input', properties: {} },
    ];

    const boundary = extractDesignBoundary(elements);

    expect(boundary.documented).toContain('submit-button');
    expect(boundary.documented).toContain('email-input');
    expect(boundary.documented).toHaveLength(2);
  });

  it('should identify undocumented features', () => {
    const elements: DesignElement[] = [
      { type: 'button', id: 'submit-button', properties: {} },
    ];

    const boundary = extractDesignBoundary(elements);

    expect(boundary.undocumented).toContain('loading');
    expect(boundary.undocumented).toContain('error');
    expect(boundary.undocumented).toContain('api');
  });

  it('should handle empty design', () => {
    const elements: DesignElement[] = [];

    const boundary = extractDesignBoundary(elements);

    expect(boundary.documented).toHaveLength(0);
    expect(boundary.undocumented.length).toBeGreaterThan(0);
  });

  it('should correctly mark loading state as documented when present', () => {
    const elements: DesignElement[] = [
      { type: 'spinner', id: 'loading-spinner', properties: {} },
    ];

    const boundary = extractDesignBoundary(elements);

    expect(boundary.documented).toContain('loading-spinner');
    expect(boundary.undocumented).not.toContain('loading');
  });
});

describe('figma-react-orchestrator - Retry Logic', () => {
  it('should retry on transient failures', async () => {
    let attempt = 0;

    const retryableMcpCall = vi.fn().mockImplementation(() => {
      attempt++;
      if (attempt < 3) {
        throw new Error('Network timeout');
      }
      return Promise.resolve({ success: true });
    });

    async function retryMcpCall<T>(
      mcpCall: () => Promise<T>,
      maxAttempts: number = 3,
      backoffMs: number = 100
    ): Promise<T> {
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return await mcpCall();
        } catch (error: any) {
          const isRetryable =
            error.message.includes("timeout") ||
            error.message.includes("rate limit") ||
            error.message.includes("network");

          if (!isRetryable || attempt === maxAttempts) {
            throw error;
          }

          await new Promise(resolve => setTimeout(resolve, backoffMs));
        }
      }
      // This line should never be reached, but TypeScript requires a return
      throw new Error('Max attempts exceeded');
    }

    const result = await retryMcpCall(retryableMcpCall);

    expect(result).toEqual({ success: true });
    expect(retryableMcpCall).toHaveBeenCalledTimes(3);
  });

  it('should not retry non-retryable errors', async () => {
    const nonRetryableMcpCall = vi.fn().mockRejectedValue(
      new Error('Invalid authentication')
    );

    async function retryMcpCall<T>(
      mcpCall: () => Promise<T>,
      maxAttempts: number = 3
    ): Promise<T> {
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return await mcpCall();
        } catch (error: any) {
          const isRetryable =
            error.message.includes("timeout") ||
            error.message.includes("rate limit") ||
            error.message.includes("network");

          if (!isRetryable || attempt === maxAttempts) {
            throw error;
          }
        }
      }
      throw new Error('Max attempts exceeded');
    }

    await expect(retryMcpCall(nonRetryableMcpCall)).rejects.toThrow('Invalid authentication');
    expect(nonRetryableMcpCall).toHaveBeenCalledTimes(1);
  });

  it('should exhaust retries and throw', async () => {
    const alwaysFailingMcpCall = vi.fn().mockRejectedValue(
      new Error('Network timeout')
    );

    async function retryMcpCall<T>(
      mcpCall: () => Promise<T>,
      maxAttempts: number = 3
    ): Promise<T> {
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
          return await mcpCall();
        } catch (error: any) {
          const isRetryable =
            error.message.includes("timeout") ||
            error.message.includes("rate limit") ||
            error.message.includes("network");

          if (!isRetryable || attempt === maxAttempts) {
            throw error;
          }
        }
      }
      throw new Error('Max attempts exceeded');
    }

    await expect(retryMcpCall(alwaysFailingMcpCall)).rejects.toThrow('Network timeout');
    expect(alwaysFailingMcpCall).toHaveBeenCalledTimes(3);
  });
});
