/**
 * Icon Code Converter
 *
 * Converts icon codes from various formats (HTML entities, Unicode) to XAML-compatible formats.
 * Primarily handles Material Design Icons conversion for Zeplin-to-MAUI workflow.
 *
 * @module icon-converter
 * @version 1.0.0
 */

/**
 * Result of icon conversion operation
 */
export interface IconConversionResult {
  success: boolean;
  originalCode: string;
  convertedCode?: string;
  xamlFormat?: string;
  csharpFormat?: string;
  unicodeCodePoint?: number;
  error?: string;
  warnings?: string[];
}

/**
 * Validation result for icon codes
 */
export interface IconValidationResult {
  isValid: boolean;
  iconName?: string;
  codePoint?: number;
  error?: string;
}

/**
 * Strategy interface for icon validation
 * Extensible for different icon font families
 */
export interface IconValidationStrategy {
  /**
   * Validates if the code point belongs to the icon font family
   */
  validate(codePoint: number): IconValidationResult;

  /**
   * Returns the name of the icon font family
   */
  getFontFamilyName(): string;
}

/**
 * Material Design Icons validator
 * Validates icon codes within the Material Design Icons range (U+E000 to U+F8FF)
 */
export class MaterialDesignIconValidator implements IconValidationStrategy {
  private static readonly MIN_CODE_POINT = 0xE000;
  private static readonly MAX_CODE_POINT = 0xF8FF;
  private static readonly FONT_FAMILY_NAME = "MaterialIcons";

  /**
   * Validates if code point is within Material Design Icons range
   */
  validate(codePoint: number): IconValidationResult {
    if (codePoint < MaterialDesignIconValidator.MIN_CODE_POINT ||
        codePoint > MaterialDesignIconValidator.MAX_CODE_POINT) {
      return {
        isValid: false,
        codePoint,
        error: `Code point U+${codePoint.toString(16).toUpperCase()} is outside Material Design Icons range (U+E000 to U+F8FF)`
      };
    }

    return {
      isValid: true,
      codePoint,
      iconName: `icon-U+${codePoint.toString(16).toUpperCase()}`
    };
  }

  getFontFamilyName(): string {
    return MaterialDesignIconValidator.FONT_FAMILY_NAME;
  }
}

/**
 * Adapter for converting icon codes between different formats
 * Implements Adapter pattern for format conversion
 */
export class IconCodeAdapter {
  private validator: IconValidationStrategy;

  /**
   * Creates a new IconCodeAdapter
   * @param validator - Validation strategy (default: MaterialDesignIconValidator)
   */
  constructor(validator: IconValidationStrategy = new MaterialDesignIconValidator()) {
    this.validator = validator;
  }

  /**
   * Converts icon code from any supported format to XAML and C# formats
   *
   * Supported input formats:
   * - HTML entity (lowercase): &#xe5d2;
   * - HTML entity (uppercase): &#xE5D2;
   * - Unicode escape: \ue5d2
   * - Hex literal: 0xe5d2
   * - Plain hex: e5d2 (must contain a-f)
   * - Decimal: 58834
   *
   * @param iconCode - Icon code in any supported format
   * @returns Conversion result with XAML and C# formats
   *
   * @example
   * ```typescript
   * const adapter = new IconCodeAdapter();
   * const result = adapter.convert("&#xe5d2;");
   * if (result.success) {
   *   console.log(result.xamlFormat); // "&#xE5D2;"
   *   console.log(result.csharpFormat); // "\uE5D2"
   * }
   * ```
   */
  convert(iconCode: string): IconConversionResult {
    const warnings: string[] = [];

    // Normalize input
    const normalizedCode = iconCode.trim();

    if (!normalizedCode) {
      return {
        success: false,
        originalCode: iconCode,
        error: "Icon code is empty or null"
      };
    }

    try {
      // Parse the icon code to get code point
      const codePoint = this.parseIconCode(normalizedCode);

      if (codePoint === null) {
        return {
          success: false,
          originalCode: iconCode,
          error: `Unable to parse icon code format: "${normalizedCode}"`
        };
      }

      // Validate code point
      const validationResult = this.validator.validate(codePoint);

      if (!validationResult.isValid) {
        warnings.push(validationResult.error || "Icon code validation failed");
      }

      // Convert to target formats
      const xamlFormat = this.formatForXaml(codePoint);
      const csharpFormat = this.formatForCSharp(codePoint);
      const unicodeChar = String.fromCodePoint(codePoint);

      return {
        success: true,
        originalCode: iconCode,
        convertedCode: unicodeChar,
        xamlFormat,
        csharpFormat,
        unicodeCodePoint: codePoint,
        warnings: warnings.length > 0 ? warnings : undefined
      };
    } catch (error) {
      return {
        success: false,
        originalCode: iconCode,
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }

  /**
   * Parses icon code from various formats to Unicode code point
   *
   * @param iconCode - Icon code string
   * @returns Unicode code point or null if parsing fails
   */
  private parseIconCode(iconCode: string): number | null {
    // Format 1: HTML entity (&#xe5d2; or &#xE5D2;)
    const htmlEntityMatch = iconCode.match(/^&#x([0-9a-fA-F]+);?$/);
    if (htmlEntityMatch && htmlEntityMatch[1]) {
      return parseInt(htmlEntityMatch[1], 16);
    }

    // Format 2: Unicode escape (\ue5d2 or \uE5D2)
    const unicodeEscapeMatch = iconCode.match(/^\\u([0-9a-fA-F]{4})$/);
    if (unicodeEscapeMatch && unicodeEscapeMatch[1]) {
      return parseInt(unicodeEscapeMatch[1], 16);
    }

    // Format 3: Hex literal (0xe5d2 or 0xE5D2)
    const hexLiteralMatch = iconCode.match(/^0x([0-9a-fA-F]+)$/);
    if (hexLiteralMatch && hexLiteralMatch[1]) {
      return parseInt(hexLiteralMatch[1], 16);
    }

    // Format 4: Plain hex (e5d2 or E5D2) - must contain at least one a-f letter
    // This ensures "58834" is treated as decimal, not hex
    const plainHexMatch = iconCode.match(/^([0-9a-fA-F]{4,6})$/);
    if (plainHexMatch && plainHexMatch[1]) {
      const hexStr = plainHexMatch[1];
      // Check if it contains at least one hex letter (a-f, A-F)
      if (/[a-fA-F]/.test(hexStr)) {
        return parseInt(hexStr, 16);
      }
    }

    // Format 5: Decimal number (58834)
    const decimalMatch = iconCode.match(/^(\d+)$/);
    if (decimalMatch && decimalMatch[1]) {
      return parseInt(decimalMatch[1], 10);
    }

    // Format 6: Already a Unicode character
    if (iconCode.length === 1) {
      return iconCode.codePointAt(0) || null;
    }

    return null;
  }

  /**
   * Formats code point as XAML Unicode entity
   *
   * @param codePoint - Unicode code point
   * @returns XAML format: &#xE5D2;
   */
  private formatForXaml(codePoint: number): string {
    const hexCode = codePoint.toString(16).toUpperCase();
    return `&#x${hexCode};`;
  }

  /**
   * Formats code point as C# Unicode escape
   *
   * @param codePoint - Unicode code point
   * @returns C# format: \uE5D2
   */
  private formatForCSharp(codePoint: number): string {
    const hexCode = codePoint.toString(16).toUpperCase().padStart(4, '0');
    return `\\u${hexCode}`;
  }

  /**
   * Gets the font family name from the validator
   */
  getFontFamilyName(): string {
    return this.validator.getFontFamilyName();
  }
}

/**
 * Converts HTML entity format to direct Unicode character
 * Convenience function for simple conversions
 *
 * @param htmlEntity - HTML entity (e.g., "&#xe5d2;")
 * @returns Unicode character or null if conversion fails
 *
 * @example
 * ```typescript
 * const char = convertHtmlEntityToUnicode("&#xe5d2;");
 * console.log(char); // "" (hamburger menu icon)
 * ```
 */
export function convertHtmlEntityToUnicode(htmlEntity: string): string | null {
  const adapter = new IconCodeAdapter();
  const result = adapter.convert(htmlEntity);
  return result.success && result.convertedCode ? result.convertedCode : null;
}

/**
 * Formats icon code for XAML Glyph attribute
 *
 * @param iconCode - Icon code in any supported format
 * @returns XAML-formatted icon code or null if conversion fails
 *
 * @example
 * ```typescript
 * const xaml = formatForXaml("&#xe5d2;");
 * console.log(xaml); // "&#xE5D2;"
 * ```
 */
export function formatForXaml(iconCode: string): string | null {
  const adapter = new IconCodeAdapter();
  const result = adapter.convert(iconCode);
  return result.success && result.xamlFormat ? result.xamlFormat : null;
}

/**
 * Formats icon code for C# string literals
 *
 * @param iconCode - Icon code in any supported format
 * @returns C#-formatted icon code or null if conversion fails
 *
 * @example
 * ```typescript
 * const csharp = formatForCSharp("&#xe5d2;");
 * console.log(csharp); // "\uE5D2"
 * ```
 */
export function formatForCSharp(iconCode: string): string | null {
  const adapter = new IconCodeAdapter();
  const result = adapter.convert(iconCode);
  return result.success && result.csharpFormat ? result.csharpFormat : null;
}

/**
 * Batch converts multiple icon codes
 *
 * @param iconCodes - Array of icon codes
 * @returns Array of conversion results
 *
 * @example
 * ```typescript
 * const codes = ["&#xe5d2;", "&#xe8b1;", "&#xe241;"];
 * const results = batchConvert(codes);
 * results.forEach(result => {
 *   if (result.success) {
 *     console.log(`${result.originalCode} -> ${result.xamlFormat}`);
 *   }
 * });
 * ```
 */
export function batchConvert(iconCodes: string[]): IconConversionResult[] {
  const adapter = new IconCodeAdapter();
  return iconCodes.map(code => adapter.convert(code));
}

/**
 * Validates an icon code without converting
 *
 * @param iconCode - Icon code to validate
 * @returns Validation result
 *
 * @example
 * ```typescript
 * const result = validateIconCode("&#xe5d2;");
 * console.log(result.isValid); // true
 * ```
 */
export function validateIconCode(iconCode: string): IconValidationResult {
  const adapter = new IconCodeAdapter();
  const conversionResult = adapter.convert(iconCode);

  if (!conversionResult.success) {
    return {
      isValid: false,
      error: conversionResult.error
    };
  }

  return {
    isValid: true,
    codePoint: conversionResult.unicodeCodePoint,
    iconName: `U+${conversionResult.unicodeCodePoint?.toString(16).toUpperCase()}`
  };
}

// Default export
export default {
  IconCodeAdapter,
  MaterialDesignIconValidator,
  convertHtmlEntityToUnicode,
  formatForXaml,
  formatForCSharp,
  batchConvert,
  validateIconCode
};
