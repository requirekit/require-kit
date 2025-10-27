# Icon Code Conversion Pattern

Design pattern for converting icon codes from design tools (Zeplin, Figma) to platform-specific formats (XAML, React, Flutter).

## Problem Statement

Design tools export icon codes in various formats (HTML entities, Unicode escapes, hex literals), but target platforms require specific formats. Direct use of design tool formats often results in:

- Icons rendering as incorrect characters (e.g., Chinese characters in XAML)
- Platform-specific rendering inconsistencies
- Manual conversion overhead
- Error-prone copy-paste workflows

**Example Problem**:
```xml
<!-- From Zeplin: HTML entity format -->
<FontImageSource Glyph="&#xe5d2;" />
<!-- ❌ Renders as Chinese character: 嘒 -->

<!-- Required in XAML: Uppercase hex digits -->
<FontImageSource Glyph="&#xE5D2;" />
<!-- ✅ Renders as hamburger menu icon: ☰ -->
```

## Format Comparison

### Input Formats (Design Tools)

| Format | Example | Source | Valid? |
|--------|---------|--------|--------|
| HTML Entity (lowercase) | `&#xe5d2;` | Zeplin, Figma | ✅ |
| HTML Entity (uppercase) | `&#xE5D2;` | Zeplin, Figma | ✅ |
| Unicode Escape | `\ue5d2` | Figma, Sketch | ✅ |
| Hex Literal | `0xe5d2` | Code editors | ✅ |
| Plain Hex | `e5d2` | Documentation | ✅ |
| Decimal | `58834` | Unicode tables | ✅ |

### Output Formats (Target Platforms)

| Platform | Format | Example | Notes |
|----------|--------|---------|-------|
| XAML (.NET MAUI) | Unicode Entity | `&#xE5D2;` | **Must be uppercase** |
| C# | Unicode Escape | `\uE5D2` | Case-insensitive |
| React/JSX | Unicode Escape | `\uE5D2` | In string literals |
| Flutter | Unicode Escape | `\u{E5D2}` | Extended syntax |
| Swift | Unicode Scalar | `\u{E5D2}` | Extended syntax |
| Kotlin | Unicode Escape | `\uE5D2` | In string literals |

## Conversion Algorithm

### Core Conversion Logic

```typescript
/**
 * Converts icon code from any format to platform-specific format
 */
function convertIconCode(input: string, targetPlatform: Platform): string {
  // Step 1: Parse input to Unicode code point
  const codePoint = parseToCodePoint(input);

  // Step 2: Validate code point range
  if (!isValidIconCodePoint(codePoint)) {
    throw new Error(`Invalid icon code point: U+${codePoint.toString(16)}`);
  }

  // Step 3: Format for target platform
  return formatForPlatform(codePoint, targetPlatform);
}
```

### Step 1: Parse to Unicode Code Point

```typescript
function parseToCodePoint(input: string): number {
  // HTML entity: &#xe5d2; or &#xE5D2;
  if (/^&#x([0-9a-fA-F]+);?$/.test(input)) {
    const hex = input.match(/^&#x([0-9a-fA-F]+);?$/)[1];
    return parseInt(hex, 16);
  }

  // Unicode escape: \ue5d2 or \uE5D2
  if (/^\\u([0-9a-fA-F]{4})$/.test(input)) {
    const hex = input.match(/^\\u([0-9a-fA-F]{4})$/)[1];
    return parseInt(hex, 16);
  }

  // Hex literal: 0xe5d2 or 0xE5D2
  if (/^0x([0-9a-fA-F]+)$/.test(input)) {
    const hex = input.match(/^0x([0-9a-fA-F]+)$/)[1];
    return parseInt(hex, 16);
  }

  // Plain hex: e5d2 or E5D2
  if (/^([0-9a-fA-F]{4,6})$/.test(input)) {
    return parseInt(input, 16);
  }

  // Decimal: 58834
  if (/^\d+$/.test(input)) {
    return parseInt(input, 10);
  }

  // Single character: extract code point
  if (input.length === 1) {
    return input.codePointAt(0);
  }

  throw new Error(`Unable to parse icon code: ${input}`);
}
```

### Step 2: Validate Code Point Range

```typescript
function isValidIconCodePoint(codePoint: number): boolean {
  // Material Design Icons range: U+E000 to U+F8FF (Private Use Area)
  const MDI_MIN = 0xE000;
  const MDI_MAX = 0xF8FF;

  return codePoint >= MDI_MIN && codePoint <= MDI_MAX;
}
```

**Note**: For other icon fonts (Font Awesome, Ionicons), adjust validation range.

### Step 3: Format for Target Platform

```typescript
function formatForPlatform(codePoint: number, platform: Platform): string {
  switch (platform) {
    case Platform.XAML:
      // XAML requires uppercase hex digits
      return `&#x${codePoint.toString(16).toUpperCase()};`;

    case Platform.CSharp:
      // C# Unicode escape
      return `\\u${codePoint.toString(16).toUpperCase().padStart(4, '0')}`;

    case Platform.React:
    case Platform.TypeScript:
      // JavaScript/TypeScript Unicode escape
      return `\\u${codePoint.toString(16).padStart(4, '0')}`;

    case Platform.Flutter:
    case Platform.Swift:
      // Extended Unicode syntax
      return `\\u{${codePoint.toString(16).toUpperCase()}}`;

    case Platform.Unicode:
      // Direct Unicode character
      return String.fromCodePoint(codePoint);

    default:
      throw new Error(`Unsupported platform: ${platform}`);
  }
}
```

## Validation Rules

### Material Design Icons Validation

Material Design Icons use Unicode Private Use Area (PUA):
- **Range**: U+E000 to U+F8FF
- **Total Icons**: ~4,000 icons
- **Font Family**: "MaterialIcons"

```typescript
class MaterialDesignIconValidator {
  private static MIN = 0xE000;
  private static MAX = 0xF8FF;

  validate(codePoint: number): ValidationResult {
    if (codePoint < MaterialDesignIconValidator.MIN ||
        codePoint > MaterialDesignIconValidator.MAX) {
      return {
        valid: false,
        error: `Code point U+${codePoint.toString(16)} is outside Material Design Icons range`
      };
    }

    return { valid: true };
  }
}
```

### Font Awesome Validation

Font Awesome uses different Unicode ranges:
- **Font Awesome 5 Free**: U+F000 to U+F8FF
- **Font Awesome 6 Pro**: U+E000 to U+F8FF + others

```typescript
class FontAwesomeValidator {
  private static RANGES = [
    { min: 0xF000, max: 0xF8FF }, // FA5 Free
    { min: 0xE000, max: 0xEFFF }, // FA6 Extended
  ];

  validate(codePoint: number): ValidationResult {
    const inRange = FontAwesomeValidator.RANGES.some(
      range => codePoint >= range.min && codePoint <= range.max
    );

    return inRange
      ? { valid: true }
      : { valid: false, error: "Not a Font Awesome icon code" };
  }
}
```

## Implementation Pattern

### Adapter Pattern

Use the Adapter pattern to convert between incompatible interfaces:

```typescript
interface IconCodeAdapter {
  convert(input: string): ConversionResult;
  validate(input: string): ValidationResult;
  formatFor(platform: Platform): string;
}

class ZeplinIconAdapter implements IconCodeAdapter {
  convert(zeplinCode: string): ConversionResult {
    // Parse Zeplin format (HTML entity)
    const codePoint = this.parseZeplinFormat(zeplinCode);

    // Validate
    const validation = this.validator.validate(codePoint);
    if (!validation.valid) {
      return { success: false, error: validation.error };
    }

    // Convert to target formats
    return {
      success: true,
      codePoint,
      xaml: this.formatXaml(codePoint),
      csharp: this.formatCSharp(codePoint),
      unicode: String.fromCodePoint(codePoint)
    };
  }
}
```

### Strategy Pattern

Use Strategy pattern for platform-specific formatting:

```typescript
interface FormattingStrategy {
  format(codePoint: number): string;
}

class XamlFormattingStrategy implements FormattingStrategy {
  format(codePoint: number): string {
    return `&#x${codePoint.toString(16).toUpperCase()};`;
  }
}

class CSharpFormattingStrategy implements FormattingStrategy {
  format(codePoint: number): string {
    return `\\u${codePoint.toString(16).toUpperCase().padStart(4, '0')}`;
  }
}

class IconFormatter {
  constructor(private strategy: FormattingStrategy) {}

  format(codePoint: number): string {
    return this.strategy.format(codePoint);
  }
}
```

## Usage Examples

### Example 1: Zeplin to XAML

```typescript
import { IconCodeAdapter } from './utils/icon-converter';

const adapter = new IconCodeAdapter();

// Input from Zeplin (lowercase HTML entity)
const zeplinCode = "&#xe5d2;";

// Convert
const result = adapter.convert(zeplinCode);

if (result.success) {
  console.log(result.xamlFormat); // "&#xE5D2;"

  // Use in XAML
  const xaml = `
    <FontImageSource FontFamily="{StaticResource IconsFontFamily}"
                     Glyph="${result.xamlFormat}"
                     Color="White"
                     Size="34" />
  `;
}
```

### Example 2: Batch Conversion

```typescript
import { batchConvert } from './utils/icon-converter';

const zeplinCodes = [
  "&#xe5d2;", // Menu
  "&#xe8b1;", // Lightbulb
  "&#xe241;", // Label
  "&#xe86c;", // Check
];

const results = batchConvert(zeplinCodes);

results.forEach((result, index) => {
  if (result.success) {
    console.log(`Icon ${index + 1}:`);
    console.log(`  Original: ${result.originalCode}`);
    console.log(`  XAML: ${result.xamlFormat}`);
    console.log(`  C#: ${result.csharpFormat}`);
    console.log(`  Unicode: ${result.convertedCode}`);
  } else {
    console.error(`Icon ${index + 1} failed: ${result.error}`);
  }
});
```

### Example 3: Validation Before Conversion

```typescript
import { validateIconCode } from './utils/icon-converter';

const iconCode = "&#xe5d2;";

const validation = validateIconCode(iconCode);

if (validation.isValid) {
  console.log(`✅ Valid icon code: ${validation.iconName}`);
  console.log(`   Code point: U+${validation.codePoint.toString(16).toUpperCase()}`);

  // Proceed with conversion
  const result = adapter.convert(iconCode);
} else {
  console.error(`❌ Invalid icon code: ${validation.error}`);
}
```

## Error Handling

### Common Errors

1. **Invalid Format**
   ```typescript
   Error: Unable to parse icon code: "invalid"
   Solution: Use supported format (HTML entity, Unicode escape, hex)
   ```

2. **Out of Range**
   ```typescript
   Error: Code point U+FFFF is outside Material Design Icons range (U+E000 to U+F8FF)
   Solution: Verify icon code is from Material Design Icons font
   ```

3. **Empty Input**
   ```typescript
   Error: Icon code is empty or null
   Solution: Provide valid icon code string
   ```

### Error Recovery

```typescript
function convertWithFallback(iconCode: string, fallback: string): string {
  try {
    const result = adapter.convert(iconCode);

    if (result.success) {
      return result.xamlFormat;
    } else {
      console.warn(`Icon conversion failed: ${result.error}. Using fallback.`);
      return fallback;
    }
  } catch (error) {
    console.error(`Icon conversion error: ${error.message}. Using fallback.`);
    return fallback;
  }
}

// Usage
const xamlGlyph = convertWithFallback(
  "&#xe5d2;",
  "&#xE5D2;" // Fallback to known-good format
);
```

## Performance Considerations

### Caching

Cache conversion results to avoid redundant parsing:

```typescript
class CachedIconConverter {
  private cache = new Map<string, ConversionResult>();

  convert(iconCode: string): ConversionResult {
    // Check cache first
    if (this.cache.has(iconCode)) {
      return this.cache.get(iconCode);
    }

    // Convert and cache
    const result = this.adapter.convert(iconCode);
    this.cache.set(iconCode, result);

    return result;
  }
}
```

### Batch Processing

Process multiple icons in parallel:

```typescript
async function batchConvertAsync(iconCodes: string[]): Promise<ConversionResult[]> {
  const promises = iconCodes.map(code =>
    Promise.resolve(adapter.convert(code))
  );

  return Promise.all(promises);
}
```

### Performance Targets

- **Single Conversion**: <1ms
- **Batch Conversion (100 icons)**: <10ms
- **Validation**: <0.5ms per icon
- **Memory**: <1KB per cached result

## Testing Strategy

### Unit Tests

```typescript
describe('IconCodeAdapter', () => {
  it('should convert lowercase HTML entity to XAML format', () => {
    const result = adapter.convert("&#xe5d2;");
    expect(result.success).toBe(true);
    expect(result.xamlFormat).toBe("&#xE5D2;");
  });

  it('should validate Material Design Icons range', () => {
    const result = adapter.convert("&#xFFFF;");
    expect(result.success).toBe(true);
    expect(result.warnings).toContain(/outside Material Design Icons range/);
  });

  it('should handle invalid input gracefully', () => {
    const result = adapter.convert("invalid");
    expect(result.success).toBe(false);
    expect(result.error).toContain("Unable to parse icon code");
  });
});
```

### Integration Tests

```typescript
describe('Zeplin-to-MAUI Icon Integration', () => {
  it('should convert all icons in generated XAML', async () => {
    const xaml = await generateXamlFromZeplin(zeplinUrl);

    // Extract all Glyph attributes
    const glyphs = extractGlyphAttributes(xaml);

    // Verify all are uppercase format
    glyphs.forEach(glyph => {
      expect(glyph).toMatch(/^&#x[0-9A-F]+;$/);
    });
  });
});
```

## Related Patterns

- **Adapter Pattern**: Convert between incompatible interfaces
- **Strategy Pattern**: Platform-specific formatting strategies
- **Factory Pattern**: Create validators for different icon fonts
- **Result Pattern**: Explicit error handling without exceptions

## References

### Material Design Icons
- [Google Material Design Icons](https://fonts.google.com/icons)
- [Material Icons Codepoints](https://github.com/google/material-design-icons/blob/master/font/MaterialIcons-Regular.codepoints)

### Unicode Standards
- [Unicode Private Use Area](https://unicode.org/charts/PDF/UE000.pdf)
- [Unicode Character Code Charts](https://unicode.org/charts/)

### Platform Documentation
- [.NET MAUI Fonts](https://learn.microsoft.com/en-us/dotnet/maui/user-interface/fonts)
- [XAML Escape Sequences](https://learn.microsoft.com/en-us/dotnet/desktop/xaml-services/escape-sequence-markup-extension)

---

**Last Updated**: 2025-10-16
**Version**: 1.0.0
